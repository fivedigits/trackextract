#!/usr/bin/python2

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

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

            print("Could not find timestamp in line:" + line)

    return {"time": timestamps, "name": names}

def extractTracks(beg_ls,name_ls,args):

    input_file = args.infile

    artist = args.artist

    album = args.album

    genre = args.genre

    # print("Converting infile to ogg.")

    # call(["ffmpeg","-loglevel","quiet","-i",input_file,"-q","9",input_file + ".ogg"])

    if len(name_ls) != len(beg_ls):

        print("number of tracks not well defined")

        return -1

    end_ls = ["=" + stamp for stamp in beg_ls[1:]] + ['-00:00:00']


    for index in range(len(beg_ls)):

        print("Extracting: " + names[index])

        call(["sox",input_file,"-C","6","--norm=-9",names[index] + ".ogg","trim",beg_ls[index],end_ls[index]])

    for index in range(len(names)):

        call(["vorbiscomment","-t","ARTIST=" + artist,"-t","ALBUM=" + album,"-t","TITLE=" + names[index],"-t","TRACKNUMBER=" + str(index+1),"-t","TRACKTOTAL=" + str(len(names)),"-t","GENRE=" + genre,"-w",names[index]+ ".ogg"])

        call(["vorbiscomment","-l",names[index] + ".ogg"])

    call(["rm",input_file])

    call(["vorbisgain","-a","*.ogg"])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Split a single audio file into multiple based on a list in a text file.')

    parser.add_argument('infile',help="audio file to split")
    parser.add_argument('listfile',help="list of tracks with timestamps [hh:m]m:ss, one per line")
    parser.add_argument('-A',"--artist",default="Unknown Artist",help="Artist")
    parser.add_argument('-a',"--album",default="Unknown Album",help="Album")
    parser.add_argument('-g',"--genre",default="Unknown Genre",help="Genre")

    args = parser.parse_args()

    ls_file = args.listfile

    metadata = parseList(ls_file)

    beg_times = metadata["time"]

    names = metadata["name"]

    extractTracks(beg_times, names,args)
