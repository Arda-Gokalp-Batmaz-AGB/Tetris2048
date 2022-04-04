import os
class Sound:
    soundType = None
    def __init__(self, soundtype : str):
        self.soundType = soundtype

    def CallSound(self):
        os.system("mpg123 " + self.soundType)
