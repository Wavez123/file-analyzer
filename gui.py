import tkinter, file_parser, os, csv, hashlib, database_tools, sqlite3, re, logging, threading, json, sql_db_generator
from ttkbootstrap import Style
from csv import DictWriter
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
from logging import handlers

# [Logging]
logDir = os.path.normcase('.\\logs\\')

debug = True
if not os.path.exists(logDir):
    os.mkdir(logDir)
logfile = logDir + 'file-analyzer.log'

log = logging.getLogger('file-analyzer.log')
if debug:
    log.setLevel(logging.DEBUG)
else:
    log.setLevel(logging.INFO)
format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')

log_handler = handlers.TimedRotatingFileHandler(logfile, when='midnight', backupCount=10, utc=True)
log_handler.setFormatter(format)
log.addHandler(log_handler)

if debug:
    print = log.debug
else:
    print = log.info


# define a class for the app "window"
#class App(tkinter.Tk):
#    def __init__(self):
#        super().__init__()

# Variables
file_attr_list = []
global currentSelection
global currentName
currentSelection = None

window = tkinter.Tk()
window.title("Media Analyzer")
window.geometry("800x600")
style = Style(theme='flatly')

# Classes
class Table:
    def __init__(self, master, name, labels):
        self.master = master
        self.name = name
        self.labels = labels
        self.tree = ttk.Treeview(master, columns=labels, show="headings", height=10, selectmode="browse")
        self.tree.bind("<<TreeviewSelect>>", self.itemSelected)
        count = 0
        for heading in self.labels:
            self.tree.heading(count, anchor="w", text=heading)
            self.tree.column(count, anchor="w", width=70, stretch=False)
            count += 1

    def itemSelected(self, event):
        global currentSelection
        global currentName
        test = str(event.widget.selection())
        #tree.focus()
        #print tree.item(curItem)
        #print("test", test)
        buttonC.pack(side="top", expand=True)
        buttonD.pack(side="top", expand=True)
        buttonE.pack(side="top", expand=True)
        buttonF.pack(side="top", expand=True)
        for selected_item in self.tree.selection():
            print(self.name)
            item = self.tree.item(selected_item)
            record = list(item['values'])
            print("selected path: " + str(record))
            currentSelection = record[-3]
            currentName = record[-5]

    def fill(self, data):
        if type(data) == list:
                    self.tree.insert("","end",text="Listbox",values=(data),)
        elif type(data) == dict:
            self.tree.insert("","end",text="Listbox",values=(list(data.values())),)
            #item['title'],item['date'],item['extension'],'N/A',item['source'],item['quality'],item['name'],item['full_path'],item['size'],item['drive']
        else:
            listRow = []
            for row in data:
                listRow.append(row)
            self.tree.insert("","end",text="Listbox",values=(listRow,),)
    
    def delete_tree(self):
        self.tree.delete(*self.tree.get_children())

    def exportcsvfile():
    # export the selected table
        return None
        
    def delete_data():
        #find the selected row
        #delete the row from the table
        #delete the file from the file system
        return None

# Functions
def comparehash(sql_data, file_data):
    sql_data = hashlib.sha256(str(sql_data))
    file_data = hashlib.sha256(str(file_data))
    if sql_data == file_data:
        return True
    else:
        return False

#find path to scan and add to entry bar
def browseFolders():
    entry1.delete(0, tkinter.END)
    filename = filedialog.askdirectory(initialdir = "/", title = "Select a Folder to scan")
    # Change label contents
    entry1.insert(tkinter.END, filename)

def startup_fill_table():
    if os.path.exists('./media.db'):
        # import all tables from the database
        rendertogui('Movies', database_tools.fetchtable('MOVIES'))
        rendertogui('TV Shows', database_tools.fetchtable('TVSHOWS'))
        rendertogui('Music', database_tools.fetchtable('MUSIC'))
        rendertogui('Subtitles', database_tools.fetchtable('SUBTITLES'))
        rendertogui('Images', database_tools.fetchtable('IMAGES'))
        rendertogui('Books', database_tools.fetchtable('BOOKS'))
        rendertogui('Misc', database_tools.fetchtable('MISC'))
        # import all tables from the database
        # fill the GUI table with the data

