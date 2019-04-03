import json

def decode_complex(dct):
    if "__complex__" in dct:
        return complex(dct["real"], dct["imaginary"])
    else:
        return dct

with open("complex_data.json") as complex_data:
    data = complex_data.read()
    z = json.loads(data, object_hook=decode_complex)

print(type(z))
print(z)