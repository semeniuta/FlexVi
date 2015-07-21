from enum import Enum
from gi.repository import Aravis as ar
import aravis as pyar

class AravisGrabber:

    States = Enum('States', 'not_initialized not_functional initialized camera_selected')
    currtent_state = States.not_initialized
    current_camera = None

    def __init__(self):
            
        ''' Get device IDs and initialize Camera objects '''
        ar.update_device_list()
        self.device_ids = pyar.get_device_ids()
        self.cameras = {i: pyar.Camera(i) for i in self.device_ids}
        
    def select_camera_by_id(self, camera_id):
        if camera_id not in self.device_ids:
            raise Exception('Incorrect device id provided')
        self.current_camera = self.cameras[camera_id]
        self.current_state = self.States.camera_selected
        
    def select_camera_by_index(self, idx):
        if idx < 0 or idx > len(self.device_ids):
            raise Exception('Incorrect device index provided')
        self.current_camera = self.cameras[self.device_ids[idx]]
        self.current_state = self.States.camera_selected
        
    def grab_image(self):
        print 'Grabbing...'
        if self.current_state is not self.States.camera_selected:
            raise Exception('No camera has been selected')
        im = pyar.get_frame(self.current_camera)
        return im
            
        
