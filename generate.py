
import os
import torch
from mingpt.model import GPT
from mingpt.utils import CfgNode as CN
import pickle


# --- Load character mappings ---
with open("vocab.pkl", "rb") as f:
    stoi, itos = pickle.load(f)

vocab_size = len(stoi)
encode = lambda s: [stoi.get(c, 0) for c in s]
decode = lambda l: ''.join([itos[i] for i in l])

# --- Load model ---
block_size = 64

model_config = GPT.get_default_config()
model_config.model_type = None
model_config.vocab_size = vocab_size
model_config.block_size = block_size
model_config.n_layer = 2
model_config.n_head = 2
model_config.n_embd = 128

model = GPT(model_config)
model.load_state_dict(torch.load("trained_model.pt", map_location='cpu'))
model.eval()

# --- Generate text ---
def generate(prompt, max_new_tokens=50):
    context = torch.tensor([encode(prompt)], dtype=torch.long)
    idx = context
    with torch.no_grad():
        idx = model.generate(idx, max_new_tokens=max_new_tokens, temperature=1.0, do_sample=False)
    print(decode(idx[0].tolist()))

# --- Example usage ---
prompt = "Employee: John Smith | Department: HR | Salary:"
generate(prompt)
