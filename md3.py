#!/usr/bin/env python3
'''
## An Audio MetaData Editor Application.
## Author : R.Cheshami
## Company : Adak Free Way .. http://afw.ir
'''
import sys, os, re, glob2
from os import path
from pathlib import Path
import logging
import threading
import datetime, time
import csv
import eyed3
import pprint

def get_logger(self, msg='',cfname=None, name=None, level=logging.DEBUG, create_file=False):
    log = logging.getLOGGer(__name__)
    # get_logger('msg', 'MD3LOGGer', 'WARNING')
    if name is None:
        name = inspect.stack()[1][1].split('.')[0]
    formatter = logging.Formatter(
        "MD3 %(levelname)s LOGGing Message: %(asctime)s - %(process)d -  - %(threadName)s - %(name)s %(message)s")
    
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

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    """Fetch and character using the termios module."""
    def __init__(self):
        import tty, sys
        from select import select

    def __call__(self):
        import sys, tty, termios
        from select import select

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(sys.stdin.fileno())

            # [ Wait until ready for reading,
            #   wait until ready for writing
            #   wait for an "exception condition" ]
            # The below line times out after 1 second
            # This can be changed to a floating-point value if necessary
            [i, o, e] = select([sys.stdin.fileno()], [], [], 1)
            if i:
                ch = sys.stdin.read(1)
            else:
                ch = None

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch


class _GetchWindows:
    """Fetch a character using the Microsoft Visual C Runtime."""
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        import time

        # Delay timeout to match UNIX behaviour
        time.sleep(1)

        # Check if there is a character waiting, otherwise this would block
        if msvcrt.kbhit():
            return msvcrt.getch()

        else:
            return

'''
    # Check Variables Values & Encode Them and substitute back-ticks
    if artist:
        artist.encode()
        artist = re.sub(u'`', u"'", artist)
    else:
        artist = 'Not Listed'
    if title is not None:
        title.encode()
        titlez = re.sub(u'`', u"'", title)
    else:
        titlez = 'Not Listed'
    if audiofile_path is not None:
        audiofile_path.encode()
        audiofile_pathz = re.sub(u'`', u"'", audiofile_path)
    else:
        audiofile_pathz = ('Not Listed, and you have an the worst luck, '
                       'because this is/should not possible.')
        # print them out
    try:
        if artist is not None and title is not None and audiofile_path is not None:
            print('Artist: "{}"'.format(artistz))
            print('audiofile : "{}"'.format(titlez))
            print('Path  : "{}"'.format(audiofile_pathz))
    except Exception as e:
        raise e

, str(audiofile.tag.comments[0].text), 
, audiofile.tag.images.get(3, )

'''
class MMutagen3:
    def __init__(self):
        self.__df = ''

    def getchar(self):
        try:
            import msvcrt
            getch = msvcrt.getch
        except:
            import sys, tty, termios
            def _unix_getch():
                """Get a single character from stdin, Unix version"""

                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())          # Raw read
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch

        return _unix_getch


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
        if (isinstance(mf.tags, mutagen._vorbis.VComment) or isinstance(mf, mutagen.OGG.OGGFileType)):
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
                print("Error reading %s:" % path, e)
                return None

        try:
            image = extractFrontCover(metadata)
        except OSError:
            print('Error extracting image from %s' % path)
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

            print("Artist: %s" % audio['TPE1'].text[0])
            print("Track: %s" % audio["TIT2"].text[0])
            #print("Release Year: %s" % audio["TDRC"].text[0])
            print('-------------------------------------------')



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
    '''for OGG files and easer get Cover Images'''
    def __init__(self):
        self.__SongsData = []

    def getOGGsTags(self, OGGFs):
        self.__tags = []

        if type(OGGFs) == list:
            for self.__OGGF in OGGFs:
                self.__tags.append(self.showOGGTags(self.__OGGF))
        else:
            self.__tags.append(self.showOGGTags(self.__OGGFs))
        return self.__tags
        
        

    def showOGGTags(self, OGGF):
        from tinytag import TinyTag

        self.__tag = TinyTag.get(OGGF)

        print('This track is by {}.'.format(self.__tag.artist))
        print(self.__tag.title)
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


    def getCoverImg(self, f):
        self.__tag = TinyTag.get(f, image=True)
        self.__img_data = self.__tag.get_image()

