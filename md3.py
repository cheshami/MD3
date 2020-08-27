#!/usr/bin/env python3
"""
# An Audio MetaData Editor Application.
# Author : R.Cheshami
# Company : Adak Free Way .. http://afw.ir

tags[] = getAllTags(f)
tag = getTag(f, tagname)
***************
CLI :

md3 file
    ************* file.mp3 ***************
    Title : ?????????????
    Artist : ????????????????
    Album : ???????????????
    *
    *
    *
    ***************************************
"""
import os, re, glob2, eyed3, pprint
from pathlib import Path
import pandas as pd
import csv
import logging


def get_logger(name=None, level=logging.DEBUG, create_file=False):
    if name is None:
        name = inspect.stack()[1][1].split('.')[0]
    formatter = logging.Formatter("MD3 %(levelname)s Logging Message: %(asctime)s - %(process)d -  - %(threadName)s - %(name)s %(message)s")
    log = logging.getLogger(name)
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

def getchar():
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

class MMD3():
    def no_padding(info):
        # this will remove all padding
        return None

    def default_implementation(info):
        # this is the default implementation, which can be extended
        return info.get_default_padding()

    def no_new_padding(info):
        # this will use existing padding but never add new one
        return max(info.padding, 0)

    def padd(audiofile):
        from mutagen.mp3 import MP3

        f = MP3("somefile.mp3")
        f.save(padding=no_padding)
        #f.save(padding=default_implementation)
        #f.save(padding=no_new_padding)

    def embed_album_art(cover_filepath, audio_filepaths):
        import mutagen
        """ Embed album art into audio files. """
        with open(cover_filepath, "rb") as f:
            cover_data = f.read()
        #for filepath in audio_filepaths:
        mf = mutagen.File(audio_filepaths)
        if (isinstance(mf.tags, mutagen._vorbis.VComment) or isinstance(mf, mutagen.ogg.OggFileType)):
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

    def get_album_art(file, pic):
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


    def mutgReadTags(audiofile):
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

    def mutgAddImage(f, image):
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


