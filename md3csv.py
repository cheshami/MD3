#!/usr/bin/env python3

import sys, os, time
import logging
import 

def userHome():
	from pathlib import Path
	return str(Path.home())

def get_args():
    import argparse

    description = (
                    "Get and Set your Music MetaData [with CSV file].\n"
                    "You set a path with an argumant -d, then application\n"
                    "create a CSV file, with all MetaData Tags of all Music files\n"
                    "you set for application [recursivly]."
    )
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--path', metavar='path', type=str, help='path or directory to Music[s](Audio[s]) files.')
    parser.add_argument('-c', '--csv', metavar='csv', required=False, help='Name of CSV file.Default is md3.csv')
    parser.add_argument('-r', '--recursive', metavar='recursive', required=False, help='all files in directory and subdirectory. Recursivly.')
    return parser.parse_args()


def getAudiosTags(self, Fs):
	self.__tags = []

	if type(Fs) == list:
	    for self.__F in Fs:
	        self.__tags.append(self.showOGGTags(self.__F))
	else:
	    self.__tags.append(self.showOGGTags(self.__Fs))
	return self.__tags

def showAudioTags(self, OGGF):
        from tinytag import TinyTag

        self.__tag = TinyTag.get(F)

        print('This track is by {}.'.format(self.__tag.artist))
        print('Track title : {}'.format(self.__tag.title))
        print('It is {:04.2f} seconds long.'.format(self.__tag.duration))
        print(self.__tag.albumartist)
        print(self.__tag.audio_offset)
        print(self.__tag.bitrate)
        print(self.__tag.comment)
        print(self.__tag.composer)
        print(self.__tag.track)
        print(self.__tag.track_total)
        print(self.__tag.year)
        print(self.__tag.disc)
        print(self.__tag.disc_total)
        print(self.__tag.duration/60)
        print('{:02.2f} MiB'.format(self.__tag.filesize/1024/1024))
        print(self.__tag.genre)
        print(self.__tag.samplerate)
        return self.__tag

def main(argv):

	args = get_args()
    
    path = args.path if args.path else ''.join((userHome(), '/Music/md3/'))
    csv_filename = args.csv if args.csv else 'md3.csv'
    recursive = True if args.recursive else False


if __name__ == '__main__':
    sys.exit(main(sys.argv))