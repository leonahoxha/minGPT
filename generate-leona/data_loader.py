
import json

def load_dataset(path):
    with open(path, 'r') as f:
        return json.load(f)

def decrypt(value):
    if value.startswith("ENC(") and value.endswith(")"):
        return value[4:-1]
    return value

def prepare_sample(sample, user_role, user_name=None):
    tokens = []
    tokens.append(f"Employee: {sample['employee']}")
    tokens.append(f"Department: {sample['department']}")

    access_roles = sample["policy"]["salary"]["access"]
    if user_role in access_roles or (user_role == "Employee" and sample["employee"] == user_name):
        salary = decrypt(sample["salary"])
    else:
        salary = "[MASK]"

    tokens.append(f"Salary: {salary}")
    return " | ".join(tokens)


from data_loader import load_dataset, prepare_sample

data = load_dataset("../data/encryption_dataset.json")

print(prepare_sample(data[0], user_role="HR"))
print(prepare_sample(data[1], user_role="Manager"))
print(prepare_sample(data[2], user_role="Employee", user_name="Carol Lee"))
