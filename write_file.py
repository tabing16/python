#===============================================================================
# with open('dog_breeds.txt','r') as reader:
#     for fline in reader.readlines():
#         print(fline, end='')
#===============================================================================

with open('dog_breeds.txt','r') as reader:
    dog_breeds = reader.readlines()

with open('dog_breeds_reverse.txt','w') as writer:
    for breed in reversed(dog_breeds):
        writer.write(breed)