def rendertogui(table, data):
    data = sorted(data, key=lambda x: x[0])

    if table == 'Movies':
        movietable.delete_tree()
    elif table == 'TV Shows':
        tvshowtable.delete_tree()
    elif table == 'Music':
        musictable.delete_tree()
    elif table == 'Subtitles':
        subtitlestable.delete_tree()
    elif table == 'Images':
        imagetable.delete_tree()
    elif table == 'Books':
        booktable.delete_tree()
    elif table == 'Misc':
        misctable.delete_tree()
        
    for item in data:
        if table == 'Movies':
            movietable.fill(item)
        elif table == 'TV Shows':
            tvshowtable.fill(item)
        elif table == 'Music':
            musictable.fill(item)
        elif table == 'Subtitles':
            subtitlestable.fill(item)
        elif table == 'Images':
            imagetable.fill(item)
        elif table == 'Books':
            booktable.fill(item)
        elif table == 'Misc':
            misctable.fill(item)

progressbar = ttk.Progressbar(mode="indeterminate", maximum=100)
def fill_tables(data):
    #first thing we need to do is iterate through the data and check for subtitles
    progress = 0
    for item in data:
        progress_step = float(100.0/len(data))
        progress += progress_step
        progress_var.set(progress)
        try:
            check = checkforsubtitles(item, data)
            if check is not None:
                item = check
        except Exception as e:
            pass

        #second thing we need to do is iterate through the data and check for duplicate files
        try:
            #need to add second check for data in the db
            check = checkforduplicates(item, data)
            if check is not None:
                item = check
        except Exception as e:
            pass
        
        try:
            database_tools.insert(item)
        except Exception as e:
            print(e)
            continue
        # next see if this has already been logged in the database, if so, update with new information
        # if not, insert the data
            #compare all values from current and former
            #data = {'mediatype': 'MOVIES', 'full_path': "Y:\Movies\Akira (1988)\Akira (1988) 1080p.mkv"}
            #print(previouslylogged(data))

        #third thing we need to do is add the data to the database
        #fourth thing we need to do is add the data to the GUI
        #try:
        #    rendertogui(item['mediatype'], database_tools.fetchtable(item['mediatype']))
        #except Exception as error:
        #    print(error)
    progress = 0
    progress_var.set(progress)
    progressbar.pack_forget()
    startup_fill_table()

def checkforsubtitles(media, list):
    pathlist = []
    for item in list:
        # if this is a movie or tv show we search the list for matching subtitles
        if media['mediatype'] == 'MOVIES' or media['mediatype'] == 'TVSHOWS':
            if media['title'] in item['title'] and item['mediatype'] == 'SUBTITLES':
                print("found subtitle for"+ media['filename'])
                if media['subtitles'] == "None":
                    media['subtitles'] = 1
                    pathlist.append(item['full_path'])
                else:
                    media['subtitles'] += 1
                    pathlist.append(item['full_path'])
    if pathlist == []:
        pathlist = "None"
    else:
        media['subtitles_list'] = str(pathlist)
    return media

