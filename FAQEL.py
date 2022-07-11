# FAQEL https://github.com/spyridongeorgiou/FAQEL
# Written by Spyridon Georgiou https://github.com/spyridongeorgiou
# See license(s) for usage

# comments starting with ## are marked as code which may be useful for debugging or may be worked on in a future release
# comments eclosed with ###  are just used to better visualize where different parts of code start

import tkinter as tk # GUI framework
import tkinter.messagebox # warning pop up
from tkinter import ttk
from turtle import update
import customtkinter # Main GUI module used in this program. Credit goes to https://github.com/TomSchimansky/CustomTkinter
import mysql.connector # importing our connector  to connect 
from mysql.connector import errorcode
import sqlite3 # use sqlite to create a local database in case you do not have internet or the firewall blocks the connection
import csv # in order to open the mysqlconfig.csv, this can be omitted however if you just enter the credentials directly into the config dictionary
import sys # check current python version
import os # for OS interaction, mainly to ensure the DB file is in the same directory the program is running as
import datetime # for getting current date to pass into DB
import time
##import logging

program_version = "1.1.1"
python_version = sys.version
combined_version = f"Programm Version: {program_version} | Python Version: {python_version}" # combine both the program version aswell as the current python version running the program

# NOTE to self: add a button to switch between german/english (maybe other languages too?)

current_date = datetime.date.today()

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue","sweetkind"

app = customtkinter.CTk() # defining our main name

screen_width = app.winfo_screenwidth() # getting current screen width
screen_height = app.winfo_screenheight() # and height

##screen_width = 1280 # screen width
##screen_height = 720 # screen height

app.geometry(f"{int(screen_width//1.2)}x{int(screen_height//1.3)}") # setting window size
#print((f"Resolution:{screen_width}x{screen_height}"))
app.title("FAQEL") # the desired app name

nutzer_id = 0 # the standard local user ID is zero, this will get changed depending on wether or not you are logged in
current_tree_focus = 0 # set the value for the focused tree item to None initially until a question is selected
current_tree2_focus = 0

# get current width and height of the monitor
# useful for sizing the window appropriately relative to monitor size
def get_current_wh():
    global current_wh_list
    current_h_app = app.winfo_height()
    current_w_app = app.winfo_width()
    current_wh_list = [current_w_app,current_h_app]
    return
get_current_wh() # call this function, outside the main/secondary loop, once so the current_wh_list isnt empty. perhaps there's a more elegant solution?

# open the main config to connecting to your desired database
# whenever you use this function to open the config a list within a list is created, below in the config variable you can see how i access the list [1] and then the contents of the list with another [?] i.e. [1][?]
with open("mysqlconfig.csv","r") as configfile:
    reader = csv.reader(configfile)
    data = list(reader)
##print(data)

# the main config to connecting to your desired database
# the config format is as follows in csv:
#   user,password,host,database,port,raise_on_warnings
# feel free to create your own mysqlconfig.csv to connect to your own database
config = {
  "user": data[1][3],
  "password": data[1][4],
  "host": data[1][0],
  "database": data[1][2],
  "port": int(data[1][1]),
  "raise_on_warnings": True
}

##try:
##    # Make sure to find the file.db in the script directory
##    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
##    db_path = os.path.join(BASE_DIR, "FAQELSQL.db")
##    conn = sqlite3.connect(db_path)
##
##except sqlite3.Error as error:
##    print("Failed to read data from sqlite table", error)
##
##sqlite_cursor = conn.cursor() #create the sqlite3 cursor
def create_mysql_cursor():
    try:
        global cnx
        cnx = mysql.connector.connect(**config,autocommit=True)
        global mysql_cursor
        mysql_cursor = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password!")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist!")
        else:
            print(err)
create_mysql_cursor()

        ## implement sqlite local db incase you cant connect to mysql db
##
        #### open the default config for sqlite db
        ####with open("mysqlconfigdefault.csv","r") as defaultconfigfile:
        ####    reader = csv.reader(defaultconfigfile)
        ####    data = list(reader)
##
        ##print("Connecting to local DB!")
        ##try:
        ##    create_nutzer_table = ("""
        ##        CREATE TABLE IF NOT EXISTS 
        ##        nutzer_table (
        ##        nutzer_id ID INTEGER PRIMARY KEY ,
        ##        benutzername VARCHAR (255),
        ##        vorname VARCHAR (255) ,
        ##        nachname VARCHAR (255);
        ##        ) """)
##
        ##    create_frage_table = ("""
        ##        CREATE TABLE IF NOT EXISTS 
        ##        frage_table (
        ##        frage_id ID INTEGER PRIMARY KEY,
        ##        frage TEXT NOT NULL, 
        ##        beantwortet BOOLEAN
        ##        tags VARCHAR(32);
        ##        ) """)
    ##
        ##    create_antwort_table = ("""
        ##        CREATE TABLE IF NOT EXISTS 
        ##        antwort_table (
        ##        antwort_id ID INTEGER PRIMARY KEY ,
        ##        antwort_datum DATE NOT NULL,
        ##        antwort TEXT NOT NULL,
        ##        FOREIGN KEY (fragen_id) REFERENCES frage_table(frage_id); ,
        ##        FOREIGN KEY (nutzer_id) REFERENCES nutzer_table(nutzer_id);
        ##        ) """)
##
    ##
        ##    sqlite_cursor.execute(create_nutzer_table) # create antwort_table in sqlite
        ##    print("Table nutzer_table created successfully!")
        ##    sqlite_cursor.execute(create_antwort_table) # create antwort_table in sqlite
        ##    print("Table antwort_table created successfully!")
        ##    sqlite_cursor.execute(create_frage_table) # create nutzer_table in sqlite
        ##    print("Table nutzer_table created successfully")
        ##    print("Database successfully created!")
        ##except:
        ##    print("Error: Database exists already!")


mysqlite_connection = cnx # our mysql connection

### creating the tables in MySQL 8 ###

### NOTE (to self): use this if you have to nuke the database ###
##mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
##mysql_cursor.execute("DROP TABLE IF EXISTS nutzer_table;")
##mysql_cursor.execute("DROP TABLE IF EXISTS frage_table;")
##mysql_cursor.execute("DROP TABLE IF EXISTS antwort_table;")
##mysql_cursor.execute("DROP TABLE IF EXISTS secret_table;")

### this DB will pretty much only be created once NOTE: perhaps move this into a seperate script?###

create_nutzer_table = ("""
    CREATE TABLE IF NOT EXISTS nutzer_table (
      nutzer_id INT NOT NULL AUTO_INCREMENT,
      nutzername VARCHAR(32) NOT NULL,
      vorname VARCHAR(32),
      nachname VARCHAR(32),
      PRIMARY KEY (nutzer_id)) ENGINE=INNODB;
    """)

try:
    mysql_cursor.execute(create_nutzer_table)
except:
    print("Error while creating nutzer_table")

create_antwort_table = ("""
    CREATE TABLE IF NOT EXISTS antwort_table (
      antwort_id INT NOT NULL AUTO_INCREMENT,
      antwort_datum DATE NOT NULL,
      antwort TEXT NOT NULL,
      frage_id INT NOT NULL,
      nutzer_id INT NOT NULL,
      PRIMARY KEY (antwort_id)) ENGINE=INNODB;
    """)

