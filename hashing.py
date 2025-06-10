import hashlib

def compute_pdf_hash(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    return hashlib.md5(pdf_bytes).hexdigest()