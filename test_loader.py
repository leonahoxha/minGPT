from data_loader import load_dataset, prepare_sample, load_keys

# Load keys
key, iv = load_keys("crypto_keys/aes_key.bin", "crypto_keys/aes_iv.bin")

# Load encrypted dataset
data = load_dataset("encryption_dataset_encrypted.json")

# Test with different roles
print(prepare_sample(data[0], user_role="HR", aes_key=key, aes_iv=iv))         # should show salary
print(prepare_sample(data[1], user_role="Manager", aes_key=key, aes_iv=iv))    # should be [MASK]
print(prepare_sample(data[2], user_role="Employee", user_name="Carol Lee", aes_key=key, aes_iv=iv))  # should show salary
print(prepare_sample(data[0], user_role="Employee", user_name="Someone Else", aes_key=key, aes_iv=iv))  # should be [MASK]