try:
    mysql_cursor.execute(create_antwort_table)
except:
    print("Error while creating antwort_table")

create_frage_table = ("""
    CREATE TABLE IF NOT EXISTS frage_table (
      frage_id INT NOT NULL AUTO_INCREMENT,
      frage VARCHAR (255) NOT NULL,
      frage_datum DATE NOT NULL,
      beantwortet ENUM('False', 'True') NOT NULL,
      antwort_id INT,
      tags VARCHAR(32),
      nutzer_id INT,
      PRIMARY KEY (frage_id),
      INDEX `idx_antwort` (antwort_id),
      CONSTRAINT `fk_antwort_id_frage`
      FOREIGN KEY (antwort_id)
      REFERENCES antwort_table(antwort_id) ON UPDATE CASCADE) ENGINE=INNODB;
    """)

try: 
    mysql_cursor.execute(create_frage_table)
except:
    print("Error while creating frage_table")

create_secret_table =("""
    CREATE TABLE IF NOT EXISTS secret_table (
      hashed_password VARCHAR(255), 
      nutzer_id INT NOT NULL,
      PRIMARY KEY (hashed_password),
      INDEX `idx_nutzer` (nutzer_id),
      CONSTRAINT `fk_nutzer_id`
      FOREIGN KEY (nutzer_id)
      REFERENCES nutzer_table(nutzer_id) ON UPDATE CASCADE)ENGINE=INNODB;
    """)

try:
    mysql_cursor.execute(create_secret_table)
except:
    print("Error while creating secret_table")

### generate some sample data
##mysql_cursor.execute(f"INSERT INTO frage_table (frage_id,frage,frage_datum,tags,nutzer_id) VALUES ('1','Was ist FAQEL?','2022-06-07','FAQEL','1');")
##mysql_cursor.execute(f"INSERT INTO frage_table (frage_id,frage,frage_datum,tags,nutzer_id) VALUES ('2','Wer hat FAQEL kreeiert?','2022-06-07','FAQEL','1');")
##mysql_cursor.execute(f"INSERT INTO frage_table (frage_id,frage,frage_datum,tags,nutzer_id) VALUES ('3','Wie wurde FAQEL programmiert?','2022-06-07','FAQEL','1');")

##def delete_empty():
##    mysql_cursor.execute("DELETE FROM antwort_table WHERE antwort =' ' OR frage IS NULL;") #delete accidental empty values
##    mysql_cursor.execute("DELETE FROM frage_table WHERE frage=' ' OR frage IS NULL;") #delete accidental empty values


def search_event(event): # button event handling function
    print("SEARCH")
    search_event_sql_frage_table = (f"""
      SELECT * FROM frage_table WHERE 
      (frage_id LIKE '%{searchbox.get()}%' OR 
      frage_datum LIKE '%{searchbox.get()}%' OR 
      frage LIKE '%{searchbox.get()}%' OR 
      antwort_id LIKE '%{searchbox.get()}%' OR
      tags LIKE '%{searchbox.get()}%' OR 
      beantwortet LIKE '%{searchbox.get()}%' OR
      nutzer_id LIKE '%{searchbox.get()}%' )  
      ORDER BY frage_id;
    """)
    search_event_sql_antwort_table = (f"""
    SELECT * FROM antwort_table WHERE 
      (antwort_id LIKE '%{searchbox.get()}%' OR 
      antwort_datum LIKE '%{searchbox.get()}%' OR 
      antwort LIKE '%{searchbox.get()}%' OR 
      frage_id LIKE '%{searchbox.get()}%' OR
      nutzer_id LIKE '%{searchbox.get()}%' )  
      ORDER BY antwort_id;
    """)
    for tree_child in tree.get_children():
        ##print(tree.get_children())
        tree.delete(tree_child)
    for tree2_child in tree2.get_children():
        ##print(tree2.get_children())
        tree2.delete(tree2_child)
    update_treeview_antwort_table(search_event_sql_antwort_table)
    update_treeview_frage_table(search_event_sql_frage_table)
    ##tkinter.messagebox.showinfo("Kein Resultat", "Leider ergab Ihre Suche kein Resultat!")

##def add_event():
##    cur.execute("INSERT INTO frage (frage) VALUES (f"{frage}")")

def query_antwort():
    print("BEANTWORTET DURCH")
    ##query_antwort = squlite_cursor.execute("""SELECT * FROM antwort_table""")
    ##print(query_antwort)

##mysql_cursor.execute("INSERT INTO nutzer_table VALUES ('1','GeorgiouS','Spyridon','Georgiou')")

def add_question(event):
    print("FRAGE STELLEN")
    add_question_sql = f"""
    INSERT INTO frage_table (frage,frage_datum,nutzer_id) 
    VALUES ('{str(ask_question_entry.get())}','{current_date}','{nutzer_id}');
    """
    try:
        mysql_cursor.execute(add_question_sql)
    except:
        tkinter.messagebox.showerror("Datenbankfehler", "Ihre Frage konnte nicht zur Datenbank hinzugefügt werden, Ihre Frage ist zu lang (Zeichenlimit 255)!")
    update_answer()
    update_treeview_antwort_table("SELECT * FROM frage_table ORDER BY frage_id;")


def add_answer(event):
    print("FRAGE BEANTWORTEN")
    add_answer_sql = f"""
    INSERT INTO antwort_table (antwort,antwort_datum,frage_id,nutzer_id) 
    VALUES ('{str(add_answer_entry.get())}','{current_date}','{current_tree_focus}','{nutzer_id}');
    """
    update_question_answered_sql = f"""
    UPDATE frage_table
    SET beantwortet = 'True'
    WHERE frage_id ='{current_tree_focus}';
    """
    try:
        mysql_cursor.execute(add_answer_sql) # execute the above add_answer_sql query to insert our answer with the standard values
        mysql_cursor.execute(update_question_answered_sql) # set the beantwortet (german for "answered") row value to True because the question has now been answered
    except:
        tkinter.messagebox.showerror("Datenbankfehler", "Ihre Antwort konnte nicht zur Datenbank hinzugefügt werden! Wählen Sie zuerst eine Frage aus (Linksklick auf die Frage)!")
    update_answer()
    update_treeview_antwort_table("SELECT * FROM antwort_table ORDER BY antwort_id;")
    #query_antwort_table()
    #update_treeview_antwort_table()

def update_answer():
    update_answer_sql = """
    SELECT * FROM antwort_table ORDER BY frage_id;"""
    mysql_cursor.execute(update_answer_sql)
    questions_with_answers = mysql_cursor.fetchall()
    ##print(questions_with_answers)
    for answer in questions_with_answers:
        ##print(answer[3])
        update_question_answered_sql = f"""
        UPDATE frage_table
        SET 
        beantwortet = 'True',
        antwort_id = '{answer[0]}'
        WHERE frage_id ='{answer[3]}';
        """
        mysql_cursor.execute(update_question_answered_sql)
    update_delete_answer_sql = """
    SELECT * FROM antwort_table
    
    """

update_answer()


def send_register_data():
    print("REGISTRIER DATEN WERDEN UEBERMITTELT")
