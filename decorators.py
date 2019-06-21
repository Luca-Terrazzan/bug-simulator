# Testing decorators out
def do_twice(callee):
    def wrapper():
        callee()
        callee()
    return wrapper
