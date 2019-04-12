class A:
    message = "Class message"

    @classmethod
    def cfoo(cls):
        print(cls.message)

    def foo(self, msg):
        self.message = msg
        print(self.message)