#    register_

### function to create new toplevel window for the user to login ###

def login_screen(): # CREATE LOGIN TOPLEVEL WINDOW
    ##app.withdraw()
    login_window = customtkinter.CTkToplevel(app) #create toplevel window

    login_window.geometry("400x300") # window size
    login_window.attributes("-topmost", True)# set topmost
    login_window.title("FAQEL - Einloggen") # window title 

    login_window.grab_set() # set grab focus

    username_frame = customtkinter.CTkFrame(master=login_window) # create login frame for entering username 
    username_frame.pack(side="top", pady=5, padx=5, fill="both")

    password_frame = customtkinter.CTkFrame(master=login_window) # create login frame for entering password
    password_frame.pack(side="top", pady=5, padx=5, fill="both")

    username_label = customtkinter.CTkLabel(master=username_frame, text="Nutzername ")
    username_label.pack(side="left", pady=5, padx=5, fill="both")

    username = customtkinter.CTkEntry(master=username_frame, placeholder_text="Nutzername eingeben...") 
    username.pack(pady=5, padx=5, fill="both")

    password_label = customtkinter.CTkLabel(master=password_frame, text="Passwort ") # password label
    password_label.pack(side="left",pady=5, padx=5, fill="both")
    
    password_login_entry = customtkinter.CTkEntry(master=password_frame, placeholder_text="Passwort eingeben...") #password box
    password_login_entry.pack(pady=5, padx=5, fill="both")

    login_button = customtkinter.CTkButton(master=login_window,text="Einloggen" ) # login button within function/toplevel window
    login_button.pack(side="top", pady=5, padx=5, fill="both")

    new_register_button = customtkinter.CTkButton(master=login_window,text="Noch kein Konto?", command=lambda:[register_screen(), login_window.destroy()]) # register button
    new_register_button.pack(side="top",pady=5, padx=5, fill="both")
    # cancel button
    cancel_button = customtkinter.CTkButton(fg_color="orange",hover_color="red", master=login_window,text="Abbrechen ", text_color="black", command=lambda:[login_window.grab_release(),login_window.destroy()]) #cancelbutton 
    cancel_button.pack(side="top",pady=5, padx=5, fill="both")
    
    ##window.grab_release()
    ##app.deiconify

### function to create new toplevel window incase user does not have credentials ###

def register_screen(): # CREATE REGISTER TOPLEVEL WINDOW
    register_window = customtkinter.CTkToplevel(app) #create toplevel window
    register_window.geometry("400x300") # window size
    register_window.attributes("-topmost", True) # set topmost
    register_window.title("FAQEL - Registrieren") # window title
    register_window.grab_set() # set grab focus

    register_label = customtkinter.CTkLabel(master=register_window, text="Wählen Sie einen Nutzernamen und ein Passwort aus") # regkster label 
    register_label.pack(side="top",pady=5, padx=5,fill="both")

    username_frame = customtkinter.CTkFrame(master=register_window) # create login frame to hold entrywidget for entering username
    username_frame.pack(side="top",pady=5, padx=5,fill="both")

    password_frame = customtkinter.CTkFrame(master=register_window) # create login frame to hold entrywidget for entering password
    password_frame.pack(side="top",pady=5, padx=5,fill="both")

    password_confirm_frame = customtkinter.CTkFrame(master=register_window) # create login frame to hold entrywidget for confirming password
    password_confirm_frame.pack(side="top",pady=5, padx=5,fill="both")

    username_label = customtkinter.CTkLabel(master=username_frame, text="Nutzername ")
    username_label.pack(side="left",pady=5, padx=5,fill="both")

    username = customtkinter.CTkEntry(master=username_frame, placeholder_text="Nutzername eingeben...") # username box 
    username.pack(side="left",pady=5, padx=5,fill="both")

    password_label = customtkinter.CTkLabel(master=password_frame, text="Passwort ") # password label
    password_label.pack(side="left",pady=5, padx=5,fill="both")

    password_register_entry = customtkinter.CTkEntry(master=password_frame, placeholder_text="Passwort eingeben...") # password box
    password_register_entry.pack(side="left",pady=5, padx=5,fill="both")

    password_label_confirm = customtkinter.CTkLabel(master=password_confirm_frame, text="Passwort bestätigen ") # confirm password label
    password_label_confirm.pack(side="left",pady=5, padx=5,fill="both")

    password_register_confirm = customtkinter.CTkEntry(master=password_confirm_frame, placeholder_text="Passwort bestätigen...") # password box
    password_register_confirm.pack(side="left",pady=5, padx=5,fill="both")

    register_button = customtkinter.CTkButton(master=register_window,text="Registrieren", command=lambda:[send_register_data(),register_window.destroy()] ) # login button
    register_button.pack(side="top",pady=5, padx=5,fill="both")

    cancel_button = customtkinter.CTkButton(fg_color="orange",hover_color="red", master=register_window,text="Abbrechen ", text_color="black", command=register_window.destroy) # cancel button
    cancel_button.pack(side="top",pady=5, padx=5,fill="both")

### main application window ###

main_container = customtkinter.CTkFrame(master=app,corner_radius=15)
main_container.pack(pady=2,fill="both")

searchbar_frame_container = customtkinter.CTkFrame(master=main_container,corner_radius=15) # frame container for options and searchbar 
searchbar_frame_container.pack(side="top",pady=2, fill="both")

##searchbar_frame_options = customtkinter.CTkFrame(master=searchbar_frame_container, width=screen_width//2, height=30, corner_radius=15) # frame container for searchbar options
##searchbar_frame_options.pack(side="top", pady=2, fill="both")

