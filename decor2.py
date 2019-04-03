def my_decorator(my_func):
    def wrapper():
        print("something1")
        my_func()
        print("something2")
    return wrapper

@my_decorator
def say_whee():
    print("say whee")
