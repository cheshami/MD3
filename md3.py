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
import eyed3
import glob2

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

def getch():
    """Gets a single character from standard input.
    Does not echo to the screen."""
    import termios
    import sys, tty
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

class MMutagen3:
    def __init__(self):
        print('MMutagen3__init__ Func ...')
        self.__df = ''

    def getIMG(self, audiofile):
        IMGS = audiofile.tag.images
        for IMG in IMGS:
            if IMG.picture_type == 3:
                return IMG.image_data

    def no_padding(self, info):
        # this will remove all padding
        return 0

    def default_implementation(self, info):
        # this is the default implementation, which can be extended
        return info.get_default_padding()

    def no_new_padding(self, info):
        # this will use existing padding but never add new one
        return max(info.padding, 0)

    def padd(self, audiofile):
        from mutagen.mp3 import MP3

        f = MP3("somefile.mp3")
        f.save(padding=no_padding)
        #f.save(padding=default_implementation)
        #f.save(padding=no_new_padding)

    def embed_album_art(self, cover_filepath, audio_filepaths):
        import mutagen
        """ Embed album art into audio files. """
        with open(cover_filepath, "rb") as f:
            cover_data = f.read()
        #for filepath in audio_filepaths:
        mf = mutagen.File(audio_filepaths)
        if (isinstance(mf.tags, mutagen._vorbis.VComment) or isinstance(mf, mutagen.ogg.oggFileType)):
            picture = mutagen.flac.Picture()
            picture.data = cover_data
            picture.type = mutagen.id3.PictureType.COVER_FRONT
            picture.mime = "image/jpeg"
            encoded_data = base64.b64encode(picture.write())
            mf["metadata_block_picture"] = encoded_data.decode("ascii")
        elif (isinstance(mf.tags, mutagen.id3.ID3) or
              isinstance(mf, mutagen.id3.ID3FileType)):
            mf.tags.add(mutagen.id3.APIC(mime="image/jpeg",
                                       type=mutagen.id3.PictureType.COVER_FRONT,
                                       data=cover_data))
            logging.warning('The album art was Changed')
        elif (isinstance(mf.tags, mutagen.mp4.MP4Tags) or
              isinstance(mf, mutagen.mp4.MP4)):
            mf["covr"] = [mutagen.mp4.MP4Cover(cover_data,
                                             imageformat=mutagen.mp4.AtomDataType.JPEG)]
        mf.save()

    def get_album_art(self, file, pic):
        fn = file.path()
        directory = os.path.dirname(path)
        for cover in ['cover.jpg', 'cover.png']:
            coverfilename = os.path.join(directory, fn, cover)
            if os.path.exists(coverfilename):
                return coverfilename

        try:
            metadata = fn.metadata
        except AttributeError:
            try:
                metadata = mutagen.File(path)
            except mutagen.mp3.HeaderNotFoundError as e:
                print(u"Error reading %s:" % path, e)
                return None

        try:
            image = extractFrontCover(metadata)
        except OSError:
            print(u'Error extracting image from %s' % path)
            return None

        return image 

    def mutgReadTags(self, audiofile):
        from mutagen.easyid3 import EasyID3
        from mutagen.id3 import ID3
        for f in audiofile:
            audiofile = EasyID3(f)
            print(f)
            print(audiofile['title'], audiofile['artist'])
            print(audiofile.items())

            audio = ID3(f)

            print(u"Artist: %s" % audio['TPE1'].text[0])
            print(u"Track: %s" % audio["TIT2"].text[0])
            #print(u"Release Year: %s" % audio["TDRC"].text[0])
            print(u'-------------------------------------------')

    def mutgAddImage(self, f, image):
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, APIC, error

        audio = MP3(f, ID3=ID3)

        # add ID3 tag if it dosen't exist
        try:
            audio.add_tags()
        except error:
            pass

        audio.tags.add(
            APIC(
                encoding=3,
                mime='image/png',
                type=3,
                desc=u'Cover',
                data=open(image).read()
            )
        )
        audio.save()

