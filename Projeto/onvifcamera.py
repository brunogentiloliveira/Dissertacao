from onvif import ONVIFCamera
from datetime import datetime

class Camera:
    def __init__(self, ip, port, user, password):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.connected = False
        self.last_error = None
    
    def connect(self):
        try:
            mycam = ONVIFCamera(self.ip, self.port, self.user, self.password)
            self.connected = True
            self.last_error = None
            return mycam
        except Exception as e:
            self.connected = False
            self.last_error = str(e)
            return None

    def get_status(self):
        return {
            'ip': self.ip,
            'connected': self.connected,
            'last_error': self.last_error,
            'last_check': datetime.now().isoformat()
        }
