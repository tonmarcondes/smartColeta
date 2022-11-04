import hashlib

def SHA256(mensage):
    return hashlib.sha256(mensage.encode("utf-8")).hexdigest()