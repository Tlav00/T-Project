import certifi

path = certifi.where()
context.load_verify_locations(path)