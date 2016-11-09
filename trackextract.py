#!/usr/bin/python2

import re
import sys
from subprocess import call
import argparse


def parseList(ls_file):

    t_expr = re.compile('\d{0,2}\:?\d{1,2}:\d\d')

    alpha = re.compile('[\w\s]+')

    f = open(ls_file,"r")

    ls = f.readlines()

    f.close()

    timestamps = []

    names = []

    for line in ls:

        t_matches = t_expr.findall(line)

        rest = ''.join(t_expr.split(line))

        name = ''.join(alpha.findall(rest))

        if len(t_matches) == 1:

            timestamps.append(t_matches[0])
            
            names.append(name.strip(" -,;.:\r\n"))

        else:

            print("too many matches")

    return {"time": timestamps, "name": names}

def extractTracks(beg_ls,name_ls,args):

    input_file = args.infile

    artist = args.artist

    album = args.album

    genre = args.genre

    print("Converting infile to ogg.")

    call(["ffmpeg","-loglevel","quiet","-i",input_file,"-q","9",input_file + ".ogg"])

    if len(name_ls) != len(beg_ls):

        print("number of tracks not well defined")

        return -1

    end_ls = ["=" + stamp for stamp in beg_ls[1:]] + ['-00:00:00']


    for index in range(len(beg_ls)):

        print("Extracting: " + names[index])

        call(["sox",input_file + ".ogg","-C","6",names[index] + ".ogg","trim",beg_ls[index],end_ls[index]])

    for index in range(len(names)):

        call(["normalize-ogg",names[index] + ".ogg"])

        call(["id3tag","--artist",artist,"--album",album,"--song",names[index],"--track",str(index+1),"--total",str(len(names)),"--genre",genre,names[index]+ ".ogg"])

    call(["rm",input_file + ".ogg"])

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Split a single audio file into multiple based on a list in a text file.')

    parser.add_argument('infile',help="audio file to split")
    parser.add_argument('listfile',help="list of tracks with timestamps [dd:h]h:mm, one per line")
    parser.add_argument('-A',"--artist",default="Unknown Artist",help="Artist")
    parser.add_argument('-a',"--album",default="Unknown Album",help="Album")
    parser.add_argument('-g',"--genre",default="Unknown Genre",help="Genre")

    args = parser.parse_args()

    ls_file = args.listfile

    metadata = parseList(ls_file)

    beg_times = metadata["time"]

    names = metadata["name"]

    extractTracks(beg_times, names,args)
