import sqlite3

# This function is used to insert data into the database with a specific table name
# and specific parameter and value
def insert(data):
    connection = sqlite3.connect('./media.db')
    cursor = connection.cursor()
    list_data = list(data.values())
    if data['mediatype'] == 'MOVIES':
        cursor.execute("INSERT INTO "+data['mediatype']+" VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", list_data)
    elif data['mediatype'] == 'TVSHOWS':
        cursor.execute("INSERT INTO "+data['mediatype']+" VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", list_data)
    elif data['mediatype'] == 'MUSIC':
        cursor.execute("INSERT INTO "+data['mediatype']+" VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)", list_data)
    elif data['mediatype'] == 'SUBTITLES':
        cursor.execute("INSERT INTO "+data['mediatype']+" VALUES (NULL,?,?,?,?,?,?,?,?)", list_data)
    elif data['mediatype'] == 'IMAGES':
        cursor.execute("INSERT INTO "+data['mediatype']+" VALUES (NULL,?,?,?,?,?,?,?)", list_data)
    elif data['mediatype'] == 'BOOKS':
        cursor.execute("INSERT INTO "+data['mediatype']+" VALUES (NULL,?,?,?,?,?,?,?,?)", list_data)
    elif data['mediatype'] == 'MISC':
        cursor.execute("INSERT INTO "+data['mediatype']+" VALUES (NULL,?,?,?,?,?,?,?)", list_data)
    connection.commit()
    connection.close()

# This function is used to fetch data from the database with a specific table name
# and specific parameter and value
# return a list of the data

def fetchdata(data):
    connection = sqlite3.connect('./media.db')
    cursor = connection.cursor()
    #print("SELECT * FROM "+data['mediatype']+" WHERE Full_Path Like "+"\""+data['full_path']+"\"")
    cursor.execute("SELECT * FROM "+data['mediatype']+" WHERE Full_Path Like "+"\""+data['full_path']+"\"")
    data = cursor.fetchall()
    connection.close()
    #print("previous: ",data)
    return data

def deletedata(data):
    connection = sqlite3.connect('./media.db')
    cursor = connection.cursor()
    #print("SELECT * FROM "+data['mediatype']+" WHERE Full_Path Like "+"\""+data['full_path']+"\"")
    try:
        cursor.execute("DELETE FROM "+data['mediatype']+" WHERE Full_Path Like "+"\""+data['full_path']+"\"")
        connection.close()
        #print("previous: ",data)
        return True
    except Exception as e:
        print(e)
        return False

def fetchTableAll(table):
    connection = sqlite3.connect('./media.db')
    cursor = connection.cursor()
    return cursor.execute("SELECT * FROM "+table)

# This function is used to fetch data from the database with a specific table name
# it returns a list of lists
def fetchtable(table):
    connection = sqlite3.connect('./media.db')
    cursor = connection.cursor()
    # need to fetch all tables from the database
    # fill the GUI table with the data
    if table == 'MOVIES':
        cursor.execute("SELECT Title, Date, Subtitles, Duplicates, Quality, Source, Extension, Media_Type, Filename, Full_Path, Size, Drive FROM "+table)
    elif table == 'TVSHOWS':
        #"Show Title", "Date", "Subtitles", "Duplicates", "Episode Title", "Episode", "Season", "Extension", "Media Type", "Source", "Resolution", "Filename", "Full Path", "Size", "Drive"
        cursor.execute("SELECT Show_Title, Date, Subtitles, Duplicates, Episode_Title, Episode, Season, Extension, Media_Type, Source, Quality, Filename, Full_Path, Size, Drive FROM "+table)
    elif table == 'MUSIC':
        cursor.execute("SELECT Artist, Album, Genre, Track, Extension, Year, Media_Type, Filename, Full_Path, Size, Drive FROM "+table)
    elif table == 'SUBTITLES':
        cursor.execute("SELECT Title, Language, Extension, Media_Type, Filename, Full_Path, Size, Drive FROM "+table)
    elif table == 'IMAGES':
        cursor.execute("SELECT Title, Extension, Media_Type, Filename, Full_Path, Size, Drive FROM "+table)
    elif table == 'BOOKS':
        cursor.execute("SELECT Title, Author, Extension, Media_Type, Filename, Full_Path, Size, Drive FROM "+table)
    elif table == 'MISC':
        cursor.execute("SELECT Filename, Media_Type, Extension, Full_Path, Size, Drive FROM "+table)
    #this is a tuple
    table = cursor.fetchall()
    #this is a list
    listRow = []
    #for each item in the tuple convert it to a list and add it to the main list
    for row in table:
        row = list(row)
        listRow.append(row)
    #return the list
    connection.close()
    #print("fetched: ",listRow)
    return listRow
