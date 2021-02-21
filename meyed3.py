import eyed3, enum

class SIZE_UNIT(enum.Enum):
    BYTES = 1
    KiB = 2
    MiB = 3
    GiB = 4
    TiB = 5

#eyed3.log.setLevel("ERROR")
def __init__():
    __csvlist = ''
    __SongsData = ''
    __dir = ''

def convert_unit(size_in_bytes, unit):
    """
    convert the size from bytes to other units linke KB, MB,...etc
    """
    if unit == SIZE_UNIT.KiB:
        return size_in_bytes/1024
    elif unit == SIZE_UNIT.MiB:
        return size_in_bytes/(1024*1024)
    elif unit == SIZE_UNIT.GiB:
        return size_in_bytes/(1024*1024*1024)
    elif unit == SIZE_UNIT.TiB:
        return size_in_bytes/(1024*1024*1024*1024)
    else:
        return(size_in_bytes)

def getMD5Hash(self, tag):
    key = '%s\t%s' % (tag.artist, tag.album)
    key = key.encode('utf-8')
    md5 = hashlib.md5()
    md5.update(key)
    return md5.hexdigest()

def emptyTag(self, audiofile):
    genre = 'Persian'
    comments = "WWW.AFW.IR : 1st Persian Audio Metadata Database"

def rename(self, audiofile):
    new_filename = "sample/tagged/{0}-{1}.mp3".format(audiofile.tag.artist,
                audiofile.tag.title)
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
    __audiofile = eyed3.core.load(f)
    for __img in __audiofile.tag.images:
        if __img.picture_type == 3:
            __fw = open("{0}{1}-{2}_{3}.jpg".format(
                        path, __audiofile.tag.artist,
                        __audiofile.tag.album, 'COVER_FRONT'), 'w+b')
            print(u"Writing image file: , {0}{1}-{2}_{3}.jpg".format(
                        path, __audiofile.tag.artist,
                        __audiofile.tag.album, 'COVER_FRONT'))
            __fw.write(__img.image_data)

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
    __audiofile = eyed3.core.load(f)
    if (__audiofile.tag == None):
        __audiofile.initTag()

    if ver == '2.4.0':
        __audiofile.tag.save(version=eyed3.id3.ID3_V2_4)
    if ver == '2.3.0':
        __audiofile.tag.save(version=eyed3.id3.ID3_V2_3)

    print(f, 'Tag Version Changed to ', ver)


def MP3_Tag(self, audiofiles, tag, searchStr):
    __counter = 0
    for __filename in audiofiles:
        __audiofile = eyed3.load(__filename)
        __genre = audiofile.tag.genre
        #searchstr = "[wWw.[a-zA-z0-9].[com|org|net]"(Path(mp3s).rglob('*.mp3'))
        #seaingenere = re.compile(str(genre))
        print(__filename)
        print(__seaingenere.findall(searchStr))
        __counter += 1
        print(u'Found '+str(__counter)+' Music File with www in Gener or In Coments.')

def saveTagsFromCSV(self, pf):
    from collections import deque
    #get_logger('MD3Logger Start Save Tags in CSV file', 'MD3Logger', 'DEBUG')
    if os.path.isfile(pf):
        __csvlist = readCSVf(pf)
    else:
        print(u'There is no CSV file : !!!', pf)
        exit(1)

    __csvlist.pop(0)
    ## .popleft()
    for __row in __csvlist:
        __f = ''.join((__row[17], __row[0]))
        print(__f)
        audiofile = eyed3.core.load(__f)
        if __row[1] is not None:
            audiofile.tag.artist = __row[1]
        if __row[2] is not None:
            audiofile.tag.title = __row[2]
        if __row[3] is not None:
            audiofile.tag.album = __row[3]
        if __row[4] is not None:
            audiofile.tag.album_artist = __row[4]
        if __row[5] != '':
            audiofile.tag.track_num = (int(__row[5]))
            if __row[5] and __row[6] != '':
                audiofile.tag.track_num = (int(__row[5]), int(__row[6]))
        if __row[7] != '':
            audiofile.tag.disc_num = (int(__row[7]))
            if __row[7] and __row[8] != '':
                audiofile.tag.disc_num = (int(__row[7]), int(__row(8)))
        if __row[9] is not None:
            audiofile.tag.release_date = __row[9]
        if __row[10] is not None:
            audiofile.tag.genre = __row[10]
        if __row[11] is not None:
            audiofile.tag.comments.set(__row[11])
        if __row[12] is not None:
            audiofile.tag.publisher = __row[12]
        if __row[13] is not None:
            audiofile.tag.lyrics.set(__row[13])
        print(u'Metadata of this file : ')
        audiofile.tag.save(version=(2, 3, 0))

def show_Tags_Column(tag):
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
    print(u'{:12} : {} MiB'.format('File Size', tag[16]))
    print(u'{:12} : {}'.format('Path', tag[17]))
    #print(u'{:12} : {}'.format('Extention', tag[18]))
    print(u'{:12} : {}'.format('Created', tag[19]))
    print(u'{:12} : {}'.format('Modified', tag[20]))
    print(u'------------------------------------')