def checkforduplicates(media, list):
    #need to fix this for TV Shows
    if media['mediatype'] == 'TVSHOWS':
        pathlist = []
        for item in list:
            # if this is a movie or tv show we search the list for matching duplicates
            filenamePattern = re.compile(media['filename'].lower())
            filenameMatch = re.fullmatch(filenamePattern, item['filename'].lower())
            basenamePattern = re.compile(os.path.splitext(os.path.basename(media['full_path']))[0].lower())
            basenameMatch = re.fullmatch(basenamePattern, os.path.splitext(os.path.basename(item['full_path']))[0].lower())
            showTitlePattern = re.compile(media['showtitle'].lower())
            showTitleMatch = re.fullmatch(showTitlePattern, item['showtitle'].lower())
            episodeTitlePattern = re.compile(media['episodetitle'].lower())
            episodeTitleMatch = re.fullmatch(episodeTitlePattern, item['episodetitle'].lower())
            
            # if basename match
            if basenameMatch and item['mediatype'] == media['mediatype'] and media['full_path'] != item['full_path']:
                print("found a possible dupe in "+ media['filename'])
                if media['duplicates'] == "None":
                    media['duplicates'] = 1
                    pathlist.append(item['full_path'])
                else:
                    media['duplicates'] += 1
                    pathlist.append(item['full_path'])
            
            # if filename match
            elif filenameMatch and item['mediatype'] == media['mediatype'] and media['full_path'] != item['full_path']:
                print("found a possible dupe in "+ media['filename'])
                if media['duplicates'] == "None":
                    media['duplicates'] = 1
                    pathlist.append(item['full_path'])
                else:
                    media['duplicates'] += 1
                    pathlist.append(item['full_path'])

            # if showtitle match and episodetitle match
            elif showTitleMatch and episodeTitleMatch and media['mediatype'] == item['mediatype'] and media['full_path'] != item['full_path']:
                print("found a possible dupe in "+ media['filename'])
                if media['duplicates'] == "None":
                    media['duplicates'] = 1
                    pathlist.append(item['full_path'])
                else:
                    media['duplicates'] += 1
                    pathlist.append(item['full_path'])
            
            # if showtitle match, date, season and episode match
            elif showTitleMatch and media['date'] == item['date'] and media['season'] == item['season'] and media['episode'] == item['episode'] and media['mediatype'] == item['mediatype'] and media['full_path'] != item['full_path']:
                print("found a possible dupe in "+ media['filename'])
                if media['duplicates'] == "None":
                    media['duplicates'] = 1
                    pathlist.append(item['full_path'])
                else:
                    media['duplicates'] += 1
                    pathlist.append(item['full_path'])

            # if showtitle match, season and episode match
            elif showTitleMatch and media['season'] == item['season'] and media['episode'] == item['episode'] and media['mediatype'] == item['mediatype'] and media['full_path'] != item['full_path']:
                print("found a possible dupe in "+ media['filename'])
                if media['duplicates'] == "None":
                    media['duplicates'] = 1
                    pathlist.append(item['full_path'])
                else:
                    media['duplicates'] += 1
                    pathlist.append(item['full_path'])
 
            # if showtitle match, date and episode match
            elif showTitleMatch and media['date'] == item['date'] and media['episode'] == item['episode'] and media['mediatype'] == item['mediatype'] and media['full_path'] != item['full_path']:
                print("found a possible dupe in "+ media['filename'])
                if media['duplicates'] == "None":
                    media['duplicates'] = 1
                    pathlist.append(item['full_path'])
                else:
                    media['duplicates'] += 1
                    pathlist.append(item['full_path'])      
        if pathlist == []:
            pathlist = "None"
        else:
            media['duplicates_list'] = str(pathlist)
        return media
    
    elif media['mediatype'] == 'MOVIES':
        pathlist = []
        for item in list:
            # if this is a movie or tv show we search the list for matching duplicates
            pattern = re.compile(media['title'])
            match = re.fullmatch(pattern, item['title'])
            if match and media['mediatype'] == item['mediatype'] and media['full_path'] != item['full_path']:
                print("found a possible dupe in "+ media['filename'])
                if media['duplicates'] == "None":
                    media['duplicates'] = 1
                    pathlist.append(item['full_path'])
                else:
                    media['duplicates'] += 1
                    pathlist.append(item['full_path'])
        if pathlist == []:
            pathlist = "None"
        else:
            media['duplicates_list'] = str(pathlist)
        return media
    else:
        if pathlist == []:
            pathlist = "None"
        else:
            media['duplicates_list'] = str(pathlist)
        return media
        
def scanFiles():
    file_list = []
    path = entry1.get()
    if path != "":
        for root, dirs, files in os.walk(path):
            for name in files:
                file_list.append(os.path.join(root, name))
        file_list.sort()
        progress = 0
        for file_path in file_list:
            progress_step = float(100.0/len(file_list))
            progress += progress_step
            progress_var.set(progress)
            file_info = file_parser.file_parser(file_path)
            media_info = file_parser.media_parser(file_path)
            new_dict = {**media_info, **file_info}
            file_attr_list.append(new_dict)

        #file_attr_list is a list of dictionaries
        fill_tables(file_attr_list)
        #fill_tbl(file_attr_list)

