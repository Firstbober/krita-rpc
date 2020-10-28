# Extension by Fistbobr

from krita import Extension
from .presence import Presence
import time
from PyQt5.QtCore import QTimer

EXTENSION_ID = 'pykrita_discord_rpc'

client_id = '744403269237080127'  # '541005130749968405'  # App ID. Change if you want

RPC = Presence(client_id)  # Initialize the client class
RPC.connect()  # Start the handshake loop
file = ""


def update_rpc():
    global file
    # Detecting new document
    if Krita.instance().activeDocument() is not None:
        if file != Krita.instance().activeDocument().fileName():
            RPC.update(details="Draws something cool",
                       state=str(Krita.instance().activeDocument().name()) or "No name",
                       large_image="krita_logo", start=int(time.time()))
            file = Krita.instance().activeDocument().fileName()
    else:
        RPC.update(details="Idle", large_image="krita_logo")
        file = ""

# Class of extension
class DiscordRpc(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.file = ""
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(update_rpc)

    def setup(self):
        self.timer.start()

    def createActions(self, window):
        pass

    def windowClosed(self):
        print("Closed")

    def action_triggered(self):
        pass


# And add the extension to Krita's list of extensions:
app = Krita.instance()
extension = DiscordRpc(parent=app)
app.addExtension(extension)