searchbar_frame = customtkinter.CTkFrame(master=searchbar_frame_container, width=screen_width//2, height=30, corner_radius=15) # frame container for the searchbar itself
searchbar_frame.pack(side="top", pady=2, fill="both")

searchbutton = customtkinter.CTkButton(master=searchbar_frame, width=5,text="Suchen ", command=lambda:[search_event('<Return>')],corner_radius=15) #searchbutton
searchbutton.pack(side="left", pady=5, padx=5)

searchbox = customtkinter.CTkEntry(master=searchbar_frame,width=screen_width//2, placeholder_text="Suchen... ") #searchbox top left
searchbox.pack(side="left", pady=5, padx=5, fill="both")
searchbox.bind('<Return>',search_event) # bind the Return i.e. the Enter key as an option to trigger the search_event function 

login_button = customtkinter.CTkButton(master=searchbar_frame, width=200,height=30,text="Einloggen/Registrieren", command=login_screen, corner_radius=15) #login button top _right_bottom
login_button.pack(side="right", pady=5, padx=5)


# NOTE: Create a function for a toplevel window for the about page

##about_button = customtkinter.CTkButton(master=searchbar_frame_options, width=40, height=20, text="Über FAQEL", fg_color="grey",text_font=["default_theme", 10])
##about_button.pack( )

##version_label = customtkinter.CTkLabel(master=searchbar_frame_options, width=200,height=30,text=combined_version, corner_radius=15) #login button top _right_bottom
##version_label.pack(side="right", pady=5, padx=5)

##optionmenu_1 = customtkinter.CTkOptionMenu(searchbar_frame_options, values=["Alle", "Option 2", "Option 42 long long long...","Test"]) # optionmenu 1
##optionmenu_1.pack(side="left", pady=5, padx=5)
##optionmenu_1.set("Frage gestellt durch")
##
##optionmenu_2 = customtkinter.CTkOptionMenu(searchbar_frame_options, values=["Alle", "Option 42 long long long...","Test"]) # optionmenu 2
##optionmenu_2.pack(side="left", pady=5, padx=5,)
##optionmenu_2.set("Beantwortet durch")


search_util_container = customtkinter.CTkFrame(master=main_container,height=50,corner_radius=15)
search_util_container.pack(side="bottom",pady=5,padx=5,fill="both")


ask_question_frame = customtkinter.CTkFrame(master=search_util_container,width=current_wh_list[0]*3, height=60, corner_radius=15) #frame which stores entry aswell as button(s)
ask_question_frame.pack(side="left",pady=5, padx=5, fill="both")

ask_question_entry = customtkinter.CTkEntry(master=ask_question_frame,width=current_wh_list[0]*3, placeholder_text="Frage eingeben... ")
ask_question_entry.pack(side="top",pady=10, padx=15, fill="both")

ask_question_button = customtkinter.CTkButton(master=ask_question_frame,width=current_wh_list[0]*3,height=35, text="Frage stellen", command=lambda:[add_question('<Return>')])
ask_question_button.pack(side="bottom", pady=10, padx=10, fill="both")
ask_question_entry.bind('<Return>',add_question)

add_answer_frame = customtkinter.CTkFrame(master=search_util_container, width=current_wh_list[0]*3, height=60, corner_radius=15) #frame which stores entry aswell as button(s)
add_answer_frame.pack(side="right",pady=5, padx=5, fill="both")

add_answer_entry = customtkinter.CTkEntry(master=add_answer_frame,width=current_wh_list[0]*3, placeholder_text="Antwort eingeben... ")
add_answer_entry.pack(side="top",pady=10, padx=15, fill="both")

add_answer_button = customtkinter.CTkButton(master=add_answer_frame,fg_color="#21a366",width=current_wh_list[0]*3,height=35,text="Beantworten ", command=lambda:[add_answer('<Return>')])
add_answer_button.pack(side="bottom",pady=10,padx=10,fill="both")
add_answer_entry.bind('<Return>',add_answer)


main_content_frame_container = customtkinter.CTkFrame(master=main_container,corner_radius=15) # main content frame container
main_content_frame_container.pack(pady=5,padx=5,fill="both")

main_content_frame_left = customtkinter.CTkFrame(master=main_content_frame_container, height=current_wh_list[1]//2.5, width=current_wh_list[0]//3, corner_radius=15) #main content frame left
main_content_frame_left.pack(side="left",pady=5, padx=5, fill="both")

tree_columns = ("frage_id","frage","frage_datum","beantwortet","antwort_id", "tags", "nutzer_id")

style = tk.ttk.Style()
##style.theme_use("clam")
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11,)) # Modify the font of the body
##style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
style.configure("Treeview",
    background="#DDDDDD",
    foreground="#444444",
    rowheight=25,
    fieldbackground="#222222"
    )
style.map("Treeview",
    background=[("selected","#111111")])

tree = tk.ttk.Treeview(main_content_frame_left,style="mystyle.Treeview", height=current_wh_list[1]//3, columns=tree_columns, show='headings')
#print(current_wh_list[1])
tree.column("frage_id",minwidth=55)
tree.column("frage",minwidth=500)
tree.column("frage_datum",minwidth=70)
tree.column("beantwortet",minwidth=85)
tree.column("antwort_id",minwidth=75)
tree.column("tags",minwidth=100)
tree.column("nutzer_id",minwidth=75)

tree.heading("frage_id", text="Frage ID")
tree.heading("frage", text="Frage")
tree.heading("frage_datum", text="Frage Datum")
tree.heading("beantwortet", text="Beantwortet")
tree.heading("antwort_id", text="Antwort ID")
tree.heading("tags", text="Tags")
tree.heading("nutzer_id", text="Nutzer ID",anchor=tk.W)

##tree.grid(row=0,column=0,sticky="nsew")
tree.pack(pady=5,padx=5,fill="both")

##def tree_return_iid():
##    print(tree.identify())



main_content_frame_right_bottom = customtkinter.CTkFrame(master=main_content_frame_container,height=275, width=500, corner_radius=15)
main_content_frame_right_bottom.pack(side="bottom",pady=5, padx=5,fill="both")


mcfrb_add_answer_frame = customtkinter.CTkFrame(master=main_content_frame_right_bottom,corner_radius=15)
mcfrb_add_answer_frame.pack(side="bottom",pady=5,padx=5,fill="both")


mcfrb_question_label_frame = customtkinter.CTkFrame(master=mcfrb_add_answer_frame,height=100,corner_radius=15)
mcfrb_question_label_frame.pack(side="top",pady=5,padx=5,fill="both")


mcfrb_question_label_header_frame = customtkinter.CTkFrame(master=mcfrb_question_label_frame,corner_radius=15)
mcfrb_question_label_header_frame.pack(side="top",pady=15,padx=5,fill="x")

mcfrb_question_label_header = customtkinter.CTkLabel(master=mcfrb_question_label_header_frame,height=18,corner_radius=15,text_font=["Arial", 14],text="Frage")
mcfrb_question_label_header.pack(side="top",pady=5,padx=5)

mcfrb_question_label = customtkinter.CTkLabel(master=mcfrb_question_label_frame,height=50,corner_radius=15,text_font=["Arial", 14],wraplength=current_wh_list[0]*2)
mcfrb_question_label.pack(side="top",pady=5,padx=5,fill="both")
mcfrb_question_label["text"]="""Bitte wählen Sie eine Frage aus (Doppelklick)!
"""


mcfrb_answer_label_frame = customtkinter.CTkFrame(master=mcfrb_add_answer_frame,height=50,corner_radius=15)
mcfrb_answer_label_frame.pack(side="top",pady=5,padx=5,fill="both")

mcfrb_answer_label_header_frame = customtkinter.CTkFrame(master=mcfrb_answer_label_frame,corner_radius=15)
mcfrb_answer_label_header_frame.pack(side="top",pady=15,padx=5,fill="x")

mcfrb_answer_label_header = customtkinter.CTkLabel(master=mcfrb_answer_label_header_frame,height=18,corner_radius=15,text_font=["Arial", 14],text="Antwort")
mcfrb_answer_label_header.pack(side="top",pady=5,padx=5)

mcfrb_answer_label = customtkinter.CTkLabel(master=mcfrb_answer_label_frame,height=100,corner_radius=15,text_font=["Arial", 14,],wraplength=current_wh_list[0]*2)
mcfrb_answer_label.pack(side="top",pady=5,padx=5,fill="both")
mcfrb_answer_label["text"]="""Bitte wählen Sie eine Antwort aus (Doppelklick)!
"""


##show_answers_button = customtkinter.CTkButton(master=mcfrb_add_answer_frame,fg_color="#21a366", width=60,height=30,text="Antworten anzeigen " ) #press this button to refresh the view
##show_answers_button.pack(side="left",pady=5,padx=5,fill="both")


main_content_frame_right_top = customtkinter.CTkFrame(master=main_content_frame_container, height=10, width=500, corner_radius=15)
main_content_frame_right_top.pack(side="top",pady=5, padx=5,fill="x")

tree2_columns = ("antwort_id","antwort_datum","antwort","frage_id","nutzer_id")
tree2 = tk.ttk.Treeview(main_content_frame_right_top,style="mystyle.Treeview", height=200, columns=tree2_columns, show='headings')
#print(current_wh_list[1])
tree2.column("antwort_id",minwidth=55)
tree2.column("antwort",minwidth=400)
tree2.column("antwort_datum",minwidth=55)
tree2.column("frage_id",minwidth=40)
tree2.column("nutzer_id",minwidth=55)

tree2.heading("antwort_id", text="Antwort ID")
tree2.heading("antwort_datum", text="Antwort Datum ")
tree2.heading("antwort", text="Antwort ")
tree2.heading("frage_id", text="Frage ID")
tree2.heading("nutzer_id", text="Nutzer ID", anchor=tk.W)

##tree.grid(row=0,column=0,sticky="nsew")
tree2.pack(side="top",pady=5,padx=5,fill="x")

##def query_frage_table():
##    global frage_count
##    frage_count = 0
##
##    mysql_cursor.execute("SELECT * FROM frage_table ORDER BY frage_id;") 
##    frage_table_records = mysql_cursor.fetchall()
##    
##    ##print(frage_table_records)
##    for record in frage_table_records:
###    if frage_count % 2 == 0:
##        try:
##            tree.insert(parent="",index="end", iid=frage_count, values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6])) # tags="evenrow"
##            frage_count +=1
##        except:
##            frage_count +=1
##            return
####    else:
####        tree.insert(parent="",index="end",iid=frage_count, values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6])) # tags = "oddrow"
##    frage_count +=1
##    print(frage_count)
##query_frage_table()


def query_frage_table():
    mysql_cursor.execute("SELECT * FROM frage_table ORDER BY frage_id;") 
    frage_table_records = mysql_cursor.fetchall()
    #print(frage_table_records)
    ##for index, record in enumerate(frage_table_records):
    for record in frage_table_records:
        ##num = 0
        ##id_reference = str(record[0])
        ##add_answer_button = customtkinter.CTkButton(tree, text="Edit " + id_reference, width=25,height=15)
        ##add_answer_button.grid(row=index, column=num)
        tree.insert(parent="", index="end", iid=record[0], values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6]))
        
