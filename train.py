
import os
import torch
from torch.utils.data import Dataset
from mingpt.model import GPT
from mingpt.trainer import Trainer
from mingpt.utils import CfgNode as CN
import matplotlib.pyplot as plt
import pickle

# --- Optional: Toggle masking ---
MASK_SALARY = True

# --- Masking logic ---
def mask_salary(text, mask_token="[MASK]"):
    lines = text.splitlines()
    masked = []
    for line in lines:
        parts = line.split("|")
        masked_line = []
        for part in parts:
            if "Salary:" in part:
                masked_line.append(f"Salary: {mask_token}")
            else:
                masked_line.append(part.strip())
        masked.append(" | ".join(masked_line))
    return "\n".join(masked)

# --- Load and encode the dataset ---
data_path = os.path.join('data', 'employee info', 'input.txt')
with open(data_path, 'r') as f:
    raw_text = f.read()
    text = mask_salary(raw_text) if MASK_SALARY else raw_text

chars = sorted(list(set(text)))
vocab_size = len(chars)
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

with open("vocab.pkl", "wb") as f:
    pickle.dump((stoi, itos), f)

encode = lambda s: [stoi[c] for c in s]
decode = lambda l: ''.join([itos[i] for i in l])

data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9 * len(data))
train_data = data[:n]
val_data = data[n:]

# --- Dataset class ---
class CharDataset(Dataset):
    def __init__(self, data, block_size):
        self.data = data
        self.block_size = block_size

    def __len__(self):
        return len(self.data) - self.block_size

    def __getitem__(self, idx):
        chunk = self.data[idx:idx + self.block_size + 1]
        x = chunk[:-1]
        y = chunk[1:]
        return x, y

# --- Configurations ---
block_size = 64
batch_size = 32
train_dataset = CharDataset(train_data, block_size)

# --- Model configuration ---
model_config = GPT.get_default_config()
model_config.model_type = None
model_config.vocab_size = vocab_size
model_config.block_size = block_size
model_config.n_layer = 2
model_config.n_head = 2
model_config.n_embd = 128

model = GPT(model_config)

# --- Trainer configuration ---
train_config = Trainer.get_default_config()
train_config.learning_rate = 1e-3
train_config.batch_size = batch_size
train_config.max_iters = 500
train_config.num_workers = 0

trainer = Trainer(train_config, model, train_dataset)

# --- Log training losses ---
train_losses = []

def log_loss(trainer_instance):
    train_losses.append(trainer_instance.loss.item())

trainer.add_callback('on_batch_end', log_loss)

# --- Run training ---
trainer.run()

# --- Plot and save training loss ---
plt.plot(train_losses)
plt.xlabel("Iteration")
plt.ylabel("Training Loss")
plt.title("minGPT Training Loss")
plt.grid(True)
plt.savefig("training_loss.png")
print("Training loss plot saved as training_loss.png")


# --- Save trained model ---
torch.save(model.state_dict(), 'trained_model.pt')
print("Trained model saved as trained_model.pt")


