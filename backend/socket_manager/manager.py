class Connections():
    def __init__(self):
        self.active_connections = {}

    def add_sockets(self,user_id,ws):
        self.active_connections[user_id] = ws

    def remove_socket(self,user_id):
        self.active_connections.pop(user_id)

    async def broadcast_msg(self,attack):
        for ws in self.active_connections.values():
            await ws.send_json(attack)

manager = Connections()