class MTinyTag3:
    '''for ogg files and easer get Cover Images'''
    def __init__(self):
        print('MyTinyTag3__init__ Func ...')
        self.__SongsData = []

    def get_tags(self, oggFs):
        from tinytag import TinyTag
        self.__tags = []

        if type(oggFs) == list:
            for self.__oggF in oggFs:
                self.__tags.append(TinyTag.get(self.__oggF))
                print(self.__oggF)
        else:
            self.__tags.append(TinyTag.get(self.__oggF))
            print(self.__oggF)

        return self.__tags
        
    def show_tags(self, oggF):
        from tinytag import TinyTag
        self.__tag = TinyTag.get(oggF)

        print('This track is by {}.'.format(self.__tag.artist))
        print(self.__tag.title)
        print(u'It is {:04.2f} seconds long.'.format(self.__tag.duration))
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
        print(u'{:02.2f} MiB'.format(self.__tag.filesize/1024/1024))
        print(self.__tag.genre)
        print(self.__tag.samplerate)
        return self.__tag

    def getCoverImg(self, f):
        self.__tag = TinyTag.get(f, image=True)
        self.__img_data = self.__tag.get_image()

class MEyed3:
    """ Eyed3 Modules """
    #eyed3.log.setLevel("ERROR")
    def __init__(self):
        self.__csvlist = ''
        self.__SongsData = ''
        self.__dir = ''

    def getMD5Hash(self, tag):
        key = '%s\t%s' % (tag.artist, tag.album)
        key = key.encode('utf-8')
        md5 = hashlib.md5()
        md5.update(key)
        return md5.hexdigest()

    def EchoMimeType(self):
        pass

    def emptyTag(self, audiofile):
        genre = 'Persian'
        comments = "WWW.AFW.IR : 1st Persian Audio Metadata Database"

    def rename(self, audiofile):
        new_filename = "sample/tagged/{0}-{1}.mp3".format(audiofile.tag.artist, audiofile.tag.title)
        os.rename('samples/tagged/song1.mp3', new_filename)

    def embed_album_art(self, mp3_file, artwork_file, artist, item_title):
        #### TODO
        ## NOT WORKING
        #edit the ID3 tag to add the title, artist, artwork, date, and genre
        tag = eyed3.Tag()
        tag.link(mp3_file)
        tag.setVersion([2,3,0])
        tag.addImage(0x08, artwork_file)
        tag.setArtist(artist)
        tag.setDate(localtime().tm_year)
        tag.setTitle(item_title)
        tag.setGenre(u"Trance")
        tag.update()

    def get_album_art(self, path, f):
        self.__audiofile = eyed3.core.load(f)
        for self.__img in self.__audiofile.tag.images:
            if self.__img.picture_type == 3:
                self.__fw = open("{0}{1}-{2}_{3}.jpg".format(path, self.__audiofile.tag.artist,
                                                self.__audiofile.tag.album, 'COVER_FRONT'), 'w+b')
                print(u"Writing image file: , {0}{1}-{2}_{3}.jpg".format(path, self.__audiofile.tag.artist,
                                                                    self.__audiofile.tag.album, 'COVER_FRONT'))
                self.__fw.write(self.__img.image_data)

    def get_album_art2(self):
        FRONT_COVER = eyed3.id3.frames.ImageFrame.FRONT_COVER
        audiofile = eyed3.load("test.id3")
        IMAGES = audiofile.tag.images
        with open("./FRONT_COVER.jpg", "rb") as fp:
            IMAGES.set(FRONT_COVER, fp.read(), "img/jpg", u"")
        audiofile.tag.save(encoding='utf-8', version=eyed3.id3.ID3_V2_4)

    def get_lyrics(self, filename):
        url = "http://www.azlyrics.com/lyrics/" + artist + "/" + song + ".html"
            # Getting Source and extracting lyrics
        text = urllib2.urlopen(url).read()
        where_start = text.find('<!-- start of lyrics -->')
        start = where_start + 26
        where_end = text.find('<!-- end of lyrics -->')
        end = where_end - 2
        lyrics = unicode(text[start:end].replace('<br />', ''), "UTF8")
        pass

    def setTagVersion(self, f, ver):
        self.__audiofile = eyed3.core.load(f)
        if (self.__audiofile.tag == None):
            self.__audiofile.initTag()

        if ver == '2.4.0':
            self.__audiofile.tag.save(version=eyed3.id3.ID3_V2_4)
        if ver == '2.3.0':
            self.__audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
        
        print(f, 'Tag Version Changed to ', ver)


    def MP3_Tag(self, audiofiles, tag, searchStr):
        self.__counter = 0
        for self.__filename in audiofiles:
            self.__audiofile = eyed3.load(self.__filename)
            self.__genre = audiofile.tag.genre
            #searchstr = "[wWw.[a-zA-z0-9].[com|org|net]"(Path(mp3s).rglob('*.mp3'))
            #seaingenere = re.compile(str(genre))
            print(self.__filename)
            print(self.__seaingenere.findall(searchStr))
            self.__counter += 1
            print(u'Found ' + str(self.__counter) + '  Music File with www in Gener or In Coments.')

    def saveTagsFromCSV(self, pf):
        from collections import deque
        #get_logger('MD3Logger Start Save Tags in CSV file', 'MD3Logger', 'DEBUG')
        if os.path.isfile(pf):
            self.__csvlist = self.readCSVf(pf)
        else:
            print(u'There is no CSV file : !!!', pf)
            exit(1)

        self.__csvlist.pop(0)
        ## .popleft()
        for self.__row in self.__csvlist:
            self.__f = ''.join((self.__row[17], self.__row[0]))
            print(self.__f)
            audiofile = eyed3.core.load(self.__f)
            if self.__row[1] is not None:
                audiofile.tag.artist = self.__row[1]
            if self.__row[2] is not None:
                audiofile.tag.title = self.__row[2]
            if self.__row[3] is not None:
                audiofile.tag.album = self.__row[3]
            if self.__row[4] is not None:
                audiofile.tag.album_artist = self.__row[4]
            if self.__row[5] != '':
                audiofile.tag.track_num = (int(self.__row[5])) 
                if self.__row[5] and self.__row[6] != '':
                    audiofile.tag.track_num = (int(self.__row[5]), int(self.__row[6]))
            if self.__row[7] != '':
                audiofile.tag.disc_num = (int(self.__row[7]))
                if self.__row[7] and self.__row[8] != '':
                    audiofile.tag.disc_num = (int(self.__row[7]), int(self.__row(8)))
            if self.__row[9] is not None:
                audiofile.tag.release_date = self.__row[9]
            if self.__row[10] is not None:
                audiofile.tag.genre = self.__row[10]
            if self.__row[11] is not None:
                audiofile.tag.comments.set(self.__row[11])
            if self.__row[12] is not None:
                audiofile.tag.publisher = self.__row[12]
            if self.__row[13] is not None:
                audiofile.tag.lyrics.set(self.__row[13])
            print(u'Metadata of this file : ')
            audiofile.tag.save(version=(2, 3, 0))

    def show_Tags(self, tag):
        #get_logger('MD3Logger Start Showing all Tags of Eyed3 Song Object', 'MD3Logger', 'DEBUG')
        print(u'{:12} : {}'.format('File Name', tag[0]))
        print(u'{:12} : {}'.format('Artist(s)', tag[1]))
        print(u'{:12} : {}'.format('Title', tag[2]))
        print(u'{:12} : {}'.format('Album', tag[3]))
        print(u'{:12} : {}'.format('Album Artist', tag[4]))
        print(u'{:12} : {} {} : {}'.format('Track Number', tag[5], 'In', tag[6]))
        print(u'{:12} : {} {} : {}'.format('Disk Number', tag[7], 'All Disks', tag[8]))
        print(u'{:12} : {}'.format('Date', tag[9]))
        print(u'{:12} : {}'.format('Gener', tag[10]))
        print(u'{:12} : {}'.format('Comments', tag[11]))
        print(u'{:12} : {}'.format('Publisher', tag[12]))
        print(u'{:12} : {}'.format('Lyrics', tag[13]))
        print(u'{:12} : {}'.format('ID3 Version', tag[14]))
        print(u'{:12} : {}'.format('Tag Size', tag[15]))
        print(u'{:12} : {:04.2f} (Mega Byte)'.format('File Size', float(tag[16])))
        print(u'{:12} : {}'.format('Path', tag[17]))
        #print(u'{:12} : {}'.format('Extention', tag[18]))
        print(u'{:12} : {}'.format('Created', tag[19]))
        print(u'{:12} : {}'.format('Modified', tag[20]))
        print(u'------------------------------------')

    def get_Tags(self, f):
        import time
        #get_logger('MD3Logger Start Get all Metadata of MP3 file', 'MD3Logger', 'DEBUG')
        #print(f)

        self.__tags = eyed3.core.load(f)
        self.__path =''.join((os.path.dirname(f), '/'))
        self.__mtime = time.strftime("%Y/%m/%d %a - %H:%M:%S", time.localtime(os.path.getmtime(f)))
        self.__ctime = time.strftime("%Y/%m/%d %a - %H:%M:%S", time.localtime(os.path.getctime(f)))
        self.__id3version = str(self.__tags.tag.version[0]) + '.' + str(self.__tags.tag.version[1])

        if len(self.__tags.tag.comments) > 0:
            self.__comm = self.__tags.tag.comments[0].text
            self.__commlang = self.__tags.tag.comments[0].lang
        else:
            self.__comm = ''

        if len(self.__tags.tag.lyrics) > 0:
            self.__lyric = self.__tags.tag.lyrics[0].text
            self.__lyriclang = self.__tags.tag.lyrics[0].lang
        else:
            self.__lyric = ''

        self.__tags = [
            os.path.basename(f), self.__tags.tag.artist, self.__tags.tag.title,
            self.__tags.tag.album, self.__tags.tag.album_artist, self.__tags.tag.track_num[0],\
            self.__tags.tag.track_num[1], self.__tags.tag.disc_num[0], self.__tags.tag.disc_num[1],\
            self.__tags.tag.release_date, self.__tags.tag.genre, self.__comm, self.__tags.tag.publisher,\
            self.__lyric, self.__id3version, self.__tags.tag.header.tag_size,\
            os.path.getsize(f)/1024/1024, os.path.dirname(f) + "/", os.path.splitext(f)[1],\
            self.__mtime, self.__ctime
            ]

        self.__tags = self.removeNone(self.__tags)
        return self.__tags

    def makeCSVf(self, pf):
        import csv
        print(u'Creating New Music MetaData File ',pf)
        try:
            with open(pf, 'w', newline='') as self.__csvfile:
                self.__fieldnames = ['File Name','Artist', 'Title', 'Album', 'AlbumArtists', 'Track Number',\
                    'Totall Tracks', 'Disk Number', 'All Disks','Date', 'Gener', 'Comments',\
                    'Publisher','Lyrics', 'ID3 Version', 'Tag Size', 'Size (MiB)', 'Path',\
                    'File Extention', 'Last Access',\
                    'Last Modify', 'coverArtFileName']
                writer = csv.DictWriter(self.__csvfile, fieldnames=self.__fieldnames)
                writer.writeheader()
            self.__csvfile.close()
        except IOError:
            print(u'Error: File {} Was Not Created.'.format(pf))
        else:
            print(u'File {} was created. and Header of CSV was added.'.format(pf))

        return True

    def saveCSVf(self, pf, csvlist):
        import csv
        #get_logger('MD3Logger Start Save Tags in CSV file', 'MD3Logger', 'DEBUG')
        try:
            if not os.path.exists(pf):
                self.makeCSVf(pf)
            with open(pf, 'a', newline='') as self.__csvfile:
                for self.__row in csvlist:
                    writer = csv.DictWriter(self.__csvfile, self.__row)
                    writer.writeheader()
                print(u'The Tags Was writed to CSV file.')
            self.__csvfile.close()
        except IOError:
            print(u'File was not find.')
        else:
            print(u' -- CSV file Saved.')
        return True

    def correctPath(self, csvlist):
        #get_logger('MD3Logger Start fix path of CSV file', 'MD3Logger', 'DEBUG')
        for self.__row in csvlist:
            self.__row[16] = ''.join((self.__row[16], '/'))
        return csvlist

    def readCSVf(self, pf):
        import csv
        #get_logger('MD3Logger Start Read CSV file', 'MD3Logger', 'DEBUG')
        with open(pf) as self.__csvfile:
            self.__csvlist = csv.reader(self.__csvfile)
            return list(self.__csvlist)

    def setAudioTags(self, f, tagName, tagText):
        self.__audiofile = eyed3.load(f)
        if (self.__audiofile.tag == None):
            self.__audiofile.initTag()

        self.__audiofile.tag.artist = ''

    def removeNone(self, tags):
        #get_logger('MD3Logger Start Remove None Tags', 'MD3Logger', 'DEBUG')
        tags = list(map(str, tags))
        tags = [ self.__tag.replace('None', '') for self.__tag in tags ]
        return tags

    def getMP3sTags(self, mp3s):
        #get_logger('MD3Logger Start Split MP3 files', 'MD3Logger', 'DEBUG')
        self.__SongsData = []

        for self.__f in mp3s:
            self.__tags = self.get_Tags(self.__f)
            self.__SongsData.append(self.__tags)
        return self.__SongsData

    def splitCSVlist(self, csvlist):
        #get_logger('MD3Logger Start Split CSV file', 'MD3Logger', 'DEBUG')
        self.__mp3s = []
        for self.__row in csvlist:
            if self.__row[17] != 'Path':
                self.__fp = ''.join((self.__row[17], self.__row[0]))
                print('Read Tags Of {} File From CSV'.format(self.__fp))
                self.__mp3s.append(self.__fp)
        return self.__mp3s

