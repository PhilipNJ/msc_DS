import sqlite3 
with sqlite3.connect("BookInfo.db") as db: 
 cursor=db.cursor() 

print("List of Authors and their Place of Birth")

cursor.execute("SELECT * FROM Authors")
print(cursor.fetchall())

print("Given a Place of Birth, list of the books of the authors born there")
place_birth = input("Enter the place of birth: ")

cursor.execute("""
               SELECT Books.Title, Books."Date Published", Authors.Name, Authors."Place of Birth" 
               FROM Authors,Books 
               WHERE Authors.Name= Books.Author AND Authors."Place of Birth" = ?""", 
               (place_birth,))
print(cursor.fetchall())
db.close()