class MD3():
	# Main Class
	SongsData = []
	pp = pprint.PrettyPrinter(indent=4, sort_dicts=True)
	def __init__():
		print('WellCome Tp MD3')

    import eyed3
    def getMD5Hash(tag):
        key = '%s\t%s' % (tag.artist, tag.album)
        key = key.encode('utf-8')
        md5 = hashlib.md5()
        md5.update(key)
        return md5.hexdigest()

    def EchoMimeType():
        pass

    def renameaudiofile(audiofile):
        new_filename = "sample/tagged/{0}-{1}.mp3".format(audiofile.tag.artist, audiofile.tag.title)
        os.rename('samples/tagged/song1.mp3', new_filename)

    def embed_album_art(mp3_file_name, artwork_file_name, artist, item_title):
        #### TODO
        ## NOT WORKING
        #edit the ID3 tag to add the title, artist, artwork, date, and genre
        tag = eyed3.Tag()
        tag.link(mp3_file_name)
        tag.setVersion([2,3,0])
        tag.addImage(0x08, artwork_file_name)
        tag.setArtist(artist)
        tag.setDate(localtime().tm_year)
        tag.setTitle(item_title)
        tag.setGenre(u"Trance")
        tag.update()

    def get_album_art(path, f):
        audiofile = eyed3.core.load(f)
        for img in audiofile.tag.images:
            if img.picture_type == 3:
                fw = open("{0}{1}-{2}_{3}.jpg".format(path, audiofile.tag.artist, audiofile.tag.album, 'COVER_FRONT'), 'w+b')
                print("Writing image file: , {0}{1}-{2}_{3}.jpg".format(path, audiofile.tag.artist, audiofile.tag.album, 'COVER_FRONT'))
                fw.write(img.image_data)

    def get_album_art2():
        FRONT_COVER = eyed3.id3.frames.ImageFrame.FRONT_COVER
        audiofile = eyed3.load("test.id3")
        IMAGES = audiofile.tag.images
        with open("./FRONT_COVER.jpg", "rb") as fp:
            IMAGES.set(FRONT_COVER, fp.read(), "img/jpg", u"")
        audiofile.tag.save(encoding='utf-8', version=eyed3.id3.ID3_V2_4)

    def get_lyrics(filename):
        url = "http://www.azlyrics.com/lyrics/" + artist + "/" + song + ".html"
            # Getting Source and extracting lyrics
        text = urllib2.urlopen(url).read()
        where_start = text.find('<!-- start of lyrics -->')
        start = where_start + 26
        where_end = text.find('<!-- end of lyrics -->')
        end = where_end - 2
        lyrics = unicode(text[start:end].replace('<br />', ''), "UTF8")
        return lyrics

    def audioTag(audiofiles, tag, searchStr):
        counter = 0
        for filename in audiofiles:
            audiofile = eyed3.load(filename)
            genre = audiofile.tag.genre
            #searchstr = "[wWw.[a-zA-z0-9].[com|org|net]"(Path(mp3s).rglob('*.mp3'))
            #seaingenere = re.compile(str(genre))
            print(filename)
            print(seaingenere.findall(searchStr))
            counter += 1
            print('Found ' + str(counter) + '  Music File with www in Gener or In Coments.')

    def saveTagsFromCSV(pf):
        from collections import deque
        csvlist = MD3.readCSVf(pf)
        csvlist.pop(0)## .popleft()
        for row in csvlist:
            print(row[0])
            f = row[16] + row[0]
            audiofile = eyed3.core.load(f)
            if row[1] is not None:
                audiofile.tag.artist = row[1]
            if row[2] is not None:
                audiofile.tag.title = row[2]
            if row[3] is not None:
                audiofile.tag.album = row[3]
            if row[4] is not None:
                audiofile.tag.album_artist = row[4]
            if row[5] and row[6] is not None:
                audiofile.tag.track_num = int(row[5]), int(row[6])
            elif row[5] is not None:
                audiofile.tag.track_num = int(row[5])
            if row[7] is not None:
                    audiofile.tag.disc_num = int(row[7])
            if row[9] is not None:
                audiofile.tag.release_date = row[9]
            if row[10] is not None:
                audiofile.tag.genre = row[10]
            if row[11] is not None:
                audiofile.tag.comments[0].text = row[11]
            if row[12] is not None:
                audiofile.tag.publisher = row[12]
            if row[13] is not None:
                audiofile.tag.lyrics[0].text = row[13]
            audiofile.tag.save()

    def showAudioTags(tags):
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
        print('Extention : ', tags[18])
        print('Created : ', tags[19])
        print('Modified : ', tags[20])
        print('------------------------------------')

    def makeCSVf(path, file='SongsData.csv'):
        with open(path+file, 'w', newline='') as csvfile:
            fieldnames = ['File Name','Artist', 'Title', 'Album', 'AlbumArtists', 'Track Number',\
                'Totall Tracks', 'Disk Number', 'All Disks','Date', 'Gener', 'Comments', 'Publisher',\
                'Lyrics', 'ID3 Version', 'Tag Size', 'Path',\
                'File Extention', 'Last Access',\
                'Last Modify', 'Size Byte', 'coverArtFileName']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        csvfile.close()
        return True

    def saveCSVf(pf, csvlist):
        if os.path.isfile(pf):
            print(pf)
            with open(pf, 'a', newline='') as csvfile:
                for row in csvlist:
                    writer = csv.DictWriter(csvfile, row)
                    writer.writeheader()
            csvfile.close()
        return True    

    def readCSVf(pf):
        print(pf)
        with open(pf) as csvfile:
            csvlist = csv.reader(csvfile)
            return list(csvlist)

    def setAudioTags(f, tagName, tagText):
        audiofile = eyed3.load(f)
        if (audiofile.tag == None):
            audiofile.initTag()

        audiofile.tag.artist = ''

    def removeNone(tags):
        tags = list(map(str, tags))
        tags = [ tag.replace('None', '') for tag in tags ]
        return tags

    def splitMP3s(mp3s):
        SongsData = []

        for f in mp3s:
            tags = MD3.getAllTag(f)
            SongsData.append(tags)
        return SongsData

    def getAllTag(f):
        import time
        tags = eyed3.core.load(f)
        #get_logger('getAllTag', 'WARNING')

        path = os.path.dirname(f)
        mtime = time.strftime("%Y/%m/%d %a - %H:%M:%S", time.localtime(os.path.getmtime(f)))
        ctime = time.strftime("%Y/%m/%d %a - %H:%M:%S", time.localtime(os.path.getctime(f)))
        id3version = str(tags.tag.version[0]) + '.' + str(tags.tag.version[1])
        
        if len(tags.tag.comments) > 0:
            comm = tags.tag.comments[0].text
        else:
            comm = ''
        if len(tags.tag.lyrics) > 0:
            lyric = tags.tag.lyrics[0].text
        else:
            lyric = ''

        tags = [
            os.path.basename(f), tags.tag.artist, tags.tag.title,
            tags.tag.album, tags.tag.album_artist, tags.tag.track_num[0],\
            tags.tag.track_num[1], tags.tag.disc_num[0], tags.tag.disc_num[1],\
            tags.tag.release_date, tags.tag.genre, comm, tags.tag.publisher,\
            lyric, id3version, tags.tag.header.tag_size,\
            os.path.getsize(f), os.path.dirname(f) + "/", os.path.splitext(f)[1],\
            mtime, ctime
            ]

        tags = MD3.removeNone(tags)
        return tags

def main():
    # DEBUG INFO WARNING ERROR CRITICAL
    get_logger('MD3Logger', 'DEBUG')
    
    path = '/home/ro/Downloads'
    filename = '/SongsData.csv'
    pf = path.join(filename)

    #mp3s = glob2.glob(path+'*/*.mp3')
    mp3s = '/home/ro/Music/md3/donya.mp3'

    if type(mp3s) is list:
        SongsData = MD3.splitMP3s(mp3s)
        for SongData in SongsData:
            MD3.showAudioTags(SongData)
    else:
        SongData = MD3.getAllTag(mp3s)
        MD3.showAudioTags(SongData)

    #SongsData = MD3.readCSVf(pf)
    #MD3.saveTagsFromCSV(pf)
    
    #MD3.makeCSVf(path)
    #MD3.saveCSVf(pf, SongsData)
    #pprint.pp(SongsData)
    #MMD3.mutgReadTags(mp3s)
    #MMD3.embed_album_art('/home/ro/Music/md3/Ball.jpg', '/home/ro/Music/md3/donya.mp3')
    #MD3.get_album_art('/home/ro/Music/md3/','/home/ro/Music/md3/donya.mp3')

if __name__ == '__main__':
    main()
