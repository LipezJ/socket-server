import os
from client import Client

def eject(data, socket_):
    print('ejecutando', data['program'])
    if 'props' in data:
        props = data['props']
    else: props = ''
    os.system('start ' + data['program'] + props)
    

s = Client('localhost', 8080)
s.connect()

s.addFunction('eject', eject)

user = input('user: ')
program = input('program: ')

s.userDo('eject', user, {'program': program})

s.close()