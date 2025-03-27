
import json
from crypto_utils import decrypt_aes
import base64

def load_keys(aes_key_path, aes_iv_path):
    with open(aes_key_path, "rb") as f:
        key = f.read()
    with open(aes_iv_path, "rb") as f:
        iv = f.read()
    return key, iv

def load_dataset(path):
    with open(path, 'r') as f:
        return json.load(f)

def prepare_sample(sample, user_role, user_name=None, aes_key=None, aes_iv=None):
    tokens = []
    tokens.append(f"Employee: {sample['employee']}")
    tokens.append(f"Department: {sample['department']}")

    access_roles = sample["policy"]["salary"]["access"]
    encrypted_salary = sample["salary"]

    if user_role in access_roles or (user_role == "Employee" and sample["employee"] == user_name):
        if sample["policy"]["salary"]["encrypted"] and aes_key and aes_iv:
            salary = decrypt_aes(encrypted_salary, aes_key, aes_iv)
        else:
            salary = encrypted_salary
    else:
        salary = "[MASK]"

    tokens.append(f"Salary: {salary}")
    return " | ".join(tokens)
