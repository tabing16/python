import struct
import os


class File:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    @staticmethod
    def write_string(name, value):
        with open(name, 'a') as writer:
            writer.write(value)

    @staticmethod
    def write_binary(name, value):
        with open(name, 'ab') as writer:
            writer.write(value)

    def put_string(self, val, length, mode=1):
        if mode == 1:
            self.write_string(self.name, val.ljust(length, " "))
        elif mode == 2:
            self.write_string(self.name, str(val).rjust(length, "0"))

    def put_bint(self, val):
        self.write_binary(self.name, struct.pack('<H', val))

    def put_bfloat(self, val):
        self.write_binary(self.name, struct.pack('<f', val))


my_file = File('MV90_MDEF_EXPORT_1234.TXT')

if os.path.exists(my_file.get_name()):
    os.remove(my_file.get_name())

my_file.put_string("10", 10)
