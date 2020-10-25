import json
from addonLoader import *
from socketserver import TCPServer, StreamRequestHandler

class Handler(StreamRequestHandler):
    games = addon_loader()
    
    def handle(self) -> None:
        print(f"Connection from: {self.client_address}")
        while True:
            raw = self.rfile.readline()
            command = raw.decode(encoding="utf-8").strip().lower()
            print(f"{self.client_address[0]} wrote:\n{command}")
            if command == "gamelist":
                print(f"Sending:\n{json.dumps(self.games)}")
                gamelist = json.dumps(self.games) + "\n"
                self.wfile.write(gamelist.encode("utf-8"))
            elif command == "":
                print(f"Disconnecting from: {self.client_address}")
                break


def start_server() -> None:
    with TCPServer(("127.0.0.1", 12345), Handler) as server:
        server.serve_forever()


if __name__ == "__main__":
    start_server()
