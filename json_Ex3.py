import json

class Person:
    def __init__(self, name, age):
        self.name = name
        self. age = age

def complex_encoder(z):
    if isinstance(z, complex):
        return(z.real, z.imag)
    else:
        type_name = z.__class__.__name__
        raise TypeError(f"Object of type {type_name} is not JSON Serializable")

class ComplexEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(self, z):
            return(z.real, z.imag)
        else:
            super().default(self, z)

json_str = json.dumps( 4 + 6j, default=complex_encoder)

