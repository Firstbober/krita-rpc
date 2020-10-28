# Extension by Fistbobr

from krita import Extension
from .presence import Presence
import time
import PyQt5.QtCore

DISCORD_RPC_CLIENT_ID = '744403269237080127'  # '541005130749968405'  # App ID. Change if you want
EXTENSION_ID = 'pykrita_discord_rpc'


RPC = Presence(DISCORD_RPC_CLIENT_ID)  # Initialize the client class

class DiscordRpc(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.file = ""
        self.timer = PyQt5.QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_rpc)

    def setup(self):
        RPC.connect()  # Start the handshake loop
        self.timer.start()

    def update_rpc(self):
        # Detecting new document
        if Krita.instance().activeDocument() is not None:
            if self.file != Krita.instance().activeDocument().fileName():
                RPC.update(details="Draws something cool",
                           state=str(Krita.instance().activeDocument().name()) or "No name",
                           large_image="krita_logo", start=int(time.time()))
                self.file = Krita.instance().activeDocument().fileName()
        else:
            RPC.update(details="Idle", large_image="krita_logo")
            self.file = ""

    # This is C methods so can't rename
    # noinspection PyPep8Naming
    def createActions(self, window):
        pass

    # noinspection PyPep8Naming
    def windowClosed(self):
        self.timer.stop()
        pass

    def action_triggered(self):
        pass


# And add the extension to Krita's list of extensions:
app = Krita.instance()
extension = DiscordRpc(parent=app)
app.addExtension(extension)