query_frage_table()

def query_antwort_table():
    mysql_cursor.execute("SELECT * FROM antwort_table ORDER BY antwort_id;") 
    antwort_table_records = mysql_cursor.fetchall()
    ##print(antwort_table_records)
    for record in antwort_table_records:
        tree2.insert(parent="",index="end", iid=record[0], values=(record[0],record[1],record[2],record[3],record[4])) 

query_antwort_table()

def update_treeview_frage_table(sql_query):
    for tree_child in tree.get_children(): #destroy the treeview
        ##print(tree.get_children())
        tree.delete(tree_child)
    try:
        mysql_cursor.execute(sql_query) # get new data for treeview
        frage_table_records = mysql_cursor.fetchall()
    except:
        mysql_cursor.close()
        create_mysql_cursor()
        query_frage_table()
        return
    ##frage_table_records.reverse()
    try:
        for record in frage_table_records:
            tree.insert(parent="", index="end", iid=record[0], values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6]))
    except:
        print("Couldn't update treeview [frage_table]!")
        return


def update_treeview_antwort_table(sql_query2):
    for tree2_child in tree2.get_children(): #destroy the second treeview
        ##print(tree2.get_children())
        tree2.delete(tree2_child)
    try:
        mysql_cursor.execute(sql_query2) # get new data for treeview
        antwort_table_records = mysql_cursor.fetchall()
    ##antwort_table_records.reverse()
    except:
        mysql_cursor.close()
        create_mysql_cursor()
        query_antwort_table()
        return
    try:
        for record in antwort_table_records:
            tree2.insert(parent="",index="end", iid=record[0], values=(record[0],record[1],record[2],record[3],record[4])) # create new treeview with new data
    except:
        print("Couldn't update treeview [antwort_table]!")
        return



def mcfrb_answer_label_query(event): # function which sends a query, whenever an entry in tree2 is clicked, getting the current answer from the db
    current_tree2_focus=tree2.focus()
    delete_answer_button.configure(text= f"Antwort mit ID: {current_tree2_focus} löschen ")
    edit_answer_button.configure(text= f"Antwort mit ID: {current_tree2_focus} bearbeiten ")

    sql_query_mcfrb_answer_label = (f"SELECT * FROM antwort_table WHERE antwort_id ='{current_tree2_focus}';")
    mysql_cursor.execute(sql_query_mcfrb_answer_label)
    mcfrb_answer_label_data = mysql_cursor.fetchall()
    ##print(mcfrb_answer_label_data)
    mcfrb_answer_label["text"]=f"""{mcfrb_answer_label_data[0][2]}
    """
    antwort_question_id = str(mcfrb_answer_label_data[0][3])
    ##print(antwort_question_id)

    sql_query_mcfrb_question_label = (f"SELECT * FROM frage_table WHERE frage_id ='{antwort_question_id}';")
    try:
        mysql_cursor.execute(sql_query_mcfrb_question_label)
        mcfrb_question_label_data = mysql_cursor.fetchall()
        mcfrb_question_label["text"]=f"""{mcfrb_question_label_data[0][1]}
        """
    except:
        print("Error while searching for question ID!")
        return
    ##print(mcfrb_question_label_data)
    question_antwort_id = str(mcfrb_question_label_data[0][4])
tree2.bind('<Button-1>', mcfrb_answer_label_query)


def mcfrb_question_label_query(event): # function which sends a query, whenenever an entry in tree is clicked, getting the current question from the DB
    current_tree_focus=tree.focus()
    delete_question_button.configure(text= f"Frage mit ID: {current_tree_focus} löschen ")
    edit_question_button.configure(text= f"Frage mit ID: {current_tree_focus} bearbeiten ")

    sql_query_mcfrb_question_label = (f"SELECT * FROM frage_table WHERE frage_id ='{current_tree_focus}';")
    mysql_cursor.execute(sql_query_mcfrb_question_label)
    mcfrb_question_label_data = mysql_cursor.fetchall()
    ##print(mcfrb_question_label_data)
    mcfrb_question_label["text"]=f"""{mcfrb_question_label_data[0][1]}
    """
    question_antwort_id = str(mcfrb_question_label_data[0][4])
    ##print(question_antwort_id)

    sql_query_mcfrb_answer_label = (f"SELECT * FROM antwort_table WHERE antwort_id ='{question_antwort_id}';")
    try:
        mysql_cursor.execute(sql_query_mcfrb_answer_label)
        mcfrb_answer_label_data = mysql_cursor.fetchall()
        mcfrb_answer_label["text"]=f"""{mcfrb_answer_label_data[0][2]}
        """
    except:
        print("Error question does not have an answer!")
        return
    ##print(mcfrb_answer_label_data)
