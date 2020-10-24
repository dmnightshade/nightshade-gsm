from socketserver import TCPServer, StreamRequestHandler


class Handler(StreamRequestHandler):

    games = {
        "game1": {
            "exec": "program1",
            "args": {
                "-a1": {
                    "default": 100,
                    "editable": False
                },
                "-a2": {
                    "default": 200
                }
            }
            },
        "game2": {
            "exec": "program2",
            "args": {
                "-a3": {
                    "default": 300
                }
            }
        }
    }

    def handle(self) -> None:
        pass


if __name__ == '__main__':
    with TCPServer(("127.0.0.1", 12345), Handler) as server:
        server.serve_forever()
