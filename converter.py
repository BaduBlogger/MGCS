import os,subprocess
def mp3_to_ogg(file,root_):
    path = ''
    if os.path.splitext(file)[1] == '.mp3':
        filename = os.path.splitext(file)[0]
        # os.system("ffmpeg -i '{}.mp3' '{}.ogg'".format(filename,filename))   
        cmd = "ffmpeg -i {}.mp3 {}.ogg".format(filename,filename)
        #s = subprocess.check_call(cmd, stdin=None, stderr=None,shell = True)
        os.system(cmd)
        
        path = (root_ + '/' + filename+'.ogg').replace('\\','/')
        print(path)
    else:
        path = (root_ + '/' + file).replace('\\','/')
    return path

mp3_to_ogg('Immigrant.mp3','/home/dell/Desktop/MGCS/MGC_Final/Songs')