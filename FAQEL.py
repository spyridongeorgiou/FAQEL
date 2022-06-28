# FAQEL https://github.com/spyridongeorgiou/FAQEL
# Written by Spyridon Georgiou https://github.com/spyridongeorgiou
# See license(s) for usage

import tkinter as tk # GUI framework
import tkinter.messagebox # warning pop up
import customtkinter # Main GUI module used in this program. Credit goes to https://github.com/TomSchimansky/CustomTkinter 
import sqlite3 # for DB
import os # for OS interaction, mainly to ensure the DB file is in the same directory the program is running as
#import logging

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk() # defining our main name

##screen_width = app.winfo_screenwidth() # getting current screen width
##screen_height = app.winfo_screenheight() # and height

screen_width = 1280 # screen width
screen_height = 720 # screen height

app.geometry(f"{screen_width}x{screen_height}") # setting current screen width and height as our starting window size
#print((f"Resolution:{screen_width}x{screen_height}"))
app.title("FAQEL") # the app name
logged_in = False
### Database ###

try:
    # Make sure to find the file.db in the script directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
    db_path = os.path.join(BASE_DIR, "FAQELSQL.db")
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

    cur.execute("""
        CREATE TABLE nutzer_table (
        nutzerid id integer primary key ,
        benutzername VARCHAR (255),
        vorname VARCHAR (255) ,
        nachname VARCHAR (255) ,
        passwort VARCHAR (255))
        """)
    print("Table nutzer_table successfully created!")

    print("Database successfully created!")
except:
    print("Error: Database exists already!")
##print("Error: Tables not created!")

##eventqueue = [] #maybe try making a custom eventqueue for handling buttons?

def search_event(): # button event handling function
    print("SEARCH")
    search_query = cur.execute(f"SELECT * FROM frage_table, antwort_table, nutzer_table WHERE{searchbox.get()}")
    tkinter.messagebox.showerror("Fehler", "Bitte geben Sie einen Wert ein.")
##def add_event():
##    cur.execute("INSERT INTO frage (frage) VALUES (f"{frage}")")

def query_antwort():
    print("BEANTWORTET DURCH")
    query_antwort = cur.execute("SELECT * FROM antwort_table")
    print(query_antwort)

def add_question():
    print("FRAGE STELLEN")
    sql = f"""INSERT INTO frage_table (frage,antwortid)
        VALUES ({str(ask_question_entry.get())})"""

#    insert_frage = cur.execute("""
#        INSERT INTO frage_table (
#        frage,beantwortet,nutzerid) VALUES (?,?,?)
#        """)
#    question = (ask_question_entry.get(),False,)

#    cur.commit()
#    return cur.lastrowid

def login_screen(): # CREATE LOGIN TOPLEVEL WINDOW
    ##app.withdraw()
    login_window = customtkinter.CTkToplevel(app) #create toplevel window
    login_window.geometry("350x200") # window size
    login_window.attributes("-topmost", True)# set topmost
    login_window.title("FAQEL - Einloggen") # window title 

    login_window.grab_set() # set grab focus

    username_frame = customtkinter.CTkFrame(master=login_window) # create login frame for entering username and password
    username_frame.pack(side="top", fill="both")

    password_frame = customtkinter.CTkFrame(master=login_window) # create login frame for entering username and password
    password_frame.pack(side="top", fill="both")

    username_label = customtkinter.CTkLabel(master=username_frame, text="Nutzername ") # username label 
    username_label.pack(side="left")

    username = customtkinter.CTkEntry(master=username_frame, placeholder_text="Nutzername eingeben...") #username box 
    username.pack(side="left", pady=5, padx=5)

    password_label = customtkinter.CTkLabel(master=password_frame, text="Passwort ") # password label
    password_label.pack(side="left")   
    
    password_login_entry = customtkinter.CTkEntry(master=password_frame, placeholder_text="Passwort eingeben...") #password box
    password_login_entry.pack(side="left", pady=5, padx=5)

    login_button = customtkinter.CTkButton(master=login_window,text="Einloggen" ) # login button within function/toplevel window
    login_button.pack(side="top", pady=5, padx=10, fill="both")

    new_register_button = customtkinter.CTkButton(master=login_window,text="Kein Konto?", command=lambda:[register_screen(), login_window.destroy()]) # register button
    new_register_button.pack(side="top", pady=5, padx=10, fill="both",)

    cancel_button = customtkinter.CTkButton(fg_color="orange",hover_color="red", master=login_window,text="Abbrechen ", text_color="black", command=login_window.destroy) #cancelbutton 
    cancel_button.pack(side="top", pady=5, padx=10, fill="both")
    
    ##window.grab_release()
    ##app.deiconify