class MEyed3:
    """tags[] = getMP3Tagss(f)
        tag = getTag(f, tagname)
        ****   *********
        setAllTags(tags[])
        setTag(f, tagname)
        ***********
        md3.getTagz(f)
        md3.setTags(f)
    """    
    def __init__(self):
        print('__init__ Func ...')
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
                self.__fw = open("{0}{1}-{2}_{3}.jpg".format(path, self.__audiofile.tag.artist, self.__audiofile.tag.album, 'COVER_FRONT'), 'w+b')
                print("Writing image file: , {0}{1}-{2}_{3}.jpg".format(path, self.__audiofile.tag.artist, self.__audiofile.tag.album, 'COVER_FRONT'))
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


    def audioTag(self, audiofiles, tag, searchStr):
        self.__counter = 0
        for self.__filename in audiofiles:
            self.__audiofile = eyed3.load(self.__filename)
            self.__genre = audiofile.tag.genre
            #searchstr = "[wWw.[a-zA-z0-9].[com|org|net]"(Path(mp3s).rglob('*.mp3'))
            #seaingenere = re.compile(str(genre))
            print(self.__filename)
            print(self.__seaingenere.findall(searchStr))
            self.__counter += 1
            print('Found ' + str(self.__counter) + '  Music File with www in Gener or In Coments.')

    def saveTagsFromCSV(self, pf):
        from collections import deque
        #get_logger('MD3LOGGer Start Save Tags in CSV file', 'MD3LOGGer', 'DEBUG')
        if os.path.isfile(pf):
            self.__csvlist = mycsv.readCSVf(pf)
        else:
            print('There is no CSV file : !!!', pf)
            exit(1)

        self.__csvlist.pop(0)
        ## .popleft()
        for self.__row in self.__csvlist:
            self.__f = ''.join((self.__row[17], self.__row[0]))
            print(self.__f)
            audiofile = eyed3.core.load(self.__f)
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
            print('Metadata of this file : ')
            pprint.pp(self.__row)
            audiofile.tag.save(version=(2, 3, 0))

    def showAudioTags(self, tags):
        #get_logger('MD3LOGGer Start Showing all Tags of Eyed3 Song Object', 'MD3LOGGer', 'DEBUG')
        print(len(tags))
        print('File Name : ', tags[0])
        print('Artist : ', tags[1])
        print('Title : ', tags[2])
        print('Album : ', tags[3])
        print('Album Artists : ', tags[4])
        print('Track Number : ', tags[5], ' Totall : ', tags[6])
        print('Disk Number : ', tags[7], ' All Disks : ', tags[8])
        print('Date : ', tags[9])
        print('Gener : ', tags[10])
        print('Comments : ', tags[11])
        print('Publisher : ', tags[12])
        print('Lyrics : ', tags[13])
        print('ID3 Version : ', tags[14])
        print('Tag Size : ', tags[15])
        print('File Size : ', format(tags[16]), '(Byte)')
        print('Path : ', tags[17])
        #if tags[18]:
         #   print('Extention : ', tags[18])
        print('Created : ', tags[19])
        print('Modified : ', tags[20])
        print('------------------------------------')

    def getMP3Tags(self, f):
        #get_logger('MD3LOGGer Start Get all Metadata of MP3 file', 'MD3LOGGer', 'DEBUG')
        print(f)

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
            os.path.getsize(f), os.path.dirname(f) + "/", os.path.splitext(f)[1],\
            self.__mtime, self.__ctime
            ]

        self.__tags = self.removeNone(self.__tags)
        return self.__tags

    def makeCSVf(self, pf):
        print('Create New Music MetaData File in ',pf)
        try:
            with open(pf, 'w', newline='') as self.__csvfile:
                self.__fieldnames = ['File Name','Artist', 'Title', 'Album', 'AlbumArtists', 'Track Number',\
                    'Totall Tracks', 'Disk Number', 'All Disks','Date', 'Gener', 'Comments',\
                    'Publisher','Lyrics', 'ID3 Version', 'Tag Size', 'Size Byte', 'Path',\
                    'File Extention', 'Last Access',\
                    'Last Modify', 'coverArtFileName']
                writer = csv.DictWriter(self.__csvfile, fieldnames=self.__fieldnames)
                writer.writeheader()
            self.__csvfile.close()
        except IOError:
            print('Error: File {} Was Not Created.', format(pf))
        else:
            print('File {} was created. and Header of CSV was added.', format(pf))

        return True

    def saveCSVf(self, pf, csvlist):
        #get_logger('MD3LOGGer Start Save Tags in CSV file', 'MD3LOGGer', 'DEBUG')
        try:
            if os.path.isfile(pf):
                self.makeCSVf(pf)
            with open(pf, 'a', newline='') as self.__csvfile:
                for self.__row in csvlist:
                    writer = csv.DictWriter(self.__csvfile, self.__row)
                    print(writer)
                    writer.writeheader()
                print(' -- file Saved.')
            self.__csvfile.close()
        except IOError:
            print('File was not find.')
        else:
            print('The Tags Was writed to CSV file.')
        return True

    def correctPath(self, csvlist):
        #get_logger('MD3LOGGer Start fix path of CSV file', 'MD3LOGGer', 'DEBUG')
        for self.__row in csvlist:
            self.__row[16] = ''.join((self.__row[16], '/'))
        return csvlist

    def readCSVf(self, pf):
        #get_logger('MD3LOGGer Start Read CSV file', 'MD3LOGGer', 'DEBUG')
        print(pf)
        with open(pf) as self.__csvfile:
            self.__csvlist = csv.reader(self.__csvfile)
            print(self.__csvlist)
            return list(self.__csvlist)

    def setAudioTags(self, f, tagName, tagText):
        self.__audiofile = eyed3.load(f)
        if (self.__audiofile.tag == None):
            self.__audiofile.initTag()

        self.__audiofile.tag.artist = ''

    def removeNone(self, tags):
        #get_logger('MD3LOGGer Start Remove None Tags', 'MD3LOGGer', 'DEBUG')
        tags = list(map(str, tags))
        tags = [ self.__tag.replace('None', '') for self.__tag in tags ]
        return tags

    def getMP3sTags(self, mp3s):
        #get_logger('MD3LOGGer Start Split MP3 files', 'MD3LOGGer', 'DEBUG')
        self.__SongsData = []

        for self.__f in mp3s:
            self.__tags = self.getMP3Tags(self.__f)
            self.__SongsData.append(self.__tags)
        return self.__SongsData

    def splitCSVlist(self, csvlist):
        #get_logger('MD3LOGGer Start Split CSV file', 'MD3LOGGer', 'DEBUG')
        self.__mp3s = []
        for self.__row in csvlist:
            self.__fp = ''.join((self.__row[16], self.__row[0]))
            print(self.__fp)
            self.__mp3s.append(fp)
        return self.__mp3s

