import multiprocessing as mp
from queue import Empty
from typing import Dict, List
import time
from onvifcamera import Camera
import devicemgmt

class CameraManager:
    def __init__(self):
        self.cameras: Dict[str, mp.Process] = {}
        self.status_queue = mp.Queue()
        self.command_queues: Dict[str, mp.Queue] = {}

    def add_camera(self, ip: str, port: str, user: str, password: str):
        if ip in self.cameras:
            return False
        
        command_queue = mp.Queue()
        self.command_queues[ip] = command_queue
        
        process = mp.Process(
            target=self._camera_process,
            args=(ip, port, user, password, command_queue, self.status_queue)
        )
        self.cameras[ip] = process
        process.start()
        return True

    def _camera_process(self, ip: str, port: str, user: str, password: str, 
                       command_queue: mp.Queue, status_queue: mp.Queue):
        camera = Camera(ip=ip, port=port, user=user, password=password)
        
        while True:
            try:
                # Check for commands
                try:
                    cmd = command_queue.get_nowait()
                    if cmd == "stop":
                        break
                except Empty:
                    pass

                # Connect and get camera info
                cam_connection = camera.connect()
                if cam_connection:
                    hostname = devicemgmt.gethostName(cam_connection)
                    datetime = devicemgmt.getDateTime(cam_connection)
                    
                    status = {
                        'ip': ip,
                        'hostname': hostname,
                        'datetime': datetime,
                        'status': 'connected'
                    }
                else:
                    status = {
                        'ip': ip,
                        'status': 'disconnected',
                        'error': camera.last_error
                    }

                status_queue.put(status)
                time.sleep(5)  # Update interval

            except Exception as e:
                status_queue.put({
                    'ip': ip,
                    'status': 'error',
                    'error': str(e)
                })
                time.sleep(5)

    def stop_all(self):
        for ip, queue in self.command_queues.items():
            queue.put("stop")
        
        for process in self.cameras.values():
            process.join(timeout=5)
            if process.is_alive():
                process.terminate()

    def get_status(self) -> List[dict]:
        statuses = []
        while not self.status_queue.empty():
            statuses.append(self.status_queue.get())
        return statuses