def previouslylogged(data):
    #if this file is in the csv file, and the fields match skip it
    try:
        data_dict = database_tools.fetchdata(data)
        return data_dict
    except:
        return None

#top frame
topframe = ttk.Frame(window)
bottomframe = ttk.Frame(window)

tabcontrol = ttk.Notebook(topframe)
movietab = ttk.Frame(tabcontrol)
subtitlestab = ttk.Frame(tabcontrol)
tvshowtab = ttk.Frame(tabcontrol)
musictab = ttk.Frame(tabcontrol)
booktab = ttk.Frame(tabcontrol)
imagetab = ttk.Frame(tabcontrol)
misctab = ttk.Frame(tabcontrol)

tabcontrol.add(movietab, text="Movies")
tabcontrol.add(subtitlestab, text="Subtitles")
tabcontrol.add(tvshowtab, text="TV Shows")
tabcontrol.add(musictab, text="Music")
tabcontrol.add(booktab, text="Books")
tabcontrol.add(imagetab, text="Images")
tabcontrol.add(misctab, text="Misc")

movielabels = ["Title", "Date", "Subtitles", "Duplicates", "Quality", "Source", "Extension", "Media Type", "Filename", "Full Path", "Size", "Drive"]
movietable = Table(movietab, "Movie", movielabels)
#print(tabcontrol.tab('current'))
movieverscrlbar = ttk.Scrollbar(movietab, orient='vertical', style='Vertical.TScrollbar', command=movietable.tree.yview)
moviehorscrlbar = ttk.Scrollbar(movietab, orient='horizontal', style='Horizontal.TScrollbar', command=movietable.tree.xview)

movietable.tree.configure(yscrollcommand=movieverscrlbar.set)
movietable.tree.configure(xscrollcommand=moviehorscrlbar.set)

tvshowlabels = ["Show Title", "Date", "Subtitles", "Duplicates", "Episode Title", "Episode", "Season", "Extension", "Media Type", "Source", "Resolution", "Filename", "Full Path", "Size", "Drive"]
tvshowtable = Table(tvshowtab, "TV Show", tvshowlabels)
tvshowverscrlbar = ttk.Scrollbar(tvshowtab, orient='vertical', style='Vertical.TScrollbar', command=tvshowtable.tree.yview)
tvshowhorscrlbar = ttk.Scrollbar(tvshowtab, orient='horizontal', style='Horizontal.TScrollbar', command=tvshowtable.tree.xview)

tvshowtable.tree.configure(yscrollcommand=tvshowverscrlbar.set)
tvshowtable.tree.configure(xscrollcommand=tvshowhorscrlbar.set)

musiclabels = ["Artist", "Album", "Genre", "Track", "Extension", "Year", "Media Type", "Filename", "Full Path", "Size", "Drive"]
musictable = Table(musictab, "Music", musiclabels)
musicverscrlbar = ttk.Scrollbar(musictab, orient='vertical', style='Vertical.TScrollbar', command=musictable.tree.yview)
musichorscrlbar = ttk.Scrollbar(musictab, orient='horizontal', style='Horizontal.TScrollbar', command=musictable.tree.xview)

musictable.tree.configure(yscrollcommand=musicverscrlbar.set)
musictable.tree.configure(xscrollcommand=musichorscrlbar.set)

sublabels = ["Title", "Language", "Extension", "Media Type", "Filename", "Full Path", "Size", "Drive"]
subtitlestable = Table(subtitlestab, "Subtitles", sublabels)
subtitlesverscrlbar = ttk.Scrollbar(subtitlestab, orient='vertical', style='Vertical.TScrollbar', command=subtitlestable.tree.yview)
subtitleshorscrlbar = ttk.Scrollbar(subtitlestab, orient='horizontal', style='Horizontal.TScrollbar', command=subtitlestable.tree.xview)

subtitlestable.tree.configure(yscrollcommand=subtitlesverscrlbar.set)
subtitlestable.tree.configure(xscrollcommand=subtitleshorscrlbar.set)

