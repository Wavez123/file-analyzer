import sqlite3
def wipe():
    # Connecting to sqlite
    # connection object
    connection_obj = sqlite3.connect('.\media.db')
    
    # cursor object
    cursor_obj = connection_obj.cursor()
    
    # Drop the MOVIES table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS MOVIES")

    #"Title","Date","Subtitles","Quality","Source","Extension","Media Type","Filename","Full Path","Size","Drive"
    # Creating Movie Table
    table = """ CREATE TABLE MOVIES (
                ID INT PRIMARY KEY,
                Title VARCHAR(255) NOT NULL,
                Date VARCHAR(255) NOT NULL,
                Subtitles INT NOT NULL,
                Duplicates INT NOT NULL,
                Subtitles_List VARCHAR(255) NOT NULL,
                Duplicates_List VARCHAR(255) NOT NULL,
                Quality VARCHAR(255) NOT NULL,
                Source VARCHAR(255) NOT NULL,
                Media_Type VARCHAR(255) NOT NULL,
                Filename VARCHAR(255) NOT NULL,
                Full_Path VARCHAR(255) NOT NULL UNIQUE,
                Extension VARCHAR(255) NOT NULL,
                Size VARCHAR(255) NOT NULL,
                Drive VARCHAR(255) NOT NULL
            ); """
    
    cursor_obj.execute(table)

    # Drop the TVSHOWS table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS TVSHOWS")

    #"Show Title","Date","Subtitles","Media Type","Episode Title","Episode","Season","Extension","Source","Resolution","Filename","Full Path","Size","Drive"
    # Creating TVSHOWS Table
    # "Show Title", "Date", "Subtitles", "Duplicates", "Episode Title", "Episode", "Season", "Extension", "Media Type", "Source", "Resolution", "Filename", "Full Path", "Size", "Drive"
    table = """ CREATE TABLE TVSHOWS (
                ID INT PRIMARY KEY,
                Title VARCHAR(255) NOT NULL,
                Show_Title VARCHAR(255) NOT NULL,
                Date VARCHAR(255) NOT NULL,
                Subtitles INT NOT NULL,
                Duplicates INT NOT NULL,
                Subtitles_List VARCHAR(255) NOT NULL,
                Duplicates_List VARCHAR(255) NOT NULL,
                Episode_Title VARCHAR(255) NOT NULL,
                Episode INT NOT NULL,
                Season INT NOT NULL,
                Media_Type VARCHAR(255) NOT NULL,
                Source VARCHAR(255) NOT NULL,     
                Quality VARCHAR(255) NOT NULL,
                Filename VARCHAR(255) NOT NULL,
                Full_Path VARCHAR(255) NOT NULL UNIQUE,
                Extension VARCHAR(255) NOT NULL,
                Size VARCHAR(255) NOT NULL,
                Drive VARCHAR(255) NOT NULL
            ); """
    
    cursor_obj.execute(table)

    # Drop the MUSIC table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS MUSIC")

    #"Artist","Album","Genre","Track","Extension","Year","Media Type","Filename","Full Path","Size","Drive"
    # Creating MUSIC Table
    table = """ CREATE TABLE MUSIC (
                ID INT PRIMARY KEY,
                Artist VARCHAR(255) NOT NULL,
                Album VARCHAR(255) NOT NULL,
                Genre VARCHAR(255) NOT NULL,
                Track INT NOT NULL,
                Year INT NOT NULL,
                Media_Type VARCHAR(255) NOT NULL,
                Filename VARCHAR(255) NOT NULL,
                Full_Path VARCHAR(255) NOT NULL UNIQUE,
                Extension VARCHAR(255) NOT NULL,
                Size VARCHAR(255) NOT NULL,
                Drive VARCHAR(255) NOT NULL
            ); """
    
    cursor_obj.execute(table)

    # Drop the SUBTITLES table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS SUBTITLES")

    #"Title","Language","Extension","Media Type","Filename","Full Path","Size","Drive"
    # Creating SUBTITLES Table
    table = """ CREATE TABLE SUBTITLES (
                ID INT PRIMARY KEY,
                Title VARCHAR(255) NOT NULL,
                Language VARCHAR(255) NOT NULL,
                Media_Type VARCHAR(255) NOT NULL,
                Filename VARCHAR(255) NOT NULL,
                Full_Path VARCHAR(255) NOT NULL UNIQUE,
                Extension VARCHAR(255) NOT NULL,
                Size VARCHAR(255) NOT NULL,
                Drive VARCHAR(255) NOT NULL
            ); """
    
    cursor_obj.execute(table)

    # Drop the IMAGES table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS IMAGES")

    #"Title","Language","Extension","Media Type","Filename","Full Path","Size","Drive"
    # Creating IMAGES Table
    table = """ CREATE TABLE IMAGES (
                ID INT PRIMARY KEY,
                Title VARCHAR(255) NOT NULL,
                Media_Type VARCHAR(255) NOT NULL,
                Filename VARCHAR(255) NOT NULL,
                Full_Path VARCHAR(255) NOT NULL UNIQUE,
                Extension VARCHAR(255) NOT NULL,
                Size VARCHAR(255) NOT NULL,
                Drive VARCHAR(255) NOT NULL
            ); """
    
    cursor_obj.execute(table)

    # Drop the BOOKS table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS BOOKS")

    #"Title","Author","Extension","Media Type","Filename","Full Path","Size","Drive"
    # Creating BOOKS Table
    table = """ CREATE TABLE BOOKS (
                ID INT PRIMARY KEY,
                Title VARCHAR(255) NOT NULL,
                Author VARCHAR(255) NOT NULL,
                Media_Type VARCHAR(255) NOT NULL,
                Filename VARCHAR(255) NOT NULL,
                Full_Path VARCHAR(255) NOT NULL UNIQUE,
                Extension VARCHAR(255) NOT NULL,
                Size VARCHAR(255) NOT NULL,
                Drive VARCHAR(255) NOT NULL
            ); """
    
    cursor_obj.execute(table)

    # Drop the MISC table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS MISC")

    #"Filename","Extension","Full Path","Size","Drive"
    # Creating MISC Table
    table = """ CREATE TABLE MISC (
                ID INT PRIMARY KEY,
                Title VARCHAR(255) NOT NULL,
                Media_Type VARCHAR(255) NOT NULL,
                Filename VARCHAR(255) NOT NULL,
                Full_Path VARCHAR(255) NOT NULL UNIQUE,
                Extension VARCHAR(255) NOT NULL,
                Size VARCHAR(255) NOT NULL,
                Drive VARCHAR(255) NOT NULL
            ); """
    
    cursor_obj.execute(table)

    print("Table is Ready")
    
    # Close the connection
    connection_obj.close()
