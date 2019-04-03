import argparse
import os
from builtins import str


def str2unix(input_str: str) -> str:
    r_str = input_str.replace('\r\n', '\n')
    return r_str


def dos2unix(source_file: str, dest_file: str):
    with open(source_file, 'r') as reader:
        dos_content = reader.read()
        
    unix_content = str2unix(dos_content)
    
    with open(dest_file,'w') as writer:
        writer.write(unix_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts DOS like file to UNIX like file")
    
    parser.add_argument('--source_file', help='The location of the source')
    parser.add_argument('--dest_file', help='The Location of the destination file', default=None)
    
    args = parser.parse_args()
    
    s_file = args.source_file
    d_file = args.dest_file
    
    if d_file is None:
        file_path, file_extension = os.path.splitext(s_file)
        d_file = f'{file_path}_unix{file_extension}'
        
    dos2unix(s_file, d_file)
