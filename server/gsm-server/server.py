import json
from socketserver import StreamRequestHandler, ThreadingTCPServer, BaseServer
from typing import Tuple, Any

from PySignal import Signal


class GSMServer(ThreadingTCPServer):
    class Handler(StreamRequestHandler):
        def __init__(
            self, request: Any, client_address: Any, server: BaseServer, command: Signal
        ) -> None:
            self.response = Signal()
            self.command = command
            self.response.connect(self.send_response)
            super().__init__(request, client_address, server)

        def handle(self) -> None:
            print(f"Connection from: {self.client_address}")
            while True:
                raw = self.rfile.readline()
                command = raw.decode(encoding="utf-8").strip().lower()
                if command == "":
                    print(f"Disconnecting from: {self.client_address}")
                    break
                print(f"{self.client_address[0]} wrote: {command}")
                self.command.emit(self.response, command)

        def send_response(self, msg: bytes):
            print(f"Sending:\n{str(msg, encoding='utf-8')}")
            self.wfile.write(msg)

    def __init__(self):
        self.command = Signal()
        self.command.connect(self.handle_command)
        self.games = {
            "game2": {
                "exec": "program1",
                "args": {
                    "-a1": {"default": 100, "editable": False},
                    "-a2": {"default": 200},
                },
            },
            "game1": {"exec": "program2", "args": {"-a3": {"default": 300}}},
        }
        self.address = ("127.0.0.1", 12345)

        super().__init__(
            server_address=self.address,
            RequestHandlerClass=self.Handler,
            bind_and_activate=True,
        )
        self.serve_forever()

    def handle_command(self, return_signal: Signal, command: str):
        response = str()
        if command == "gamelist":
            response = json.dumps(self.games)
        return_signal.emit((response + "\n").encode("utf-8"))

    def finish_request(self, request: bytes, client_address: Tuple[str, int]) -> None:
        self.RequestHandlerClass(request, client_address, self, self.command)


if __name__ == "__main__":
    GSMServer()
