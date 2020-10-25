import json
from typing import Dict

from qtpy.QtCore import *
from qtpy.QtNetwork import QTcpSocket
from qtpy.QtWidgets import *


class Client(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        self.socket = QTcpSocket(self)

        #### Set central widget, which is what is shown on the GUI ####
        main_widget = QWidget(self)
        self.layout = QStackedLayout(main_widget)
        self.setCentralWidget(main_widget)

        #### Not connected page ####
        not_connected = QPushButton(text="Connect to server", parent=main_widget)
        not_connected.clicked.connect(self.connect_to_server)
        self.layout.addWidget(not_connected)
        self.socket.disconnected.connect(lambda: self.change_page(0))

        #### Connected page ####
        connected = QWidget(parent=main_widget)
        c_layout = QVBoxLayout(connected)
        self.layout.addWidget(connected)
        self.socket.connected.connect(self.populate_game_list)

        # Disconnect button #
        disconnect_button = QPushButton(text="Disconnect from server", parent=connected)
        disconnect_button.clicked.connect(self.disconnect_from_server)
        disconnect_button.setMaximumHeight(30)
        c_layout.addWidget(disconnect_button)

        # Game selection area #
        self.game_area = QHBoxLayout(connected)
        c_layout.addLayout(self.game_area)

        # Lists available game server to create
        self.game_list = None

        # Holds the server creations dialogs
        # This is set by self.populate_game_list()
        self.game_creation = None

    def change_page(self, page_num: int) -> None:
        self.layout.setCurrentIndex(page_num)

    def connect_to_server(self) -> None:
        self.socket.connectToHost("127.0.0.1", 12345)

    def disconnect_from_server(self) -> None:
        self.socket.disconnectFromHost()

    def fetch_game_list(self) -> Dict:
        cmd = QByteArray("gamelist\n".encode(encoding="utf-8"))
        self.socket.write(cmd)
        self.socket.waitForReadyRead(msecs=3000)
        game_list = str(self.socket.readLine(), encoding="utf-8")
        game_list = json.loads(game_list)
        return game_list

    def populate_game_list(self) -> None:
        # Ask server for game list
        gl = self.fetch_game_list()

        # Remove previous game list
        if self.game_list is not None:
            self.game_list.setParent(None)
            self.game_list.hide()
            self.game_area.layout().removeWidget(self.game_list)
            self.game_list = None

        # Remove any previous creation area
        if self.game_creation is not None:
            self.game_creation.setParent(None)
            self.game_creation.hide()
            self.game_area.layout().removeWidget(self.game_creation)
            self.game_creation = None

        # Create new game list
        self.game_list = QListWidget()
        self.game_list.setMaximumWidth(200)
        self.game_area.addWidget(self.game_list)

        # Create new game creation area
        self.game_creation = QWidget()
        c_layout = QStackedLayout(self.game_creation)
        self.game_area.addWidget(self.game_creation)

        # Now add the games in the game list
        for name in sorted(gl.keys()):
            self.game_list.addItem(name)
            info = gl[name]
            form_w = QWidget(self.game_creation)

            form = QFormLayout(form_w)
            field = QTextEdit(info["exec"], form_w)
            field.setEnabled(False)
            form.addRow("Program:", field)
            for arg_name, arg_info in info["args"].items():
                field = QTextEdit(str(arg_info["default"]), form_w)
                if "editable" in arg_info:
                    field.setEnabled(arg_info["editable"])
                else:
                    field.setEnabled(True)
                form.addRow(arg_name, field)
            c_layout.addWidget(form_w)

        # Set starting selection
        self.game_list.setCurrentRow(0)
        c_layout.setCurrentIndex(0)

        # Creation area changes with game list selections
        self.game_list.currentRowChanged.connect(c_layout.setCurrentIndex)

        # Show game list page
        self.change_page(1)


if __name__ == "__main__":
    # Start client
    app = QApplication([])
    client = Client()
    client.show()
    app.exec_()