tree.bind('<Button-1>', mcfrb_question_label_query)

def delete_answer():
    try:
        current_tree2_focus = tree2.focus()
        mysql_cursor.execute(f"DELETE FROM antwort_table WHERE antwort_id = '{current_tree2_focus}';)")
        deleted_answer = mysql_cursor.fetchall()
        ##print(deleted_answer)
        update_treeview_antwort_table()
    except:
        mysql_cursor.close()
        create_mysql_cursor()
        try:
            query_frage_table()
            query_antwort_table()
        except:
            update_treeview_antwort_table()
            update_treeview_frage_table()
    return

##def delete_answer_window():
##    delete_answer_yesno = tk.messagebox.askyesno('Datensatz Antwort löschen', 'Möchten Sie die Antwort wirklich Löschen ?')
##    if delete_answer_yesno == "Ja" or "Yes" or "ja" or "yes":
##        delete_answer()
##    else:
##        return
##    for tree_child in tree.get_children(): #destroy the treeview
##        ##print(tree.get_children())
##        tree.delete(tree_child)
##    ##query_frage_table()

def delete_question():
    try:
        current_tree_focus = tree.focus()
        mysql_cursor.execute(f"DELETE FROM frage_table WHERE frage_id = '{current_tree_focus}';)")
        deleted_question = mysql_cursor.fetchall()
        ##print(deleted_question)
        update_treeview_frage_table()
    except:
        mysql_cursor.close()
        create_mysql_cursor()
        try:
            query_frage_table()
            query_antwort_table()
        except:
            update_treeview_antwort_table()
            update_treeview_frage_table()
    return

##def delete_question_window():
##    delete_question_yesno = tk.messagebox.askyesno('Datensatz Frage löschen', 'Möchten Sie die Frage wirklich Löschen ?')
##    if delete_question_yesno == "Ja" or "Yes" or "ja" or "yes":
##        delete_question()
##    else:
##        return
##    for tree2_child in tree2.get_children(): #destroy the treeview
##        ##print(tree.get_children())
##        tree2.delete(tree2_child)
##    ##query_antwort_table()


##def update_all():
##    ##try:
##    update_treeview_frage_table("SELECT * FROM frage_table ORDER BY frage_id;")
##    updated_treeview_frage_table_result = mysql_cursor.fetchall()
##    ##except:
##    ##print("Error couldn't update treeview of frage table!")
##    ##print(updated_treeview_frage_table_result)
##    ##try:
##    update_treeview_antwort_table("SELECT * FROM antwort_table ORDER BY antwort_id;")
##    updated_treeview_antwort_table_result = mysql_cursor.fetchall()
##    ##except:
##    ##print("Error couldn't update treeview of antwort table!")
##    ##print(updated_treeview_antwort_table_result)

def edit_question():
    current_tree_focus = tree.focus()
    edit_question_window = customtkinter.CTkToplevel(app) #create toplevel window

    edit_question_window.geometry("900x650") # window size
    edit_question_window.attributes("-topmost", True)# set topmost
    edit_question_window.title("FAQEL - Frage bearbeiten") # window title 

    edit_question_window.grab_set() # set grab focus

    edit_question_query_sql = f"""
    SELECT * FROM frage_table WHERE frage_id = '{current_tree_focus}';
    """
    mysql_cursor.execute(edit_question_query_sql)
    edit_question_query_result = mysql_cursor.fetchall()
    edit_question_query_result = edit_question_query_result[0]
    ##print(edit_question_query_result)

    edit_question_frame = customtkinter.CTkFrame(master=edit_question_window,width=900,height=650,corner_radius=15)
    edit_question_frame.pack(side="top", pady=5, padx=5, fill="both")


    value0_frame = customtkinter.CTkFrame(master=edit_question_frame,corner_radius=15) #0
    value0_frame.pack(side="top", pady=5, padx=5, fill="both")

    value0_label = customtkinter.CTkLabel(master=value0_frame, text=f"Frage ID {edit_question_query_result[0]} ")
    value0_label.pack(side="top", pady=5, padx=5, fill="both")


    value1_frame = customtkinter.CTkFrame(master=edit_question_frame,corner_radius=15) #1
    value1_frame.pack(side="top", pady=5, padx=5, fill="both")

    value1_label = customtkinter.CTkLabel(master=value1_frame, text=f"Frage: {edit_question_query_result[1]} ")
    value1_label.pack(side="top", pady=5, padx=5, fill="both")

    value1_entry = customtkinter.CTkEntry(master=value1_frame, placeholder_text=f"{edit_question_query_result[1]}") 
    value1_entry.pack(pady=5, padx=5, fill="both")


    value2_frame = customtkinter.CTkFrame(master=edit_question_frame,corner_radius=15) #2
    value2_frame.pack(side="top", pady=5, padx=5, fill="both")

    value2_label = customtkinter.CTkLabel(master=value2_frame, text=f"Datum: {edit_question_query_result[2]}")
    value2_label.pack(side="top", pady=5, padx=5, fill="both")

    value2_entry = customtkinter.CTkEntry(master=value2_frame, placeholder_text=f"{edit_question_query_result[2]}") 
    value2_entry.pack(pady=5, padx=5, fill="both")


    value3_frame = customtkinter.CTkFrame(master=edit_question_frame,corner_radius=15) #3
    value3_frame.pack(side="top", pady=5, padx=5, fill="both")

    value3_label = customtkinter.CTkLabel(master=value3_frame, text=f"Beantwortet: {edit_question_query_result[3]} ")
    value3_label.pack(side="top", pady=5, padx=5, fill="both")

    value3_entry = customtkinter.CTkEntry(master=value3_frame, placeholder_text=f"{edit_question_query_result[3]}") 
    value3_entry.pack(pady=5, padx=5, fill="both")


    value4_frame = customtkinter.CTkFrame(master=edit_question_frame,corner_radius=15) #4
    value4_frame.pack(side="top", pady=5, padx=5, fill="both")

    value4_label = customtkinter.CTkLabel(master=value4_frame, text=f"Antwort ID: {edit_question_query_result[4]} ")
    value4_label.pack(side="top", pady=5, padx=5, fill="both")

    value4_entry = customtkinter.CTkEntry(master=value4_frame, placeholder_text=f"{edit_question_query_result[4]}") 
    value4_entry.pack(pady=5, padx=5, fill="both")


    value5_frame = customtkinter.CTkFrame(master=edit_question_frame,corner_radius=15) #5
    value5_frame.pack(side="top", pady=5, padx=5, fill="both")

    value5_label = customtkinter.CTkLabel(master=value5_frame, text=f"Tags: {edit_question_query_result[5]} ")
    value5_label.pack(side="top", pady=5, padx=5, fill="both")

    value5_entry = customtkinter.CTkEntry(master=value5_frame, placeholder_text=f"{edit_question_query_result[5]}") 
    value5_entry.pack(pady=5, padx=5, fill="both")


    value6_frame = customtkinter.CTkFrame(master=edit_question_frame,corner_radius=15) #6
    value6_frame.pack(side="top", pady=5, padx=5, fill="both")

    value6_label = customtkinter.CTkLabel(master=value6_frame, text=f"Nutzer ID: {edit_question_query_result[6]} ")
    value6_label.pack(side="top", pady=5, padx=5, fill="both")

    value6_entry = customtkinter.CTkEntry(master=value6_frame, placeholder_text=f"{edit_question_query_result[6]}") 
    value6_entry.pack(pady=5, padx=5, fill="both")

    def send_updated_question():
        value1_entry_result = value1_entry.get() # frage
        value2_entry_result = value2_entry.get() # frage_datum
        value3_entry_result = value3_entry.get() # beantwortet
        value4_entry_result = value4_entry.get() # antwort_id
        value5_entry_result = value5_entry.get() # tags
        value6_entry_result = value6_entry.get() # nutzer_id

        send_updated_value1 = f"""
        UPDATE frage_table
        SET frage = '{value1_entry_result}'
        WHERE frage_id ='{current_tree_focus}';
        """
        send_updated_value2 = f"""
        UPDATE frage_table
        SET frage_datum = '{value2_entry_result}'
        WHERE frage_id ='{current_tree_focus}';
        """
        send_updated_value3 = f"""
        UPDATE frage_table
        SET beantwortet = '{value3_entry_result}'
        WHERE frage_id ='{current_tree_focus}';
        """
        send_updated_value4 = f"""
        UPDATE frage_table
        SET antwort_id = '{value4_entry_result}'
        WHERE frage_id ='{current_tree_focus}';
        """
        send_updated_value5 = f"""
        UPDATE frage_table
        SET tags = '{value5_entry_result}'
        WHERE frage_id ='{current_tree_focus}';
        """
        send_updated_value6 = f"""
        UPDATE frage_table
        SET nutzer_id = '{value6_entry_result}'
        WHERE frage_id ='{current_tree_focus}';
        """
        try:
            mysql_cursor.execute(send_updated_value1)
        except:
            print("Error while Updating value1")
        try:
            mysql_cursor.execute(send_updated_value2)
        except:
            print("Error while Updating value3")
        try:
            mysql_cursor.execute(send_updated_value3)
        except:
            print("Error while Updating value3")
        try:
            mysql_cursor.execute(send_updated_value4)
        except:
            print("Error while Updating value4")
        try:
            mysql_cursor.execute(send_updated_value5)
        except:
            print("Error while Updating value5")
        try:
            mysql_cursor.execute(send_updated_value6)
        except:
            print("Error while Updating value6")
        
        update_treeview_frage_table("SELECT * FROM frage_table ORDER BY frage_id;")
        edit_question_window.destroy()

    confirm_edit_button = customtkinter.CTkButton(master=edit_question_window,text="Fertig ", command=send_updated_question) # login button within function/toplevel window
    confirm_edit_button.pack(side="top", pady=5, padx=5, fill="both")


    cancel_button = customtkinter.CTkButton(fg_color="orange",hover_color="red", master=edit_question_window,text="Schließen ", text_color="black", command=lambda:[edit_question_window.grab_release(),edit_question_window.destroy(),update_answer()]) #cancelbutton 
    cancel_button.pack(side="top",pady=5, padx=5, fill="both")

    value1_entry.insert(0, edit_question_query_result[1])
    value2_entry.insert(0, edit_question_query_result[2])
    value3_entry.insert(0, edit_question_query_result[3])
    value4_entry.insert(0, edit_question_query_result[4])
    value5_entry.insert(0, edit_question_query_result[5])
    value6_entry.insert(0, edit_question_query_result[6])