imagelabels = ["Title", "Extension", "Media Type", "Filename", "Full Path", "Size", "Drive"]
imagetable = Table(imagetab, "Image", imagelabels)
imageverscrlbar = ttk.Scrollbar(imagetab, orient='vertical', style='Vertical.TScrollbar', command=imagetable.tree.yview)
imagehorscrlbar = ttk.Scrollbar(imagetab, orient='horizontal', style='Horizontal.TScrollbar', command=imagetable.tree.xview)

imagetable.tree.configure(yscrollcommand=imageverscrlbar.set)
imagetable.tree.configure(xscrollcommand=imagehorscrlbar.set)

booklabels = ["Title", "Author", "Extension", "Media Type", "Filename", "Full Path", "Size", "Drive"]
booktable = Table(booktab, "Books", booklabels)
bookverscrlbar = ttk.Scrollbar(booktab, orient='vertical', style='Vertical.TScrollbar', command=booktable.tree.yview)
bookhorscrlbar = ttk.Scrollbar(booktab, orient='horizontal', style='Horizontal.TScrollbar', command=booktable.tree.xview)

booktable.tree.configure(yscrollcommand=bookverscrlbar.set)
booktable.tree.configure(xscrollcommand=bookhorscrlbar.set)

misclabels = ["Filename", "Media Type", "Extension", "Full Path", "Size", "Drive"]
misctable = Table(misctab, "Misc", misclabels)
miscverscrlbar = ttk.Scrollbar(misctab, orient='vertical', style='Vertical.TScrollbar', command=misctable.tree.yview)
mischorscrlbar = ttk.Scrollbar(misctab, orient='horizontal', style='Horizontal.TScrollbar', command=misctable.tree.xview)

misctable.tree.configure(yscrollcommand=miscverscrlbar.set)
misctable.tree.configure(xscrollcommand=mischorscrlbar.set)

def showFile():
    global currentSelection
    print("Opening " + currentSelection)
    path = currentSelection
    base = os.path.basename(path)
    path = path.replace(base, '')
    os.startfile(path)

def deleteFile():
    global currentSelection
    path = currentSelection
    warning = tkinter.messagebox.askokcancel(title="Delete File", message="Are you sure you want to delete " + path + "?",)
    if warning:
        print("Deleting " + currentSelection)
        os.remove(path)
        data = {'mediatype': currentName, 'full_path': currentSelection}
        database_tools.deletedata(data)
        startup_fill_table()
        tkinter.messagebox.showinfo(title="File Deleted", message="File " + path + " has been deleted")
    pass

def openFiles(path):
    os.startfile(path)

def threadOpenFile(path):
    thread = threading.Thread(target=openFiles, args=(path,))
    thread.daemon = True
    thread.start()

def showDuplicates():
    data = {'mediatype': currentName, 'full_path': currentSelection}
    duplicatesPaths = database_tools.fetchdata(data)
    duplicatesPaths = list(duplicatesPaths[0])
    duplicatesPaths = duplicatesPaths[5]
    duplicatesPaths = list(duplicatesPaths.split(","))
    print(type(duplicatesPaths))
    for path in duplicatesPaths:
        path = path.replace("\\", "/").replace("//", "/").replace("[", "").replace("]", "").replace("'", "")
        path = re.sub('^ ', '', path)
        base = os.path.basename(path)
        print("Opened " + path)
        path = path.replace(base, '')
        threadOpenFile(path)
        

def showSubtitles():
    data = {'mediatype': currentName, 'full_path': currentSelection}
    subtitlesPaths = database_tools.fetchdata(data)
    subtitlesPaths = list(subtitlesPaths[0])
    subtitlesPaths = subtitlesPaths[5]
    subtitlesPaths = list(subtitlesPaths.split(","))
    print(type(subtitlesPaths))
    for path in subtitlesPaths:
        path = path.replace("\\", "/").replace("//", "/").replace("[", "").replace("]", "").replace("'", "")
        path = re.sub('^ ', '', path)
        base = os.path.basename(path)
        print("Opened " + path)
        path = path.replace(base, '')
        threadOpenFile(path)