def show_Tags_Row(tag):
    #get_logger('MD3Logger Start Showing all Tags of Eyed3 Song Object', 'MD3Logger', 'DEBUG')
    print(u'{:25} | {:25} | {:25} | {:25} | {:25}'.format(
        'Artist(s)', 'Title', 'Album', 'Album Artist', 'Date'))
    print(u'{:25} | {:25} | {:25} | {:25} | {:25}'.format(
        tag[1], tag[2], tag[3], tag[4], tag[9]))
    """
    print(u'{:12} : {:04.2f} MiB'.format( float(tag[16])))
    print(u'{:12} : {}'.format('Path', tag[17]))
    #print(u'{:12} : {}'.format('Extention', tag[18]))
    """

    print(u'------------------------------------')

def get_Tags(f):
    import time, os
    #get_logger('MD3Logger Start Get all Metadata of MP3 file', 'MD3Logger', 'DEBUG')
    #print(f)

    print(f)

    try:
        __tags = eyed3.core.load(f)
    except OSError as err:
        print("OS Error: {0}".format(err))
        md3.main()
    except FileNotFoundError as fnferr:
        print('fnferr')
        md3.main()
    else:
        print('are')

    __path =''.join((os.path.dirname(f), '/'))
    __mtime = time.strftime("%Y/%m/%d %a - %H:%M:%S", time.localtime(
                os.path.getmtime(f)))
    __ctime = time.strftime("%Y/%m/%d %a - %H:%M:%S", time.localtime(
                os.path.getctime(f)))
    __id3version = str(__tags.tag.version[0]) + '.' + str(
                __tags.tag.version[1])

    if len(__tags.tag.comments) > 0:
        __comm = __tags.tag.comments[0].text
        __commlang = __tags.tag.comments[0].lang
    else:
        __comm = ''

    if len(__tags.tag.lyrics) > 0:
        __lyric = __tags.tag.lyrics[0].text
        __lyriclang = __tags.tag.lyrics[0].lang
    else:
        __lyric = ''

    __tags = [
        os.path.basename(f), __tags.tag.artist, __tags.tag.title,
        __tags.tag.album, __tags.tag.album_artist, __tags.tag.track_num[0],
        __tags.tag.track_num[1], __tags.tag.disc_num[0], __tags.tag.disc_num[1],
        __tags.tag.release_date, __tags.tag.genre, __comm, __tags.tag.publisher,
        __lyric, __id3version, convert_unit(__tags.tag.header.tag_size, SIZE_UNIT.KiB),
        convert_unit(os.path.getsize(f), SIZE_UNIT.MiB), os.path.dirname(f) + "/", os.path.splitext(f)[1],
        __mtime, __ctime
        ]

    __tags = removeNone(__tags)
    return __tags

def makeCSVf(pf):
    import csv
    print(u'Creating New Music MetaData File ',pf)
    try:
        with open(pf, 'w', newline='') as csvfile:
            fieldnames = ['File Name','Artist', 'Title', 'Album', 'Album Artists', 'Track Number',
                'Totall Tracks', 'Disk Number', 'All Disks','Date', 'Gener', 'Comments',
                'Publisher','Lyrics', 'ID3 Version', 'Tag Size', 'Size (MiB)', 'Path',
                'Extention', 'Last Access',
                'Last Modify', 'CoverArt']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        csvfile.close()
    except IOError:
        print(u'Error: File {} Was Not Created.'.format(pf))
    else:
        print(u'File {} was created. and Header of CSV was added.'.format(pf))

    return True

def saveCSVf(pf, csvlist):
    import csv, os
    #get_logger('MD3Logger Start Save Tags in CSV file', 'MD3Logger', 'DEBUG')
    try:
        if not os.path.exists(pf):
            makeCSVf(pf)
        with open(pf, 'a', newline='') as __csvfile:
            for __row in csvlist:
                writer = csv.DictWriter(__csvfile, __row)
                writer.writeheader()
            print(u'The Tags Was writed to CSV file.')
        __csvfile.close()
    except IOError:
        print(u'File was not find.')
    else:
        print(u' -- CSV file Saved.')
    return True

def correctPath(self, csvlist):
    #get_logger('MD3Logger Start fix path of CSV file', 'MD3Logger', 'DEBUG')
    for __row in csvlist:
        __row[16] = ''.join((__row[16], '/'))
    return csvlist

def readCSVf(self, pf):
    import csv
    #get_logger('MD3Logger Start Read CSV file', 'MD3Logger', 'DEBUG')
    with open(pf) as __csvfile:
        __csvlist = csv.reader(__csvfile)
        return list(__csvlist)

def setAudioTags(self, f, tagName, tagText):
    __audiofile = eyed3.load(f)
    if (__audiofile.tag == None):
        __audiofile.initTag()

    __audiofile.tag.artist = ''

def removeNone(tags):
    #get_logger('MD3Logger Start Remove None Tags', 'MD3Logger', 'DEBUG')
    tags = list(map(str, tags))
    tags = [ __tag.replace('None', '') for __tag in tags ]
    return tags

def getMP3sTags(mp3s):
    #get_logger('MD3Logger Start Split MP3 files', 'MD3Logger', 'DEBUG')
    __SongsData = []

    for __f in mp3s:
        __tags = get_Tags(__f)
        __SongsData.append(__tags)
    return __SongsData

def splitCSVlist(self, csvlist):
    #get_logger('MD3Logger Start Split CSV file', 'MD3Logger', 'DEBUG')
    __mp3s = []
    for __row in csvlist:
        if __row[17] != 'Path':
            __fp = ''.join((__row[17], __row[0]))
            print('Read Tags Of {} File From CSV'.format(__fp))
            __mp3s.append(__fp)
    return __mp3s

