import base64

# Read the contents of the file as bytes
with open('entropy.py', 'rb') as f:
    contents = f.read()

# Encode the bytes as Base64
encoded = base64.b64encode(contents)

# Decode the Base64 as a string
result = encoded.decode('utf-8')

print(result)
