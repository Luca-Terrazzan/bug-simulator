import json
from typing import List

from decorators import do_twice


@do_twice
def print_something():
    print('hello!')

print_something()

myJSON = open('test.json', 'r')
myJSON = json.loads(myJSON.read())

print(f'my json is: {myJSON}')

jsonSecondValue = myJSON['anarray']

print(type(jsonSecondValue))

print(f'array second val: {jsonSecondValue}')
