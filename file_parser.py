import os, platform, pathlib, re, glob, csv
# need to make a function that accepts a file path
def path_parser(file_path):
    files_list = []
    for root, dirs, files in os.walk(file_path):
        for name in files:
            files_list.append(os.path.join(root, name))
    return files_list

# need to parse the files for attributes such as file size, file type, etc
    # size
    # type
    # name
    # extension
    # fullpath
class file_info(object):
    def __init__(self, filename, full_path, extension, size, drive):
        self.filename = filename
        self.full_path = full_path
        self.extension = extension
        self.size = size
        self.drive = drive

def file_parser(file_path):
    file = file_info(os.path.basename(file_path), file_path.replace('/', '\\').replace('\\\\', '\\'), os.path.splitext(file_path)[1], maths(os.stat(file_path).st_size), os.path.splitdrive(file_path)[0])
    print("Processing Title:", file.filename)
    return vars(file)

def maths(size):
    if size < 1024:
        return str(size) + " B"
    elif size < 1048576:
        return str(round(size / 1024, 2)) + " KB"
    elif size < 1073741824:
        return str(round(size / 1048576, 2)) + " MB"
    else:
        return str(round(size / 1073741824, 2)) + " GB"
    
# need to parse the name for name, episode number, season number, resolution, etc
def media_parser(file_path):
    movie = False
    tvshow = False
    music = False
    book = False
    subtitle = False
    image = False
    # figure out the type of media this file is and parse it
    if os.path.splitext(file_path)[1] == '.mp4' or os.path.splitext(file_path)[1] == '.mkv' or os.path.splitext(file_path)[1] == '.avi' or os.path.splitext(file_path)[1] == '.mkv' or os.path.splitext(file_path)[1] == '.m4v' or os.path.splitext(file_path)[1] == '.mov':
        for parent in pathlib.Path(file_path).parents:
            parent_string = str(parent)
            if "Movies" in parent_string:
                movie = True
            elif "TV Shows" in parent_string:
                tvshow = True
    elif os.path.splitext(file_path)[1] == '.mp3':
        music = True
    elif os.path.splitext(file_path)[1] == '.pdf' or os.path.splitext(file_path)[1] == '.pub' or os.path.splitext(file_path)[1] == '.epub':
        book = True
    elif os.path.splitext(file_path)[1] == '.srt':
        subtitle = True
    elif os.path.splitext(file_path)[1] == '.png' or os.path.splitext(file_path)[1] == '.jpg' or os.path.splitext(file_path)[1] == '.jpeg' or os.path.splitext(file_path)[1] == '.bmp':
        image = True
    else:
        print("Unsorted Media Type")

    if movie:
        title = os.path.splitext(os.path.basename(file_path))[0]
        try:
            search = re.findall(r"[(]\d{4}[)]|[[]\d{4}[]]|[[]\d{4}[.]|\d{4}[.]|[[]\d{4}\s|\d{4}\s", file_path)
            date = search[-1]
            title = title.replace(date, '')
            date = date.replace('[', '')
            date = date.replace(']', '')
            date = date.replace('(', '')
            date = date.replace(')', '')
        except:
            date = "No Date Entry"

        try:
            search = re.search('(1080p)|(720p)|(480p)|(4k)|(576p)|(HDTV)|(2160p)', file_path)
            quality = search.group()
            title = title.replace(quality, '')
        except:
            quality = "No Quality Entry"
        
        try:
            search = re.search('(BluRay)|(Dvdrip)|(WEB)|(Web Rip)|(DVD)|(BDRip)|(Brrip)|(BRrip)|(HDrip)', file_path)
            source = search.group()
            title = title.replace(source, '')
        except:
            source = "No Source Entry"

        title = os.path.splitext(os.path.basename(file_path))[0]

        return { 'title': title, 'date': date, 'subtitles': "None", 'duplicates':"None", 'subtitles_list': "None", 'duplicates_list': "None", 'quality': quality, 'source': source, 'mediatype': 'MOVIES' }
    elif tvshow:
        title = os.path.splitext(os.path.basename(file_path))[0]
        try:
            search = re.findall('[(]\d{4}[)]|[[]\d{4}[]]|[[]\d{4}[.]|\d{4}[.]|[[]\d{4}\s|\d{4}\s', title)
            date = search[-1]
            title = title.replace(date, '')
            date = date.replace('[', '')
            date = date.replace(']', '')
            date = date.replace('(', '')
            date = date.replace(')', '')
        except:
            try:
                search = re.search('[(]\d{4}[)]|[[]\d{4}[]]|[[]\d{4}[.]|\d{4}[.]|[[]\d{4}\s|\d{4}\s', file_path)
                date = search.group()
                title = title.replace(date, '')
                date = date.replace('[', '')
                date = date.replace(']', '')
                date = date.replace('(', '')
                date = date.replace(')', '')
            except:
                date = "No Date Entry"
        
        try:
            search = re.search('(1080p)|(720p)|(480p)|(\[480p\])|(4k)|(576p)|(HDTV)|(2160p)', title)
            quality = search.group()
            title = title.replace(quality, '')
            #101 Dalmatians The Series S01E01 Home is Where the Bark Is 
        except:
            quality = "No Quality Entry"

        try:
            search = re.search('(BluRay)|(Dvdrip)|(WEB)|(Web Rip)|(DVD)|(BDRip)|(Brrip)|(BRrip)|(HDrip)', title)
            source = search.group()
            title = title.replace(source, '')
            #101 Dalmatians The Series S01E01 Home is Where the Bark Is 
        except:
            source = "No Source Entry"
        #find the season and episode
        try:
            search = re.search('[sS]\d{2}|[sS] \d{2}|[sS][eE]\d{2}|[sS][eE] \d{2}|([sS]eason)\d+|([sS]eason) \d+', title)
            if search.group() == '/d[x]/d+':
                season = search.group().split('x')[0]
                episode = search.group().split('x')[1]
                title = title.replace(search.group(), '~')
            elif search.group() != None:
                season = search.group()
                title = title.replace(search.group(), '~')
                search = re.search('[eE][pP]\d+|[eE][pP] \d+|[eE]\d+|[eE] \d+|[eE][pP][.] \d+|[eE][pP][.]\d+|(Episode)\W\d{2}', title)
                episode = search.group()
                title = title.replace(search.group(), '')
                try:
                    search = re.search('[-][eE][pP]\d+|[-][eE][pP] \d+|[-][eE]\d+|[-][eE] \d+|[-][eE][pP][.] \d+|[-][eE][pP][.]\d+|[-](Episode)\W\d{2}', title)
                    if search.group() != None:
                        episode += search.group()
                        title = title.replace(search.group(), '')
                except:
                    pass
        except:
            try:
                search = re.search('[eE][pP]\d+|[eE][pP] \d+|[eE]\d+|[eE] \d+|[eE][pP][.] \d+|[eE][pP][.]\d+|(Episode)\W\d{2}', title)
                if search.group() != None:
                    episode = search.group()
                    title = title.replace(search.group(), '~')
                    search = re.search('[sS]\d{2}|[sS] \d{2}|[sS][eE]\d{2}|[sS][eE] \d{2}|([sS]eason)\d+|([sS]eason) \d+', file_path)
                    if search.group() != None:
                        season = search.group()
            except:
                season = "No Season Entry"
                episode = "No Episode Entry"

        try:
            showtitle = title.split('~')[0]
            episodetitle = title.split('~')[1]
            showtitle = showtitle.replace('.* - $', '')
            episodetitle = episodetitle.replace('^ - ', '')
            #print("Title: " + title + " Showtitle: " + showtitle + " Episodetitle: " + episodetitle)
            # S01E01 Home is Where the Bark Is 
        except:
            showtitle = "No Show Title Entry"
            episodetitle = "No Episode Title Entry"
            # need to find a method of parsing the show title from the file path parent

        title = os.path.splitext(os.path.basename(file_path))[0]

            #"Show Title", "Date", "Subtitles", "Duplicates", "Episode Title", "Episode", "Season", "Extension", "Media Type", "Source", "Resolution", "Filename", "Full Path", "Size", "Drive"
        return { 'title': title, 'showtitle': showtitle, 'date': date, 'subtitles': "None", 'duplicates': "None", 'subtitles_list': "None", 'duplicates_list': "None", 'episodetitle': episodetitle, 'episode': episode, 'season': season, 'mediatype': 'TVSHOWS', 'source': source, 'quality': quality}
    elif image:
        title = os.path.basename(file_path)
        return { 'title': title, 'mediatype': 'IMAGES'}
    elif subtitle:
        title = (os.path.splitext(os.path.basename(file_path))[0]).split('.')[0]
        try:
            search = re.findall(r"[(]\d{4}[)]|[[]\d{4}[]]|[[]\d{4}[.]|\d{4}[.]|[[]\d{4}\s|\d{4}\s", file_path)
            date = search[-1]
            title = title.replace(date, '')
            date = date.replace('[', '')
            date = date.replace(']', '')
            date = date.replace('(', '')
            date = date.replace(')', '')
        except:
            pass
        try:
            language = (os.path.splitext(os.path.basename(file_path))[0]).split('.')[1]
        except:
            language = "No Language Entry"
        return { 'title': title, 'language': language, 'mediatype': 'SUBTITLES' }
    elif music:
        try:
            album = file_path.split('/')[-2]
        except:
            album = "No Album Entry"
        try:
            artist = file_path.split('/')[-3]
        except:
            artist = "No Artist Entry"
        genre = 'N/A'
        track = (os.path.splitext(os.path.basename(file_path))[0]).split('.')[0]

        try:
            search = re.findall(r"[(]\d{4}[)]|[[]\d{4}[]]|[[]\d{4}[.]|\d{4}[.]|[[]\d{4}\s|\d{4}\s", file_path)
            date = search[-1]
            title = title.replace(date, '')
            date = date.replace('[', '')
            date = date.replace(']', '')
            date = date.replace('(', '')
            date = date.replace(')', '')
        except:
            date = "No Date Entry"
        return { 'Artist': artist, 'Album': album, 'Genre': genre,'track': track, 'Year': date, 'mediatype': 'MUSIC' }
    elif book:   
        title = (os.path.splitext(os.path.basename(file_path))[0]).split('.')[0]
        if "by" in title:
            author = title.split('by')[1]
            title = title.split('by')[0]
        elif "-" in title:
            author = title.split('-')[0]
            title = title.split('-')[1]
        else:
            author = "No Author Entry"
        return { 'title': title, 'author': author, 'mediatype': 'BOOKS' }
    else:
        title = os.path.basename(file_path)
        return { 'title': title , 'mediatype': 'MISC' }
