import sqlite3
import datetime
from datetime import datetime

databaseName = 'dataBase.db'


def create_tables():
    connect = sqlite3.connect(databaseName)
    cursor = connect.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Library(ID INTEGER,'
                   'Name TEXT,'
                   'Author TEXT,'
                   'Year INTEGER,'
                   'Count INTEGER,'
                   'OnHandsCount INTEGER,'
                   'CountTakes INTEGER,'
                   'AllTime INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS NotInLibrary(ID INTEGER,'
                   'Name TEXT,'
                   'Author TEXT,'
                   'Year INTEGER,'
                   'takeID INTEGER,'
                   'timeTake TEXT,'
                   'takerID INTEGER)')
    connect.commit()


def fill_libTable():
    connect = sqlite3.connect(databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT ID,Name,Author,Year,Count FROM Library WHERE Count>0 ORDER BY ID")
    books = cursor.fetchall()
    return books


def fill_onHandTable():
    connect = sqlite3.connect(databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT ID,Name,Author,Year,takeID FROM NotInLibrary ORDER BY ID")
    books = cursor.fetchall()
    return books


def sort1(byWhat):
    connect = sqlite3.connect(databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT ID,Name,Author,Year,Count FROM Library WHERE Count>0 ORDER BY " + str(byWhat))
    return cursor.fetchall()


def sort2(byWhat):
    connect = sqlite3.connect(databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT ID,Name,Author,Year,takeID FROM NotInLibrary ORDER BY " + str(byWhat))
    return cursor.fetchall()


def add_countBooks(ID, count):
    try:
        connect = sqlite3.connect(databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Library SET Count=Count+{0} WHERE ID={1}"
                       .format(count, ID))
        connect.commit()
    except Exception as e:
        print(e)


def add_to_database(data):
    try:
        connect = sqlite3.connect(databaseName)
        cursor = connect.cursor()
        cursor.execute("INSERT INTO library VALUES (?,?,?,?,?,0,0,0)", data)
        connect.commit()
    except Exception as e:
        print(e)


def del_from_database(ID):
    try:
        connect = sqlite3.connect(databaseName)
        cursor = connect.cursor()
        cursor.execute("DELETE FROM library WHERE ID=" + str(ID))
        connect.commit()
    except Exception as e:
        print(e)


def check_id(ID):
    try:
        connect = sqlite3.connect(databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT ID FROM Library WHERE ID=" + str(ID))
        contain = cursor.fetchall()[0]
        print(contain)
        return False
    except IndexError:
        return True


def take_book(ID, takeID):
    try:
        connect = sqlite3.connect(databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT timeTake FROM NotInLibrary WHERE takeID=" + str(takeID))
        time = cursor.fetchall()[0][0]
        date_format = '%y-%m-%d'
        time = datetime.strptime(time, date_format)
        now = datetime.strptime(datetime.now().strftime('%y-%m-%d'), date_format)
        res = now-time
        res = int(res.days)
        cursor.execute("UPDATE Library SET Count=Count+1,OnHandsCount=OnHandsCount-1,AllTime=AllTime+{0} WHERE ID={1}"
                       .format(res, ID))
        cursor.execute("DELETE FROM NotInLibrary WHERE ID={0} AND TakeID={1}".format(ID, takeID))
        connect.commit()
    except Exception as e:
        print(e)


def give_book(ID, takerID):
    try:
        connect = sqlite3.connect(databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Count FROM Library WHERE ID=" + str(ID))
        count = int(cursor.fetchall()[0][0])
        connect.commit()
        if count > 0:
            cursor.execute("UPDATE Library SET Count=Count-1,OnHandsCount=OnHandsCount+1,CountTakes=CountTakes+1 "
                           "WHERE ID=" + str(ID))
            cursor.execute("SELECT ID,Name,Author,Year FROM Library WHERE ID=" + str(ID))
            data = cursor.fetchall()[0]
            cursor.execute("INSERT INTO NotInLibrary VALUES (?,?,?,?,{0},'{1}',{2})"
                           .format(get_max_ID(), datetime.now().strftime('%y-%m-%d'), takerID), data)
            connect.commit()
            return count
        else:
            cursor.execute("UPDATE Library SET Count=0 WHERE ID=" + str(ID))
            connect.commit()
            return count
    except Exception as e:
        print(e)


def get_book(ID):
    connect = sqlite3.connect(databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT ID,Name,Author,Year,Count FROM Library WHERE ID=" + str(ID))
    book = cursor.fetchall()[0]
    return book


def get_book_onHand(ID):
    connect = sqlite3.connect(databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT MAX(takeID) FROM NotInLibrary WHERE ID=" + str(ID))
    maxID = cursor.fetchall()[0][0]
    cursor.execute("SELECT ID,Name,Author,Year,takeID FROM NotInLibrary WHERE takeID=" + str(maxID))
    book = cursor.fetchall()[0]
    return book


def get_max_ID():
    try:
        connect = sqlite3.connect(databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT MAX(takeID) FROM NotInLibrary")
        maxID = int(cursor.fetchall()[0][0])
        maxID += 1
        connect.commit()
        return maxID
    except TypeError:
        return 1


def get_middleTime(ID):
    try:
        connect = sqlite3.connect(databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT AllTime FROM Library WHERE ID=" + str(ID))
        time = cursor.fetchall()[0][0]
        cursor.execute("SELECT CountTakes FROM Library WHERE ID=" + str(ID))
        takes = cursor.fetchall()[0][0]
        if takes == 0:
            return 0
        return round(time/takes, 2)
    except Exception as e:
        print(e)