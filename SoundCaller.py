from lib.playsound import playsound
import threading
from time       import sleep


class SoundGlobal():
    global allow_sound

class SoundCaller:
    path : str
    duration : float
    def __init__(self,path):
        self.path = path
        if(SoundGlobal().allow_sound == True):
            self.CreateSoundThread()


    def CreateSoundThread(self):
        path = self.path
        sound_thread = threading.Thread(target=self.SoundThread,args=(path, ))
        sound_thread.start()

    def SoundThread(self,path):
        self.duration=playsound(f'{path}',False)
        if(self.duration==0):
            print("Sound duration is not supported in this system!")

