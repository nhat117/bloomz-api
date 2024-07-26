import torch
from transformers import AutoModelForCausalLM, BloomTokenizerFast
import pytesseract
from pdf2image import convert_from_path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re

# Model and tokenizer initialization
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = AutoModelForCausalLM.from_pretrained(
    "bigscience/bloomz-3b",
    load_in_4bit=True,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True
).to(device)

tokenizer = BloomTokenizerFast.from_pretrained('bigscience/bloom')

# Initialize Sentence Transformer model
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
dimension = 384  # Dimension of the embeddings

# Dictionary to store FAISS indices for each user
user_indices = {}

def extract_text_from_pdf(file_path):
    images = convert_from_path(file_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def llama_1_prompt(input):
    system = "You are a friendly and safe assistant. Provide suitable answer base on the provide instruction below"
    question_prefix = " ### Question: "
    answer_prefix = "\n ### Answer:"
    return system + question_prefix + input + answer_prefix

def chat(input_chat):
    model.config.pad_token_id = tokenizer.pad_token_id = 0  # unk
    model.config.bos_token_id = 1
    model.config.eos_token_id = 2
    encoding = tokenizer(llama_1_prompt(input_chat), padding=True, return_tensors="pt").to(device)
    output = model.generate(
        input_ids=encoding.input_ids,
        attention_mask=encoding.attention_mask,
        temperature=0.3,
        top_p=0.75,
        top_k=40,
        num_beams=4,
        max_new_tokens=1000,
    )
    res_raw = tokenizer.decode(output[0], skip_special_tokens=True)
    res = extract_text(res_raw)
    return res if res is not None else res_raw 

def extract_text(input_string):
    pattern = r'### Answer:\s+(.*?)\s*(?:###|$)'
    matches = re.findall(pattern, input_string, re.DOTALL)
    return matches[0].replace("", "") if matches else None

def store_in_vector_db(text, user_id):
    sentences = text.split('. ')
    embeddings = sentence_model.encode(sentences)

    if user_id not in user_indices:
        user_indices[user_id] = faiss.IndexFlatL2(dimension)
    
    user_indices[user_id].add(np.array(embeddings))

def query_vector_db(query, user_id):
    if user_id not in user_indices:
        return None

    query_embedding = sentence_model.encode([query])
    D, I = user_indices[user_id].search(np.array(query_embedding), k=1)
    return I[0][0] if I[0][0] != -1 else None
