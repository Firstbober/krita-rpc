# Extension by Fistbobr

from krita import Extension, Krita
from .presence import Presence
import time
import asyncio

try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

try:
    from PyQt6.QtCore import QTimer
except ImportError:
    from PyQt5.QtCore import QTimer

DISCORD_RPC_CLIENT_ID = '744403269237080127'  # '541005130749968405'  # App ID. Change if you want
EXTENSION_ID = 'pykrita_discord_rpc'
RECONNECT_INTERVAL = 30  # Try to reconnect every 30 seconds if offline

RPC = Presence(DISCORD_RPC_CLIENT_ID)  # Initialize the client class

class DiscordRpc(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.file = None
        self.time = 0
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_rpc)
        
        self.reconnect_timer = QTimer(self)
        self.reconnect_timer.setInterval(RECONNECT_INTERVAL * 1000)
        self.reconnect_timer.timeout.connect(self.try_reconnect)

        self.version = f"Krita {str(Krita.instance().version())}"

    def setup(self):
        RPC.connect()
        self.timer.start()
        self.reconnect_timer.start()
    
    def try_reconnect(self):
        if not RPC.connected:
            print('Retrying connection...')
            RPC.reconnect()

    def update_rpc(self):
        # Detecting new document
        try:
            doc = Krita.instance().activeDocument()

            if doc is not None:
                if self.time == 0:
                    self.time = time.time()

                filename = doc.fileName() or ""

                if self.file != filename:
                    RPC.update(
                        details="Drawing something cool!",
                        state=str(doc.name()) or "Unnamed",
                        large_image="krita_logo",
                        start=int(self.time),
                        large_text=self.version
                    )

                    self.file = filename

            else:
                RPC.update(
                    details="Idle",
                    large_image="krita_logo",
                    large_text=self.version
                )
                self.file = None
                self.time = 0
        except Exception as e:
            print("RPC update error:", e)

    # noinspection PyPep8Naming
    def createActions(self, window):
        pass
            
    # noinspection PyPep8Naming
    def windowClosed(self):
        self.timer.stop()
        self.reconnect_timer.stop()
        pass


# And add the extension to Krita's list of extensions:
app = Krita.instance()
extension = DiscordRpc(parent=app)
app.addExtension(extension)
