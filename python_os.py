import os

mydir = os.path.join('dist','csv')


def check_single_file(directory):
    single_file = True
    # root_dir = os.path.join('dist','csv')
    extensions = '.csv'
    files_arr = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[-1]
            if ext in extensions:
                files_arr.append(files)
    if(len(files_arr) != 1):
        single_file = False
    return single_file

if check_single_file(mydir):
    print('Single File')
else:
    print('Multiple File')