def edit_answer():
    current_tree2_focus = tree2.focus()
    edit_answer_window = customtkinter.CTkToplevel(app) #create toplevel window

    edit_answer_window.geometry("900x500") # window size
    edit_answer_window.attributes("-topmost", True)# set topmost
    edit_answer_window.title("FAQEL - Frage bearbeiten") # window title 

    edit_answer_window.grab_set() # set grab focus

    edit_question_query_sql = f"""
    SELECT * FROM antwort_table WHERE antwort_id = '{current_tree2_focus}';
    """
    mysql_cursor.execute(edit_question_query_sql)
    edit_answer_query_result = mysql_cursor.fetchall()
    edit_answer_query_result = edit_answer_query_result[0]
    ##print(edit_answer_query_result)

    edit_answer_frame = customtkinter.CTkFrame(master=edit_answer_window,width=900,height=650,corner_radius=15)
    edit_answer_frame.pack(side="top", pady=5, padx=5, fill="both")


    value0_answer_frame = customtkinter.CTkFrame(master=edit_answer_frame,corner_radius=15) #0
    value0_answer_frame.pack(side="top", pady=5, padx=5, fill="both")

    value0_answer_label = customtkinter.CTkLabel(master=value0_answer_frame, text=f"Antwort ID {edit_answer_query_result[0]} ")
    value0_answer_label.pack(side="top", pady=5, padx=5, fill="both")


    value1_answer_frame = customtkinter.CTkFrame(master=edit_answer_frame,corner_radius=15) #1
    value1_answer_frame.pack(side="top", pady=5, padx=5, fill="both")

    value1_answer_label = customtkinter.CTkLabel(master=value1_answer_frame, text=f"Antwort Datum: {edit_answer_query_result[1]} ")
    value1_answer_label.pack(side="top", pady=5, padx=5, fill="both")

    value1_answer_entry = customtkinter.CTkEntry(master=value1_answer_frame, placeholder_text=f"{edit_answer_query_result[1]}") 
    value1_answer_entry.pack(pady=5, padx=5, fill="both")


    value2_answer_frame = customtkinter.CTkFrame(master=edit_answer_frame,corner_radius=15) #2
    value2_answer_frame.pack(side="top", pady=5, padx=5, fill="both")

    value2_answer_label = customtkinter.CTkLabel(master=value2_answer_frame, text=f"Antwort: {edit_answer_query_result[2]}")
    value2_answer_label.pack(side="top", pady=5, padx=5, fill="both")

    value2_answer_entry = customtkinter.CTkEntry(master=value2_answer_frame, placeholder_text=f"{edit_answer_query_result[2]}") 
    value2_answer_entry.pack(pady=5, padx=5, fill="both")


    value3_answer_frame = customtkinter.CTkFrame(master=edit_answer_frame,corner_radius=15) #3
    value3_answer_frame.pack(side="top", pady=5, padx=5, fill="both")

    value3_answer_label = customtkinter.CTkLabel(master=value3_answer_frame, text=f"Frage ID: {edit_answer_query_result[3]} ")
    value3_answer_label.pack(side="top", pady=5, padx=5, fill="both")

    value3_answer_entry = customtkinter.CTkEntry(master=value3_answer_frame, placeholder_text=f"{edit_answer_query_result[3]}") 
    value3_answer_entry.pack(pady=5, padx=5, fill="both")


    value4_answer_frame = customtkinter.CTkFrame(master=edit_answer_frame,corner_radius=15) #4
    value4_answer_frame.pack(side="top", pady=5, padx=5, fill="both")

    value4_answer_label = customtkinter.CTkLabel(master=value4_answer_frame, text=f"Nutzer ID: {edit_answer_query_result[4]} ")
    value4_answer_label.pack(side="top", pady=5, padx=5, fill="both")

    value4_answer_entry = customtkinter.CTkEntry(master=value4_answer_frame, placeholder_text=f"{edit_answer_query_result[4]}") 
    value4_answer_entry.pack(pady=5, padx=5, fill="both")


    def send_updated_question():
        value1_entry_result = value1_answer_entry.get() # antwort_datum
        value2_entry_result = value2_answer_entry.get() # antwort
        value3_entry_result = value3_answer_entry.get() # frage_id
        value4_entry_result = value4_answer_entry.get() # nutzer_id


        send_updated_value1 = f"""
        UPDATE antwort_table
        SET antwort_datum = '{value1_entry_result}'
        WHERE antwort_id ='{current_tree2_focus}';
        """
        send_updated_value2 = f"""
        UPDATE antwort_table
        SET antwort = '{value2_entry_result}'
        WHERE antwort_id ='{current_tree2_focus}';
        """
        send_updated_value3 = f"""
        UPDATE antwort_table
        SET frage_id = '{value3_entry_result}'
        WHERE antwort_id ='{current_tree2_focus}';
        """
        send_updated_value4 = f"""
        UPDATE antwort_table
        SET antwort_id = '{value4_entry_result}'
        WHERE antwort_id ='{current_tree2_focus}';
        """

        try:
            mysql_cursor.execute(send_updated_value1)
        except:
            print("Error while Updating value1")
        try:
            mysql_cursor.execute(send_updated_value2)
        except:
            print("Error while Updating value3")
        try:
            mysql_cursor.execute(send_updated_value3)
        except:
            print("Error while Updating value3")
        try:
            mysql_cursor.execute(send_updated_value4)
        except:
            print("Error while Updating value4")

        
        update_treeview_antwort_table("SELECT * FROM antwort_table ORDER BY antwort_id;")
        edit_answer_window.destroy()

    confirm_edit_button = customtkinter.CTkButton(master=edit_answer_window,text="Fertig ", command=send_updated_question) # login button within function/toplevel window
    confirm_edit_button.pack(side="top", pady=5, padx=5, fill="both")

    cancel_button = customtkinter.CTkButton(fg_color="orange",hover_color="red", master=edit_answer_window,text="Schließen ", text_color="black", command=lambda:[edit_answer_window.grab_release(),edit_answer_window.destroy(),update_answer()]) #cancelbutton 
    cancel_button.pack(side="top",pady=5, padx=5, fill="both")

    value1_answer_entry.insert(0, edit_answer_query_result[1])
    value2_answer_entry.insert(0, edit_answer_query_result[2])
    value3_answer_entry.insert(0, edit_answer_query_result[3])
    value4_answer_entry.insert(0, edit_answer_query_result[4])





