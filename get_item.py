class Building(object):
    def __init__(self, floors):
        self.floors = [None] * floors

    def __setitem__(self, floor_number, data):
        self.floors[floor_number] = data

    def __getitem__(self, floor_number):
        return self.floors[floor_number]

building1 = Building(4)
building1[0] = 4

print(building1[0])