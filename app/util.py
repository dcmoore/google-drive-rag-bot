import os

def read_secret(secret_name):
  secret_path = f"/run/secrets/{secret_name}"
  if os.path.exists(secret_path):
    with open(secret_path, 'r') as secret_file:
      return secret_file.read().strip()
  return os.getenv(secret_name.upper())
