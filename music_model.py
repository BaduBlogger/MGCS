import tensorflow as tf
import librosa
from mp3towav import convert_to_wav
import sys
import shutil, os
import os.path
from os import path
import sys


def run_model(song_path = str(os.getcwd()+"Songs/Immigrant.mp3"), path_dest = str(os.getcwd())):
    ###########################################################################
    just_path = os.getcwd()+"/Just_Path/"
    # song_path = sys.argv[1]
    x1 = song_path.replace("\\", ".")
    # print(x1)
    x1 = x1.split(".")
    song_name = x1[-2]
    sn=song_name.split('/')[-1]
    print(sn)

    ##########################################################################

    #Constants which depend on the model. If you train the model with different values,
    #need to change those values here too
    num_mfcc = 13
    n_fft=2048
    hop_length = 512
    sample_rate = 22050
    samples_per_track = sample_rate * 30
    num_segment = 10
    ############################################################################

    model = tf.keras.models.load_model(os.getcwd()+"/cnn_model.h5")
    # model.summary()
    
    classes = ["Blues","Classical","Country","Disco","Hiphop",
                "Jazz","Metal","Pop","Reggae","Rock"]

    class_predictions = []

    samples_per_segment = int(samples_per_track / num_segment)
    parts = None

    if song_path.endswith('.mp3'):
        path_to_save = just_path + sn+".wav"
        convert_to_wav(song_path,path_to_save)
        song_path1 = path_to_save
    else:
        song_path1 = song_path

    #load the song
    x, sr = librosa.load(song_path1, sr = sample_rate)
    song_length = int(librosa.get_duration(filename=song_path1))

    prediction_per_part = []
    flag = 0
    if song_length > 30:
        print("Song is greater than 30 seconds")
        samples_per_track_30 = sample_rate * song_length
        parts = int(song_length/30)
        samples_per_segment_30 = int(samples_per_track_30 / (parts))
        flag = 1
        print("Song sliced into "+str(parts)+" parts")
    elif song_length == 30:
        parts = 1
        flag = 0
    else:
        print("Too short, enter a song of length minimum 30 seconds")
        parts = 0
        flag = 2

    for i in range(0,parts):
        if flag == 1:
            print("Song snippet ",i+1)
            start30 = samples_per_segment_30 * i
            finish30 = start30 + samples_per_segment_30
            y = x[start30:finish30]
            #print(len(y))
        elif flag == 0:
            print("Song is 30 seconds, no slicing")
            y = x

        for n in range(num_segment):
            start = samples_per_segment * n
            finish = start + samples_per_segment
            #print(len(y[start:finish]))
            mfcc = librosa.feature.mfcc(y[start:finish], sample_rate, n_mfcc = num_mfcc, n_fft = n_fft, hop_length = hop_length)
            mfcc = mfcc.T
            #print(mfcc.shape)
            mfcc = mfcc.reshape(1, mfcc.shape[0], mfcc.shape[1],1)
            #print(mfcc.shape)
            
            array = model.predict(mfcc)*100
            array = array.tolist()

            #find maximum percentage class predicted
            class_predictions.append(array[0].index(max(array[0])))

        occurence_dict = {}
        for i in class_predictions:
            if i not in occurence_dict:
                occurence_dict[i] = 1
            else:
                occurence_dict[i] +=1

        max_key = max(occurence_dict, key=occurence_dict.get)
        prediction_per_part.append(classes[max_key])

    #print("prediction_per_part",prediction_per_part)
    if len(prediction_per_part)>0:
        prediction = max(set(prediction_per_part), key = prediction_per_part.count)
        print(prediction)
        prediction = str(prediction)

        parent_dir = path_dest
        
        #Create respective genre folder's path
        pathOfFolder = os.path.join(parent_dir, prediction)
        print(pathOfFolder)
            
        #Check if respective genre folder already exists
        #if exists then only move file else create folder and move file
        if(os.path.exists(pathOfFolder)):        
            shutil.move(song_path, pathOfFolder)  
        else:
            os.mkdir(pathOfFolder)  
            shutil.move(song_path, pathOfFolder)
        return True, prediction
    else:
        return False, None

if __name__=="__main__":
    # run_model(song_path = str("C:\p2\you_belong_with_me.wav"), path_dest = str("F:\MGC"))     
    pass
