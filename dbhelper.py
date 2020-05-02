import sqlite3  

query = '''
CREATE TABLE Entries (
    Id       INTEGER      PRIMARY KEY AUTOINCREMENT
                          UNIQUE,
    name     STRING (250) NOT NULL,
    location STRING (250) NOT NULL,
    price    STRING (15)  NOT NULL,
    link     STRING (250) NOT NULL
);
'''

def InitializeDB(dbFileName):
    Error = None
    results = False
    try:
        db = CreateDBConnection(dbFileName=dbFileName)
        cursor = db.cursor()
        dbExists = cursor.execute("SELECT name FROM sqlite_master where name = 'Entries'")
        rows = len(dbExists.fetchall())
        db.commit()
        if rows < 1:
            queryResults = cursor.execute(query)
            rows = len(queryResults.fetchall())
            db.commit()
            results = True
        CloseDBConnection(db=db)
    except Error as error:
        print(error)
    return results

def CreateDBConnection(dbFileName):
    db = None
    Error = None
    try:
        db = sqlite3.connect(dbFileName)
    except Error as error:
        print(error)
    return db

def CloseDBConnection(db):
    Error = None
    try:
        db.close()
    except Error as error:
        print(error)

def SelectAllEntries(dbFileName):
    Error = None
    results = False
    try:
        if not InitializeDB(dbFileName=dbFileName):
            db = CreateDBConnection(dbFileName=dbFileName)
            cursor = db.cursor()
            queryResults = cursor.execute("SELECT * FROM Entries")
            rows = len(queryResults.fetchall())
            db.commit()
            CloseDBConnection(db=db)
            if rows > 0:
                results = True
    except Error as error:
        print(error)
    return results

def SelectOneEntry(dbFileName,entryLink):
    Error = None
    results = False
    try:
        if not InitializeDB(dbFileName=dbFileName):
            db = CreateDBConnection(dbFileName=dbFileName)
            cursor = db.cursor()
            queryResults = cursor.execute("SELECT * FROM Entries WHERE link =?", (entryLink,))
            rows = len(queryResults.fetchall())
            db.commit()
            CloseDBConnection(db=db)
            if rows > 0:
                results = True
    except Error as error:
        print(error)
    return results

def InsertEntry(dbFileName,entryName,entryLocation,entryPrice,entryLink):
    Error = None
    results = None
    try:
        if not InitializeDB(dbFileName=dbFileName):
            db = CreateDBConnection(dbFileName=dbFileName)
            cursor = db.cursor()
            results = cursor.execute("INSERT INTO Entries(name,location,price,link) VALUES(?,?,?,?)", (entryName,entryLocation,entryPrice,entryLink,))
            db.commit()
            CloseDBConnection(db=db)
    except Error as error:
        print(error)
    return results