def threadWipeDB():
    thread = threading.Thread(target=wipeDB)
    thread.daemon = True
    thread.start()

def wipeDB():
    warning = tkinter.messagebox.askokcancel(title="Delete Database", message="Are you sure you want to delete the entire database? \n This won't delete the original files.",)
    if warning:
        sql_db_generator.wipe()
        startup_fill_table()
    pass

def threadExport():
    thread = threading.Thread(target=showExport)
    thread.daemon = True
    thread.start()

def showExport():
    #top frame Export
    exportWindow = tkinter.Toplevel(window)
    exportWindow.title("Export")
    exportWindow.geometry("400x300")

    exportLabel = ttk.Label(exportWindow, text="Export")
    exportLabel.pack(side="top", anchor="n", padx=10, pady=10)
    exportFormat = ttk.Combobox(exportWindow, values=["CSV", "JSON"])
    exportFormat.pack(side="top", anchor="n", padx=10, pady=10)
    exportSelection = ttk.Combobox(exportWindow, values=["ALL", "MOVIES", "SUBTITLES", "TVSHOWS", "MUSIC", "BOOKS", "IMAGES", "MISC"])
    exportSelection.pack(side="top", anchor="n", padx=10, pady=10)
    exportExecuteButton = ttk.Button(exportWindow, text="Execute", command=lambda: export(exportFormat.get(), exportSelection.get()))
    exportExecuteButton.pack(side="top", anchor="n", padx=10, pady=10)

def export(format, table):
    print(format, table)
    if table == "ALL":
        for table in ["MOVIES", "SUBTITLES", "TVSHOWS", "MUSIC", "BOOKS", "IMAGES", "MISC"]:
            if format == "CSV":
                savepath = filedialog.asksaveasfilename(filetypes = [('All tyes(*.*)', '*.*'),("csv file(*.csv)","*.csv")], defaultextension = [('All tyes(*.*)', '*.*'),("csv file(*.csv)","*.csv")], initialfile = table+".csv")
                exportToCSV(table, savepath)
            elif format == "JSON":
                savepath = filedialog.asksaveasfilename(filetypes = [('All tyes(*.*)', '*.*'),("json file(*.json)","*.json")], defaultextension = [('All tyes(*.*)', '*.*'),("json file(*.json)","*.json")], initialfile = table+".json")
                exportToJSON(table, savepath)
    elif format == "CSV":
        savepath = filedialog.asksaveasfilename(filetypes = [('All tyes(*.*)', '*.*'),("csv file(*.csv)","*.csv")], defaultextension = [('All tyes(*.*)', '*.*'),("csv file(*.csv)","*.csv")], initialfile = table+".csv")
        exportToCSV(table, savepath)
    elif format == "JSON":
        savepath = filedialog.asksaveasfilename(filetypes = [('All tyes(*.*)', '*.*'),("json file(*.json)","*.json")], defaultextension = [('All tyes(*.*)', '*.*'),("json file(*.json)","*.json")], initialfile = table+".json")
        exportToJSON(table, savepath)
        #tableSelection = table

