from os import path
from pydub import AudioSegment

def convert_to_wav(src,dst):
    # convert wav to mp3
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")

def mp3_to_wav(src):
    # convert wav to mp3
    dst = src.split(".")[0]+'.wav'
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
    return dst

if __name__ == "__main__":
    pass
else:
    path = '/home/dell/Desktop/MGCS/MGC_Final/Songs'
    file = 'Is She With You.mp3'
    mp3_to_wav(path+'/'+file)