refresh_button = customtkinter.CTkButton(master=searchbar_frame,fg_color="#21a366", width=60,height=30,text="Aktualisieren", command=lambda:[update_treeview_antwort_table("SELECT * FROM antwort_table ORDER BY antwort_id;"),update_treeview_frage_table("SELECT * FROM frage_table ORDER BY frage_id;")]) #press this button to refresh the view
refresh_button.pack(side="right",pady=5,padx=5)


del_edit_question_button_frame = customtkinter.CTkFrame(master=mcfrb_question_label_frame,corner_radius=15)
del_edit_question_button_frame.pack(side="top",pady=5,padx=5,fill="both")

delete_question_button = customtkinter.CTkButton(master=del_edit_question_button_frame,fg_color="#ff8903", width=200,height=30,text=f"Frage mit ID: {current_tree_focus} löschen ", hover_color="red",command=delete_question) #press this button to refresh the view
delete_question_button.pack(side="bottom",pady=5,padx=5,fill="y")

edit_question_button = customtkinter.CTkButton(master=del_edit_question_button_frame,fg_color="#21a366", width=350,height=30,text=f"Frage mit ID: {current_tree_focus} bearbeiten ", command=edit_question) #press this button to refresh the view
edit_question_button.pack(side="bottom",pady=5,padx=5,fill="both")

##tree.bind('<Button-1>', update_button_label_question)

del_edit_answer_button_frame =customtkinter.CTkFrame(master=mcfrb_answer_label_frame,corner_radius=15)
del_edit_answer_button_frame.pack(side="top",pady=5,padx=5,fill="both")

delete_answer_button = customtkinter.CTkButton(master=del_edit_answer_button_frame,fg_color="#ff8903", width=200,height=30,text=f"Antwort mit ID:{current_tree2_focus} löschen ",hover_color="red", command=delete_answer) #press this button to refresh the view
delete_answer_button.pack(side="bottom",pady=5,padx=5,fill="y")

edit_answer_button = customtkinter.CTkButton(master=del_edit_answer_button_frame,fg_color="#21a366", width=350,height=30,text=f"Antwort mit ID: {current_tree2_focus} bearbeiten ", command=edit_answer) #press this button to refresh the view
edit_answer_button.pack(side="bottom",pady=5,padx=5,fill="both")

##tree2.bind('<Button-1>', update_button_label_answer)

##def edit_now(id,index):
##    pass


##    else:
##        tree.insert(parent="",index="end",iid=antwort_count, values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6])) # tags = "oddrow"


##scrollbar = tk.ttk.Scrollbar(main_content_frame_left, orient=tk.VERTICAL, command=tree.yview)
##tree.configure(yscroll=scrollbar.set)
##scrollbar.pack(side="right", fill="y")

##scrollbar = tk.ttk.Scrollbar(main_content_frame_left, orient=tk.HORIZONTAL, command=tree.xview)
##tree.configure(xscroll=scrollbar.set)
##scrollbar.grid(row=1, column=0, sticky='s')


def tasks(): # consider this like a "secondary" loop to run any functions in
    get_current_wh()
    global current_tree_focus # set tree2.focus as global variable to be used in other functions
    current_tree_focus = tree.focus()
    global current_tree2_focus # set tree2.focus as global variable to be used in other functions
    current_tree2_focus = tree2.focus()
    #print(current_tree_focus)
    #print(current_tree2_focus)

    ##current_selection_tree1 = tree.get_children()
    ##current_selection_tree2 = tree2.selection()

    ##print(current_selection_tree1,current_selection_tree2)
    ##print(current_wh_list[0]//2)
    ##main_content_frame_left.config(width=current_wh_list[0]//2) #dynamically update the width of the given frames
    ##main_content_frame_right_top.config(width=current_wh_list[0]//2.2)
    ##main_content_frame_right_bottom.config(width=current_wh_list[0]//2.5)
    ##main_content_frame_right_top.config(height=current_wh_list[1]//2.1)#dynamically update the height of given frames
    ##main_content_frame_right_bottom.config(height=current_wh_list[1]//2.4)
    ##mysql_cursor.execute("DELETE FROM frage_table WHERE frage=' ' OR frage IS NULL;")
    #print(current_wh_list)
    app.after(75,tasks)
    #print(main_content_frame_right_bottom.winfo_width())
    #print(current_wh_list)
if __name__ == "__main__":
    #app.eval('tk::PlaceWindow . right_top')
    app.after(75,tasks)
    print(current_wh_list)
    app.mainloop() #this is the tkinter mainloop, this ensures the program updates all the content/events (atleast anything relating to tkinter), any code after this will not be executed (in the mainloop)