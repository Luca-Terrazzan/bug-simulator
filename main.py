import json

from decorators import do_twice


@do_twice
def print_something():
    print('hello!')

print_something()

myjson = open('test.json', 'r')
myjson = json.loads(myjson.read())

print(f'my json is: {myjson}')
print(f'array second val: {myjson[2][1]}')
