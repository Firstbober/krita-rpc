# Extension by Fistbobr

from krita import Extension
from .presence import Presence
import threading
import traceback
import time
from PyQt5.QtCore import QObject, pyqtSignal

EXTENSION_ID = 'pykrita_discord_rpc'

client_id = '744403269237080127' #'541005130749968405'  # App ID. Change if you want

RPC = Presence(client_id)  # Initialize the client class
RPC.connect() # Start the handshake loop

# The status thread 
class DiscordStatusThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self, name="DRP Plugin Thread")
      self.singleOpen = 0
      self.file = ""
   def run(self):
      while True:
        try:
            # Closing this thread
            if(Krita.instance().activeWindow() == None):
                if(self.singleOpen >= 1):
                    break

                if(self.singleOpen == 0):
                    self.singleOpen = 1

            # Detecting new document
            if(Krita.instance().activeDocument() != None):
                if(self.file != Krita.instance().activeDocument().fileName()):
                    RPC.update(details="Draws something cool", state=str(Krita.instance().activeDocument().name()) or "No name", large_image="krita_logo", start=int(time.time()))
                    self.file = Krita.instance().activeDocument().fileName()
            else:
                RPC.update(details="Idle", large_image="krita_logo")
                self.file = ""
            time.sleep(5)
        except Exception as e:
            # Хз как вывести эксепшн нормально
            # with open("C:\\Users\\panko\\Desktop\\log.txt", "a") as f:
            #    f.write(traceback.format_exc())
            # RPC.update(details="An exception occured", state=type(e).__name__ + ": " + str(e), large_image="krita_logo")
            # self.file = ""
            # time.sleep(5)
            pass


# Class of extension
class DiscordRpc(Extension):
    def __init__(self, parent):
        RPC.update(details="Idle", large_image="krita_logo")
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

