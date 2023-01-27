import uuid

class socketDict:
    def __init__(self):
        self.bySocket = {}
        self.byId = {}

    def add(self, uuid, socket):
        self.bySocket[uuid] = socket
        self.byId[socket] = uuid

    def remove(self, socket):
        if socket in self.byId:
            id = self.byId.pop(socket)
            del self.bySocket[id]
        else:
            raise ValueError('UUID or socket not found')