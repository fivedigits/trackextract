#!/usr/bin/python2

import re
import sys
from subprocess import call


def parseList(ls_file):

    t_expr = re.compile('\d\d:\d\d:\d\d')

    f = open(ls_file,"r")

    ls = f.readlines()

    f.close()

    timestamps = []

    names = []

    for line in ls:

        t_matches = t_expr.findall(line)

        n_matches = t_expr.split(line)

        if len(t_matches) == 1:

            timestamps.append(t_matches[0])
            
            names.append(n_matches[0].strip(" -,;.:"))

        else:

            print("too many matches")

    return {"time": timestamps, "name": names}

def extractTracks(beg_ls,name_ls,input_file,artist,album,genre):

    call(["ffmpeg","-i",input_file,input_file + ".wav"])

    if len(name_ls) != len(beg_ls):

        print("number of tracks not well defined")

        return -1

    end_ls = ["=" + stamp for stamp in beg_ls[1:]] + ['-00:00:00']


    for index in range(len(beg_ls)):

        print("Extracting: " + names[index])

        call(["sox",input_file + ".wav",names[index] + ".wav","trim",beg_ls[index],end_ls[index]])

    for index in range(len(names)):

        call(["ffmpeg","-i",names[index] + ".wav","-q","6", names[index] + ".ogg"])

        call(["normalize-ogg",names[index] + ".ogg"])

        call(["id3tag","--artist",artist,"--album",album,"--song",names[index],"--track",str(index+1),"--total",str(len(names)),"--genre",genre,names[index]+ ".ogg"])

    call(["rm","*.wav"])

if __name__ == "__main__":

    input_file = sys.argv[1]

    ls_file = sys.argv[2]

    artist = sys.argv[3]

    album = sys.argv[4]
    
    genre = sys.argv[5]

    metadata = parseList(ls_file)

    beg_times = metadata["time"]

    names = metadata["name"]

    extractTracks(beg_times, names,input_file,artist,album,genre)
