# Extension by Fistbobr

from krita import Extension
from .presence import Presence
import threading
import time
from PyQt5.QtCore import QObject, pyqtSignal

EXTENSION_ID = 'pykrita_discord_rpc'

client_id = '744403269237080127' #'541005130749968405'  # App ID. Change if you want

RPC = Presence(client_id)  # Initialize the client class
RPC.connect() # Start the handshake loop

# The status thread 
class DiscordStatusThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
      self.updatedStatus = False
      self.loopping = True
      self.singleOpen = 0
   def run(self):
      while self.loopping:
        try:
            # Closing this thread
            if(Krita.instance().activeWindow() == None):
                if(self.singleOpen >= 1):
                    self.loopping = False

                if(self.singleOpen == 0):
                    self.singleOpen = 1

            # Detecting new document
            if(Krita.instance().activeDocument() != None):
                if(self.updatedStatus == False):
                    RPC.update(details="Working on", state=str(Krita.instance().activeDocument().name()), large_image="krita_logo", start=int(time.time()))
                    self.updatedStatus = True
            else:
                RPC.update(details="Not currently drawing", large_image="krita_logo")
                self.updatedStatus = False
            time.sleep(5)
        except:
            self.loopping = False

# Class of extension
class DiscordRpc(Extension):
    def __init__(self, parent):
        RPC.update(details="Not currently drawing", large_image="krita_logo")
        super().__init__(parent)

    def setup(self):
        DiscThread = DiscordStatusThread()
        DiscThread.start()

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

