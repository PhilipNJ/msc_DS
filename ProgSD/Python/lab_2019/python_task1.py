import sqlite3

#create database called BookInfo.db
with sqlite3.connect("BookInfo.db") as db: 
    cursor = db.cursor() 

cursor.execute("""CREATE TABLE IF NOT EXISTS Authors( 
    "Name" text PRIMARY KEY, 
    "Place of Birth" text NOT NULL);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Books( 
    "ID" text PRIMARY KEY, 
    "Title" text NOT NULL,
    "Author" text NOT NULL,
    "Date Published" text NOT NULL);""")

#insert data into Authors table
cursor.execute("""INSERT INTO Authors(Name, "Place of Birth") 
    VALUES("J.K. Rowling", "Bristol");""")

cursor.execute("""INSERT INTO Authors(Name, "Place of Birth") 
    VALUES("Agatha Christie", "Torquay");""")

cursor.execute("""INSERT INTO Authors(Name, "Place of Birth") 
    VALUES("Oscar Wilde", "Dublin");""")

cursor.execute("""INSERT INTO Books(ID, Title, Author, "Date Published")
               VALUES("1", "De Profundis", "Oscar Wilde", "1905");""")

cursor.execute("""INSERT INTO Books(ID, Title, Author, "Date Published")
               VALUES("2","Harry Potter and the chamber of secrets", "J.K. Rowling", "1998");""")

cursor.execute("""INSERT INTO Books(ID, Title, Author, "Date Published")
               VALUES("3", "The seven dials mystery","Agatha Christie", "1929");""")

cursor.execute("""INSERT INTO Books(ID, Title, Author, "Date Published")
               VALUES("4","The picture of Dorian Gray","Oscar Wilde","1890");""")

cursor.execute("""INSERT INTO Books(ID, Title, Author, "Date Published")
               VALUES("5","Murder on the orient Express","Agatha Christie","1934");""")

cursor.execute("""INSERT INTO Books(ID, Title, Author, "Date Published")
               VALUES("6","Harry Poter and the prisoner of Azkaban","J.K. Rowling","1999");""")

db.commit()