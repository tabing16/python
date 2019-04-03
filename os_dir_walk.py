import os

root_dir = '.'

for dir_name,sub_dir_list,file_list in os.walk(root_dir):
    print ('Found Directory: %s' % dir_name)
    for file_name in file_list:
        print('\t%s' % file_name)
        