def get_args(args):
    import argparse

    description = (
                    "Get and Set your Music MetaData [with CSV file].\n"
                    "You set a path with an argumant -d, then application\n"
                    "create a CSV file, with all MetaData Tags of all Music files\n"
                    "you set for application [recursivly]."
    )
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--path', metavar='path', type=str, help='path or directory. Default is user Home Directory')
    parser.add_argument('-c', '--csv', required=False, help='Name of CSV file.Default is md3.csv')
    #parser.add_argument('-f', '--file', action='showAudioTags', required=False, help='Display Metadata[s] of this file')
    #parser.add_argument('-t', '--tag', action='showAudioTag', required=False, help='Display This Tag of Music file')

    return parser.parse_args()

def main(argv):
    eyed3.log.setLevel("ERROR")
    print('Start Time:', datetime.datetime.now(), '\n\n WellCome To MD3.')

    pp = pprint.PrettyPrinter(indent=4, sort_dicts=True)

    args = get_args(argv)
    
    path = args.path
    csv_filename = args.csv
    #music_file = args.file
    #tag_name = args.tag

    if not csv_filename:
        csv_filename = 'md3.csv'
    if not path:
        home = Path.home()
        print(home)
        path = str(home) + '/Music/md3/'

    pf = ''.join((path, csv_filename))

    mymp3s = MEyed3()
    myOGGs = MTinyTag3()

    try:
        if os.path.isfile(pf):
            mp3s = glob2.glob(path + '**/*.mp3')
            OGGs = glob2.glob(path + '**/*.ogg')
    except Exception:
        print('{} Not find.', format(pf))

    if type(mp3s) is list:
        SongsData = mymp3s.getMP3sTags(mp3s)
        
    if type(OGGs) is list:
        oggSongsData = []
        oggSongsData += myOGGs.getOGGsTags(OGGs)

    pp.pprint(SongsData)
    mymp3s.saveCSVf(pf, SongsData)
    #fi = ''.join((path,'donya.OGG'))
    #mymp3s.setTagVersion(fi, '2.4.0')

    #csvlist = mymp3s.readCSVf(pf)
    #csvlist = mymp3s.correctPath(csvlist)
    #mp3s = mymp3s.splitCSVlist(csvlist)
    #mymp3s.saveTagsFromCSV(pf)

    #MMD3.embed_album_art('/home/ro/Music/md3/Ball.jpg', '/home/ro/Music/md3/donya.mp3')
    #MD3.get_album_art('/home/ro/Music/md3/','/home/ro/Music/md3/donya.OGG')
    print('Bye.\n\nEnd Time: ', datetime.datetime.now())

if __name__ == '__main__':
    sys.exit(main(sys.argv))
