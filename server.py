from websocket_server import WebSocket, Server
clients = []
class MySimpleWebSocketServer(WebSocket):

    
    def handle_message(self):
        print("message rec ")
        for client in clients:
            client.send_message({self.data})
        pass

    def handle_connected(self):
        print("connectedAtServer")
        clients.append(self)
        pass

    def handle_close(self):
        """
            Called when a websocket server gets a Close frame from a client.
        """
        pass


server = Server('127.0.0.1', 9001, MySimpleWebSocketServer)
server.serveforever()