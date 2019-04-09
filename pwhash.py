import hashlib

def makeHash(pw):
    return hashlib.sha256(str.encode(pw)).hexdigest()

def checkHash(pw, hash):
    if makeHash(pw) == hash:
        return True
    return False
