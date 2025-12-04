import sqlite3
from datetime import date
import jdatetime
import pandas as pd

today = jdatetime.date.today()


def connect():
    conn = sqlite3.Connection("TODO.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Tasks(ID integer primary key,CreatedDate text not null,TaskName text not null,Assignee text,IsDeleted text not null,Due text)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Employees(ID integer primary key,FirstName text not null,LastName text not null)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Person(PersonID integer primary key,FirstName text not null,LastName text not null)")
    conn.commit()
    conn.close()


def viewTask():
    conn = sqlite3.Connection("TODO.db")
    cursor = conn.cursor()
    cursor.execute(
        'SELECT Due,Status,Assignee,CreatedDate,TaskName FROM Tasks WHERE Status != "انجام شده" AND IsDeleted = 0')
    rows = cursor.fetchall()
    conn.close()
    return rows


def insertTask(taskName, assigne, Status, due):
    conn = sqlite3.Connection("TODO.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Tasks(CreatedDate,TaskName,Assignee,Status,Due,IsDeleted) VALUES(?,?,?,?,?,0)",
                   (str(today), taskName, assigne, Status, due))
    conn.commit()
    conn.close()


def deleteTask(oldTaskName, oldAssignee):
    conn = sqlite3.Connection("TODO.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Tasks SET IsDeleted = 1 WHERE TaskName = ? AND Assignee=?", (oldTaskName, oldAssignee))
    conn.commit()
    conn.close()


def updateTask(oldTaskName, oldAssignee, taskName, Assignee, Status, Due):
    conn = sqlite3.Connection("TODO.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Tasks SET TaskName=?,Assignee=?,Status=?,Due = ? WHERE TaskName = ? AND Assignee=?",
                   (taskName, Assignee, Status, Due, oldTaskName, oldAssignee))
    conn.commit()
    conn.close()


# =============================================== Person =============================================
def viewPerson():
    conn = sqlite3.Connection("TODO.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Person WHERE IsDeleted = 0")
    rows = cursor.fetchall()
    conn.close()
    return rows


def insertPerson(FirstName, LastName):
    conn = sqlite3.Connection("TODO.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Person(FirstName,LastName,IsDeleted) VALUES(?,?,0)", (FirstName, LastName))
    conn.commit()
    conn.close()


def duplicatePerson(fullName):
    conn = sqlite3.Connection("TODO.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Person WHERE (FirstName || ' ' || LastName) = ? AND IsDeleted = 0", (fullName,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def deletePerson(fullName):
    conn = sqlite3.Connection("TODO.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Person SET IsDeleted = 1 WHERE (FirstName || ' ' || LastName) = ?",
                   (fullName,))
    conn.commit()
    conn.close()


def editPerson(oldFullName, newFirstName, newLastName):
    conn = sqlite3.Connection("TODO.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Person SET FirstName = ? , LastName = ? WHERE (FirstName || ' ' || LastName) = ? AND IsDeleted = 0",
        (newFirstName, newLastName, oldFullName))
    conn.commit()
    conn.close()


# =============================================== Export =============================================
def exportToExcel():
    conn = sqlite3.Connection("TODO.db")
    df = pd.read_sql_query(sql="SELECT * FROM Tasks", con=conn)
    df.to_excel("Tasks.xlsx", index=False)
    conn.close()


connect()