def get_args(args):
    import argparse

    description = (
                    "Get and Set your Music MetaData in [CSV file].\n"
                    "You set a path with an argumant -p, then application\n"
                    "create a CSV file, with all MetaData Tags of all your Musics\n"
                    "you set for application [recursivly]."
    )
    parser = argparse.ArgumentParser(prog='md3.sh', description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--path', '-p', required=False, help='Music path or directory. Default is user Home Music Directory')
    parser.add_argument('--csvin', '-i', required=False, help='Name of Music Metadata CSV file to Write Musics Metadata from that file')
    parser.add_argument('--csvout', '-o', required=False, help='Name of Music Metadata CSV file.Default is md3.csv')
    parser.add_argument('--mfile', '-m', required=False, help='Display Metadata[s] of this file')
    parser.add_argument('--tag', '-t', required=False, help='Display This Tag of Music file')

    return parser.parse_args()

def main(argv):
    clear = lambda: os.system('clear')
    clear()
    print(u'Start Time:', datetime.datetime.now())
    start_time = datetime.datetime.now()

    print(u'\n\t\u2554', end='')
    for i in range(25):
        print(u'\u2550', end='')
    print(u'\u2557\n\t\u2551', u' ## WellCome To MD3 ## ', u'\u2551\n\t\u255a', end='')
    for i in range(25):
        print(u'\u2550', end='')
    print(u'\u255d\n')

    args = get_args(argv)

    if args.mfile:
        argMP3 = args.mfile
    else:
        argMP3 = 'donya.mp3'

    if args.path:
        path = args.path
    else:
        home = Path.home()
        path = str(home) + '/Music/md3/'

    mp3 = ''
    mp3SongsData = []
    oggs = ''
    oggSongsData = []

    print("What Do You Want To Do ?")
    print("\t1 - Get Tags of a Music")
    print("\t2 - Get Tags of a path Musics")
    print("\t3 - Get Tags of all path Musics Recursive")
    print("\t4 - Create CSV file")
    print("\t5 - Create CSV file")
    print("\t6 - Save Musics Tag from a CSV file")
    
    answ = getch()
    print(answ)

    home = Path.home()
    path = str(home) + '/Music/'
    print("This is your Path : {} ? (y/n) : ".format(path))
    path_is_ok = getch()
    if path_is_ok == 'n':
        path = input("Please Enter Your Path : ")
        
    cCSV = ''
    pf = ''

    if answ == '1':
        print("Tags of {} file? (y/n) : ".format(argMP3))
        mp3tag_answ = getch()
        if mp3tag_answ == 'n':
            argMP3 = input("Enter Your Music File Name : ")

        myMP3s = MEyed3()
        argMP3 = ''.join((path, argMP3))
        mp3SongData = myMP3s.get_Tags(argMP3)
        myMP3s.show_Tags(mp3SongData)

    elif answ == '2' or answ == '3':
        mp3s = ''
        try:
            if os.path.exists(path):
                if answ == '2':
                    mp3s = glob2.glob(path + '*.mp3')
                    oggs = glob2.glob(path + '*.ogg')
                    print(mp3s)
                elif answ == '3':
                    mp3s = glob2.glob(path + '**/*.mp3')
                    oggs = glob2.glob(path + '**/*.ogg')
                    print(mp3s)
        except Exception:
            print(u'{} Not find.'.format(pf))

        SongsData = ''
        if type(mp3s) is list:
            myMP3s = MEyed3()
            SongsData = myMP3s.getMP3sTags(mp3s)
            for SongData in SongsData:
                myMP3s.show_Tags(SongData)

    elif answ == '4' or answ == '5':
        csv_filename = 'md3.csv'
        print("The CSV File Name : {} ? (y/n) : ".format(csv_filename))
        cCSV = getch()
        if cCSV == 'n':
            csv_filename = input("Enter Your CSV File Name : ")

        pf = ''.join((path, csv_filename))
        myMP3s = MEyed3()
        try:
            if os.path.isdir(path):
                if answ == '4':
                    mp3s = glob2.glob(path + '*.mp3')
                    oggs = glob2.glob(path + '*.ogg')
                elif answ == '5':
                    mp3s = glob2.glob(path + '**/*.mp3')
                    oggs = glob2.glob(path + '**/*.ogg')
        except Exception:
            print(u'{} Not find.'.format(pf))

        SongsData = myMP3s.getMP3sTags(mp3s)
        myMP3s.saveCSVf(pf, SongsData)

    elif answ == '6':
        csv_filename = 'md3.csv'
        print("The CSV File Name : {} ? (y/n) : ".format(csv_filename))
        cCSV = getch()
        if cCSV == 'n':
            csv_filename = input("Enter Your CSV File Name : ")

        pf = ''.join((path, csv_filename))
        myMP3s = MEyed3()

        csvlist = myMP3s.readCSVf(pf)
        csvlist = myMP3s.correctPath(csvlist)
        mp3s = myMP3s.splitCSVlist(csvlist)
        myMP3s.saveTagsFromCSV(pf)
        
    print(u'Bye.\n\nEnd Time: {}'.format(datetime.datetime.now()))
    print(datetime.datetime.now()-start_time)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
