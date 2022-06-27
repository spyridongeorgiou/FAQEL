#FAQLE

import tkinter as tk
import tkinter.messagebox
import customtkinter #https://github.com/TomSchimansky/CustomTkinter
import sqlite3
import os
#import logging

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk() # defining our main name

screen_width = app.winfo_screenwidth() # getting current screen width
screen_height = app.winfo_screenheight() # and height

screen_width = 800 # screen width
screen_height = 600 # height

app.geometry(f"{screen_width}x{screen_height}") # setting current screen width and height as our starting window size
#print((f"Resolution:{screen_width}x{screen_height}"))
app.title("FAQEL") # the app name

### Database ###

try:
    # Make sure to find the file.db in the script directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
    db_path = os.path.join(BASE_DIR, "FAQLESQL.db")
    conn = sqlite3.connect(db_path)

except sqlite3.Error as error:
    print("Failed to read data from sqlite table", error)

#create cursor
cur = conn.cursor()

#create table
try:
    cur.execute("""CREATE TABLE frage_table (
        frageid id integer primary key ,
        frage TEXT ,
        antwortid INTEGER , 
        beantwortet BOOLEAN ,
        nutzerid INTEGER
        )""")
    print("Table frage_table successfully created!")
    cur.execute("""CREATE TABLE antwort_table (
        antwortid id INTEGER PRIMARY KEY ,
        antwort TEXT ,
        frageid INTEGER ,
        nutzerid INTEGER
        )""")
    print("Table antwort_table successfully created!")
    cur.execute("""CREATE TABLE nutzer_table (
        nutzerid id integer primary key ,
        vorname VARCHAR (255) ,
        nachname VARCHAR (255) ,
        passwort VARCHAR (255)
        )""")
    print("Table nutzer_table successfully created!")
    print("Database successfully created!")
except:
    print("Error: Database exists already!")
##print("Error: Tables not created!")

##eventqueue = [] #maybe try making a custom eventqueue for handling buttons?
rows = cur.fetchall()

for row in rows:
    print(row)

def search_event(): # button event handling function
    print("SEARCH")
    query = cur.execute(f"SELECT * FROM frage_table, antwort_table, nutzer_table WHERE{searchbox.get()}")
    tkinter.messagebox.showerror("Fehler", "Bitte geben Sie einen Wert ein.")
##def add_event():
##    cur.execute("INSERT INTO frage (frage) VALUES (f"{frage}")")

searchbarframe = customtkinter.CTkFrame(master=app, width=screen_width, height=8, corner_radius=15) # frame container+
searchbarframe.pack(side="top", pady=5, padx=5, fill="both")

contentframe1 = customtkinter.CTkFrame(master=app) # frame container
contentframe1.pack(pady=10, padx=10, fill="both", expand=True)

searchbox = customtkinter.CTkEntry(master=searchbarframe, placeholder_text="Suchen...") #searchbox
searchbox.pack(side="left", pady=5, padx=5)

optionmenu_1 = customtkinter.CTkOptionMenu(searchbarframe, values=["Option 1", "Option 2", "Option 42 long long long...","Spyridon"])
optionmenu_1.pack(side="left", pady=12, padx=10)
optionmenu_1.set("Frage gestellt durch")

optionmenu_1 = customtkinter.CTkOptionMenu(searchbarframe, values=["Option 1", "Option 2", "Option 42 long long long...","Spyridon"])
optionmenu_1.pack(side="left", pady=12, padx=10)
optionmenu_1.set("Beantwortet durch")

searchbutton = customtkinter.CTkButton(master=searchbarframe, width=5,text="Suchen", command=search_event,) #searchbutton
searchbutton.pack(side="left", pady=1, padx=1)


entry_1 = customtkinter.CTkEntry(master=contentframe1, placeholder_text="CTkEntry")
entry_1.pack(pady=12, padx=10)

button_1 = customtkinter.CTkButton(master=contentframe1,)
button_1.pack(pady=12, padx=10)

button_2 = customtkinter.CTkButton(master=contentframe1,)
button_1.pack(pady=12, padx=10)

button_3 = customtkinter.CTkButton(master=contentframe1,)
button_1.pack(pady=12, padx=10)

    

if __name__ == "__main__":
    app.attributes("-topmost", True)
    app.eval('tk::PlaceWindow . center')
    app.mainloop()