def exportToCSV(table, output_file):
    connection = sqlite3.connect('./media.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM "+table)
    with open(output_file, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="\t")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
    connection.close()
    base = os.path.basename(output_file)
    print("Opened " + output_file)
    path = output_file.replace(base, '')
    threadOpenFile(path)

def exportToJSON(table, output_file):
    connection = sqlite3.connect('./media.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM "+table)
    results = cursor.fetchall()
    results = json.dumps(results)
    with open(output_file, "w") as json_file:
        json_file.write(results)
    connection.close()
    base = os.path.basename(output_file)
    print("Opened " + output_file)
    path = output_file.replace(base, '')
    threadOpenFile(path)

def threadScanFiles():
    progressbar.pack(side="top", expand=True, fill="x")
    thread = threading.Thread(target=scanFiles)
    thread.daemon = True
    thread.start() 

# Adding light and dark mode images 
light = tkinter.PhotoImage(file="light.png") 
dark = tkinter.PhotoImage(file="dark.png") 
  
switch_value = True
  
# Defining a function to toggle 
# between light and dark theme 
def toggle(): 
  
    global switch_value 
    if switch_value == True: 
        switch.config(image=light)
        style = Style(theme='solar')       
        # Changes the window to dark theme   
        switch_value = False
  
    else: 
        switch.config(image=dark)

        style = Style(theme='flatly')
        # Changes the window to light theme
        switch_value = True
  
  
# Creating a button to toggle 
# between light and dark themes 
switch = tkinter.Button(bottomframe, image=dark, width=50, height=25, bd=0, bg="white", activebackground="white", command=toggle)

#top entry bar
progress_var = tkinter.DoubleVar()
progressbar = ttk.Progressbar(bottomframe, variable=progress_var, maximum=100)
#label1 = tkinter.Label(bottomframe, font=("Arial", 14))
buttonC = tkinter.Button(bottomframe, text="Show Duplicates", command=showDuplicates, padx=5, pady=5)
buttonD = tkinter.Button(bottomframe, text="Show Subtitles", command=showSubtitles, padx=5, pady=5)
buttonE = tkinter.Button(bottomframe, text="Show File", command=showFile, padx=5, pady=5)
buttonF = tkinter.Button(bottomframe, text="Delete File", command=deleteFile, padx=5, pady=5)

entry1 = tkinter.Entry(bottomframe, font=("Arial", 12))
buttonA = tkinter.Button(bottomframe, text="Select Folder", command=browseFolders)
buttonB = tkinter.Button(bottomframe, text="Scan Files", command=threadScanFiles)

buttonExport = tkinter.Button(bottomframe, text="Export", command=threadExport, height=1)
buttonWipeDB = tkinter.Button(bottomframe, text="Wipe DB", command=threadWipeDB, height=1)

#top frame
moviehorscrlbar.pack(side='bottom', fill='x')
movieverscrlbar.pack(side='right', fill='y')
movietable.tree.pack(side="left", expand=True, fill="both")

tvshowhorscrlbar.pack(side='bottom', fill='x')
tvshowverscrlbar.pack(side='right', fill='y')
tvshowtable.tree.pack(side="left", expand=True, fill="both")

musichorscrlbar.pack(side='bottom', fill='x')
musicverscrlbar.pack(side='right', fill='y')
musictable.tree.pack(side="left", expand=True, fill="both")

subtitleshorscrlbar.pack(side='bottom', fill='x')
subtitlesverscrlbar.pack(side='right', fill='y')
subtitlestable.tree.pack(side="left", expand=True, fill="both")

imagehorscrlbar.pack(side='bottom', fill='x')
imageverscrlbar.pack(side='right', fill='y')
imagetable.tree.pack(side="left", expand=True, fill="both")

bookhorscrlbar.pack(side='bottom', fill='x')
bookverscrlbar.pack(side='right', fill='y')
booktable.tree.pack(side="left", expand=True, fill="both")

miscverscrlbar.pack(side='bottom', fill='x')
miscverscrlbar.pack(side='right', fill='y')
misctable.tree.pack(side="left", expand=True, fill="both")

tabcontrol.pack(expand=True, fill="both")
topframe.pack(anchor="n", expand=True, fill="both")

#bottomlayout
switch.pack(side="left", expand=True, anchor='w', pady=18)
buttonExport.pack(side="left", expand=True, padx=10, pady=16)
buttonWipeDB.pack(side="left", expand=True, padx=10, pady=16)
entry1.pack(side="top", expand=True, fill="y", padx=10, pady=5)
buttonA.pack(side="left", expand=True, padx=10, pady=5)
buttonB.pack(side="left", expand=True, padx=10, pady=5)

bottomframe.pack(side="bottom")

#importcsvfile()
startup_fill_table()
# last know good
#connection = sqlite3.connect('./media.db')
#cursor = connection.cursor()
#cursor.execute("SELECT * FROM MOVIES WHERE Full_Path Like'Y:\Movies\Akira (1988)\Akira (1988) 1080p.mkv'")
#data = cursor.fetchall()
#connection.close()
#print(data)
window.mainloop()
