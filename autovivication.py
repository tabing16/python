class AutoVivication(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

a = AutoVivication()

a[1][2] = 5.2

print(a)