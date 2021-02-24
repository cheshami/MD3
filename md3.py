#!/usr/bin/env python3
"""
## An Audio MetaData Application.
## Author : R.Cheshami
## Company : Adak Free Way .. http://afw.ir
"""

import sys, os
import datetime
import logging
from pathlib import Path
import glob2
import meyed3

class MD3(object):
    """docstring for MD3"""
    def __init__(self, start_time, *args):
        super(MD3, self).__init__()

        self.args = self.get_args()

        clear = lambda: os.system('clear')
        clear()

        self.start_time = start_time
        print(u'Start Time:', start_time)

        if self.args.mfile:
            self.argMP3 = self.args.mfile
        else:
            self.argMP3 = 'donya.mp3'

        if self.args.path:
            self.path = self.args.path
        else:
            self.home = Path.home()
            self.path = str(self.home) + '/Music/md3/'

        self.mp3 = ''
        self.mp3SongsData = []
        self.oggs = ''
        self.oggSongsData = []

        self.cCSV = ''
        self.pf = ''
        self.recursive = False

        self.myMP3s = meyed3

        self.wellcome()

    def get_logger(self, msg='',cfname=None, name=None, level=logging.DEBUG, create_file=False):
            log = logging.getLogger(__name__)
            # get_logger('msg', 'MD3Logger', 'WARNING')
            if name is None:
                    name = inspect.stack()[1][1].split('.')[0]
            formatter = logging.Formatter(
                    "MD3 %(levelname)s Logging Message: %(asctime)s - %(process)d -  - %(threadName)s - %(name)s %(message)s")

            log = logging.StreamHandler()
            log.setLevel(level)
            log.setFormatter(formatter)
            if create_file:
                    # create file handler for logger.
                    fh = logging.FileHandler('md3.log')
                    fh.setLevel(level)
                    fh.setFormatter(formatter)
                    logging.root.addHandler(fh)
            logging.root.addHandler(log)
            return log

    def getch(self):
            """Gets a single character from standard input.
            Does not echo to the screen."""
            import termios
            import tty
            def _getch():
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    try:
                            tty.setraw(fd)
                            ch = sys.stdin.read(1)
                    finally:
                            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    return ch
            return _getch()

    def get_args(self):
        import argparse

        description = (
                            "Get and Set your Music MetaData in [CSV file].\n"
                            "You set a path with an argumant -p, then application\n"
                            "create a CSV file, with all MetaData Tags of all your Musics\n"
                            "you set for application [recursivly]."
            )
        parser = argparse.ArgumentParser(prog='md3.sh', description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('--path', '-p', required=False, help="if path+file writed: Display Metadata[s] of this file[s]\
	                        if just a path inserted Music path or directory. Default is user's Home Music Directory")
        parser.add_argument('--csvin', '-i', required=False, help="The Musics Metadata's CSV file to Update Musics Metadatas")
        parser.add_argument('--csvout', '-o', required=False, help="Name of Music Metadata CSV file.Default is md3.csv")
        parser.add_argument('--mfile', '-m', required=False, help="")
        parser.add_argument('--recursive', '-r', required=False, help="Recursive")

        return parser.parse_args()

    def wellcome(self):
        print(u'\n\t\u2554', end='')
        for i in range(25):
            print(u'\u2550', end='')
        print(u'\u2557\n\t\u2551', u' ## WellCome To MD3 ## ', u'\u2551\n\t\u255a', end='')
        for i in range(25):
            print(u'\u2550', end='')
        print(u'\u255d\n')
        self.main()

    def get_mp3s_files(self):
        print(self.recursive)
        if self.recursive == False:
            self.mp3s = glob2.glob(self.path + '*.mp3')
            print(self.mp3s)
        else:
            self.mp3s = glob2.glob(self.path + '**/*.mp3')
            print(self.mp3s)
        return self.mp3s

    def get_oggs_files(self):
        try:
            if os.path.exists(self.path):
                if self.answer == '2':
                    self.oggs = glob2.glob(self.path + '*.ogg')
                    print(mp3s)
                elif self.answer == '3':
                    self.oggs = glob2.glob(self.path + '**/*.ogg')
                    print(mp3s)
        except Exception:
            print(u'{} Not find.'.format(self.pf))
        return self.oggs

    def is_answer_corect(self):
        try:
            self.answer = int(raw_input('Enter a value (1..6). '))
        except ValueError:
            print('Invalid input. Enter a value from 1 till 6.')

        if not self.answer in range(1, 6):
            print('Invalid input. Enter a value between 1 - 4.')

        return self.answer

    def check_path(self):
        while True:
            try:
                if not(os.path.exists(self.path)):
                    print("Enter Valid Path or Filename : ", end="\r")
                    self.path = input('')
                else:
                    break;
            except IOError:
                print('Invalid path or Filename...', end="\r")
        return self.path
    """
    def menu(self):
        menu = {"1":(" - Get Tags of a Music",my_add_fn),
                "2":(" - Get Tags of a path Musics",my_quit_fn)
               }
        for key in sorted(menu.keys()):
             print(key+":" + menu[key][0])

        ans = raw_input("Make A Choice")
        menu.get(ans,[None,invalid])[1]()
    """

    def quit(self):
        print(u'\nBye.\n\nEnd Time: {}'.format(datetime.datetime.now()))
        print(u'Totlal Time in This Program: {}'.format(datetime.datetime.now()-self.start_time))
        exit(0)

    def main(self, *args):
        self.check_path()
        print("Your Default(Entered) path is {} ? (y/n) : ".format(self.path))
        self.pathisok = self.getch()
        if self.pathisok == 'n':
            self.check_path()

        print("What Do You Want To Do ?\n \
            \t1 - Get Tags of a Music\n \
            \t2 - Get Tags of a path Musics\n \
            \t3 - Get Tags of a path Musics Recursive\n \
            \t4 - Create CSV file\n \
            \t5 - Create CSV file for this path Recursive\n \
            \t6 - Save Musics Tag from a CSV file\n \
            \t7 - Quite")

        self.answer = self.getch()
        print(self.answer)

        if self.answer == '1':
            print("Tags of {} file? (y/n) : ".format(self.argMP3))

            self.mp3tag_answ = self.getch()
            if self.mp3tag_answ == 'n':
                self.argMP3 = ''
                self.argMP3 = input("Enter Your Music File Name : ")
            
            self.argMP3 = ''.join((self.path, self.argMP3))
            os.path.exists(self.argMP3)
            self.mp3SongData = meyed3.get_Tags(self.argMP3)
            meyed3.show_Tags_Column(self.mp3SongData)

        elif self.answer == '2' or self.answer == '3':
            self.SongsData = ''
            if self.answer == '3':
                self.recursive = True
            self.mp3s = self.get_mp3s_files()
            self.SongsData = meyed3.getMP3sTags(self.mp3s)
            for self.SongData in self.SongsData:
                ## Column Theme
                #meyed3.show_Tags_Column(self.SongData)
                ## Row Theme
                meyed3.show_Tags_Row(self.SongData)
                

        elif self.answer == '4' or self.answer == '5':
            if self.answer == '5':
                self.recursive = True
            self.csv_filename = 'md3.csv'
            print("The CSV File Name : {} ? (y/n) : ".format(self.csv_filename))
            self.CSV_answ = self.getch()
            if self.CSV_answ == 'n':
                self.csv_filename = input("Enter Your CSV File Name : ")
            self.pf = ''.join((self.path, self.csv_filename))
            self.mp3s = self.get_mp3s_files()
            self.SongsData = meyed3.getMP3sTags(self.mp3s)
            meyed3.saveCSVf(self.pf, self.SongsData)

        elif self.answer == '6':
            self.csv_filename = 'md3.csv'
            print("The CSV File Name : {} ? (y/n) : ".format(self.csv_filename))
            self.CSV_answ = self.getch()
            if self.CSV_answ == 'n':
                self.csv_filename = input("Enter Your CSV File Name : ")
            self.pf = ''.join((self.path, self.csv_filename))
            self.csvlist = meyed3.readCSVf(self.pf)
            print('Tags of all mp3 in {} was Read.'.format(self.path))
            self.csvlist = meyed3.correctPath(self.csvlist)
            self.mp3s = meyed3.splitCSVlist(self.csvlist)
            meyed3.saveTagsFromCSV(self.pf)

        elif self.answer == '7' or 'q':
            self.quit()
        self.quit()

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    mymd3=MD3(start_time, sys.argv)
    sys.exit(0)
