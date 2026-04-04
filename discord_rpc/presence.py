import os
import threading
from typing import Optional

from .baseclient import BaseClient
from .payloads import Payload
from .utils import remove_none, get_event_loop
from .exceptions import PyPresenceException


class Presence(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connected = False
        self._connection_thread: Optional[threading.Thread] = None

    def update(self, pid: int = os.getpid(),
               state: str = None, details: str = None,
               start: int = None, end: int = None,
               large_image: str = None, large_text: str = None,
               small_image: str = None, small_text: str = None,
               party_id: str = None, party_size: list = None,
               join: str = None, spectate: str = None,
               match: str = None, buttons: list = None,
               instance: bool = True,
               _donotuse=True):

        if not self.connected:
            return None  # Silently skip update if not connected, maybe add a warning? idk
        
        try:
            if _donotuse is True:
                payload = Payload.set_activity(pid=pid, state=state, details=details, start=start, end=end,
                                               large_image=large_image, large_text=large_text,
                                               small_image=small_image, small_text=small_text, party_id=party_id,
                                               party_size=party_size, join=join, spectate=spectate,
                                               match=match, buttons=buttons, instance=instance, activity=True)

            else:
                payload = _donotuse
            self.send_data(1, payload)
            return self.loop.run_until_complete(self.read_output())
        except Exception as e:
            print(f'Update failed: {e}')
            self.connected = False
            return None

    def clear(self, pid: int = os.getpid()):
        if not self.connected:
            return None
        
        try:
            payload = Payload.set_activity(pid, activity=None)
            self.send_data(1, payload)
            return self.loop.run_until_complete(self.read_output())
        except Exception as e:
            print(f'Clear failed: {e}')
            self.connected = False
            return None

    def connect(self, timeout=5):
        def _connect():
            try:
                self.update_event_loop(get_event_loop())
                self.loop.run_until_complete(self.handshake(timeout=timeout))
                self.connected = True
                print('Connected to Discord')
            except PyPresenceException as e:
                print(f'Connection failed: {e}')
                self.connected = False
            except Exception as e:
                print(f'Unexpected connection error: {e}')
                self.connected = False
        
        # Run connection in a separate thread to avoid blocking
        self._connection_thread = threading.Thread(target=_connect, daemon=True)
        self._connection_thread.start()
    
    def reconnect(self, timeout=5):
        print('Attempting to reconnect to Discord...')
        self.connect(timeout=timeout)

    def close(self):
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self.loop.close()


class AioPresence(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, isasync=True)

    async def update(self, pid: int = os.getpid(),
                     state: str = None, details: str = None,
                     start: int = None, end: int = None,
                     large_image: str = None, large_text: str = None,
                     small_image: str = None, small_text: str = None,
                     party_id: str = None, party_size: list = None,
                     join: str = None, spectate: str = None,
                     match: str = None, buttons: list = None,
                     instance: bool = True):
        payload = Payload.set_activity(pid=pid, state=state, details=details, start=start, end=end,
                                       large_image=large_image, large_text=large_text,
                                       small_image=small_image, small_text=small_text, party_id=party_id,
                                       party_size=party_size, join=join, spectate=spectate,
                                       match=match, buttons=buttons, instance=instance, activity=True)
        self.send_data(1, payload)
        return await self.read_output()

    async def clear(self, pid: int = os.getpid()):
        payload = Payload.set_activity(pid, activity=None)
        self.send_data(1, payload)
        return await self.read_output()

    async def connect(self):
        self.update_event_loop(get_event_loop())
        await self.handshake()

    def close(self):
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self.loop.close()
