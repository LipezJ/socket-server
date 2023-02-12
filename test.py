import client

def printPost(data, socket_):
    print('-> ', data['post'])

s = client.Client('localhost', 8080)
s.connect()

s.addFunction('post', printPost)

room = input('room: ')
if len(room) > 0:
    s.join(room)

to = input('usuario: ')

while True:
    post = input('mensaje: ')
    if post == '0':
        break
    if len(room) > 0:
        s.roomDo ('post', room, {'post': post})
    elif len(to) > 0:
        s.userDo('post', to, {'post': post})
    #s.do('mem', {})

s.roomDo('leaveAll')

s.socket_.close()