def register_screen(): # CREATE REGISTER TOPLEVEL WINDOW
    register_window = customtkinter.CTkToplevel(app) #create toplevel window
    register_window.geometry("350x225") # window size
    register_window.attributes("-topmost", True) # set topmost
    register_window.title("FAQEL - Registrieren") # window title 

    register_window.grab_set() # set grab focus

    register_label = customtkinter.CTkLabel(master=register_window, text="Wählen Sie einen Nutzernamen und ein Passwort aus") # regkster label 
    register_label.pack(side="top", fill="both")

    username_frame = customtkinter.CTkFrame(master=register_window) # create login frame for entering username
    username_frame.pack(side="top", fill="both")

    password_frame = customtkinter.CTkFrame(master=register_window) # create login frame for entering password
    password_frame.pack(side="top", fill="both")

    password_confirm_frame = customtkinter.CTkFrame(master=register_window) # create login frame for entering username and password
    password_confirm_frame.pack(side="top", fill="both")

    username_label = customtkinter.CTkLabel(master=username_frame, text="Nutzername ") # username label 
    username_label.pack(side="left")

    username = customtkinter.CTkEntry(master=username_frame, placeholder_text="Nutzername eingeben...") #username box 
    username.pack(side="left",pady=5, padx=5)

    password_label = customtkinter.CTkLabel(master=password_frame, text="Passwort ") # password label
    password_label.pack(side="left")

    password_register_entry = customtkinter.CTkEntry(master=password_frame, placeholder_text="Passwort eingeben...") #password box
    password_register_entry.pack(side="left",pady=5, padx=5)

    password_label_confirm = customtkinter.CTkLabel(master=password_confirm_frame, text="Passwort ") # password label
    password_label_confirm.pack(side="left")

    password_confirm = customtkinter.CTkEntry(master=password_confirm_frame, placeholder_text="Passwort eingeben...") #password box
    password_confirm.pack(side="left",pady=5, padx=5)

    register_button = customtkinter.CTkButton(master=register_window,text="Einloggen" ) # login button
    register_button.pack(side="top", pady=5, padx=10, fill="both")

    cancel_button = customtkinter.CTkButton(fg_color="orange",hover_color="red", master=register_window,text="Abbrechen ", text_color="black", command=register_window.destroy) # cancel button
    cancel_button.pack(side="top", pady=5, padx=10, fill="both") 


searchbarframe = customtkinter.CTkFrame(master=app, width=screen_width, height=8, corner_radius=5) # frame container for searchbar
searchbarframe.pack(side="top", pady=5, padx=5, fill="both")

contentframe1 = customtkinter.CTkFrame(master=app) # frame container
contentframe1.pack(pady=10, padx=10, fill="both", expand=True)

searchbox = customtkinter.CTkEntry(master=searchbarframe, placeholder_text="Suchen... ") #searchbox
searchbox.pack(side="left", pady=5, padx=5)

login_button = customtkinter.CTkButton(master=searchbarframe, width=5,text="Einloggen ", command=login_screen) #login button
login_button.pack(side="right", pady=1, padx=1)

optionmenu_1 = customtkinter.CTkOptionMenu(searchbarframe, values=["Alle", "Option 2", "Option 42 long long long...","Test"])
optionmenu_1.pack(side="left", pady=12, padx=10)
optionmenu_1.set("Frage gestellt durch")

optionmenu_1 = customtkinter.CTkOptionMenu(searchbarframe, values=["Alle", "Option 42 long long long...","Test"])
optionmenu_1.pack(side="left", pady=12, padx=10)
optionmenu_1.set("Beantwortet durch")

searchbutton = customtkinter.CTkButton(master=searchbarframe, width=5,text="Suchen ", command=search_event,) #searchbutton
searchbutton.pack(side="left", pady=1, padx=1)

ask_question_frame = customtkinter.CTkFrame(master=app, height=12, corner_radius=5) #frame which stores entry aswell as button(s)
ask_question_frame.pack(side="bottom", pady=5, padx=10, fill="both")

ask_question_entry = customtkinter.CTkEntry(master=ask_question_frame, height=80, placeholder_text="Frage eingeben... ")
ask_question_entry.pack(side="bottom", pady=12, padx=10, fill="x")

ask_question_button = customtkinter.CTkButton(master=ask_question_frame, width=10,height=35, text="Frage stellen", corner_radius = 90, command=add_question)
ask_question_button.pack(side="bottom", pady=5, padx=5)

#button_2 = customtkinter.CTkButton(master=contentframe1, width=5, text="create toplevel", command=login_screen)
#button_2.pack(pady=12, padx=10)

#button_3 = customtkinter.CTkButton(master=contentframe1,)
#button_3.pack(pady=12, padx=10)

rows = cur.fetchall() #get all rows in the DB

for row in rows: 
    print(row) # print out all the content in the rows

if __name__ == "__main__":
    ##app.eval('tk::PlaceWindow . center')
    app.mainloop() #this ensures the program updates all the content/events, any code after this will not be executed in the mainloop
    ##app.attributes("-topmost", True)