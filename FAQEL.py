# FAQEL https://github.com/spyridongeorgiou/FAQEL
# Written by Spyridon Georgiou https://github.com/spyridongeorgiou
# See license(s) for usage

# comments starting with ## are marked as code which may be useful for debugging or may be worked on in a future release
# comments eclosed with ###  are just used to better visualize where different parts of code start

import tkinter as tk # GUI framework
import tkinter.messagebox # warning pop up
import customtkinter # Main GUI module used in this program. Credit goes to https://github.com/TomSchimansky/CustomTkinter
import mysql.connector # importing our connector  to connect 
from mysql.connector import errorcode
import sqlite3 # use sqlite to create a local database in case you do not have internet or the firewall blocks the connection
import csv # in order to open the mysqlconfig.csv, this can be omitted however if you just enter the credentials directly into the config dictionary
import sys # check current python version
import os # for OS interaction, mainly to ensure the DB file is in the same directory the program is running as
import datetime # for getting current date to pass into DB
##import logging

program_version = "1.0.3"
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

app.geometry(f"{int(screen_width//1.5)}x{int(screen_height//1.5)}") # setting window size
#print((f"Resolution:{screen_width}x{screen_height}"))
app.title("FAQEL") # the desired app name

# get current width and height of the monitor
# useful for sizing the window appropriately relative to monitor size
def get_current_wh():
    global current_wh_list
    current_h_app = app.winfo_height()
    current_w_app = app.winfo_width()
    current_wh_list = [current_w_app,current_h_app]
    return


# open the main config to connecting to your desired database
with open("mysqlconfig.csv","r") as configfile:
    reader = csv.reader(configfile)
    data = list(reader)
print(data)

# the main config to connecting to your desired database
config = {
  "user": data[1][3],
  "password": data[1][4],
  "host": data[1][0],
  "database": data[1][2],
  "port": int(data[1][1]),
  "raise_on_warnings": True
}

try:
    # Make sure to find the file.db in the script directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
    db_path = os.path.join(BASE_DIR, "FAQELSQL.db")
    conn = sqlite3.connect(db_path)

except sqlite3.Error as error:
    print("Failed to read data from sqlite table", error)

sqlite_cursor = conn.cursor() #create the sqlite3 cursor

try:
    cnx = mysql.connector.connect(**config)
    mysql_cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password!")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist!")
    else:
        print(err)

        ## open the default config for sqlite db
        ##with open("mysqlconfigdefault.csv","r") as defaultconfigfile:
        ##    reader = csv.reader(defaultconfigfile)
        ##    data = list(reader)

        print("Connecting to local DB!")
        try:
            create_nutzer_table = ("""
                CREATE TABLE IF NOT EXISTS 
                nutzer_table (
                nutzer_id ID INTEGER PRIMARY KEY ,
                benutzername VARCHAR (255),
                vorname VARCHAR (255) ,
                nachname VARCHAR (255);
                ) """)

            create_frage_table = ("""
                CREATE TABLE IF NOT EXISTS 
                frage_table (
                frage_id ID INTEGER PRIMARY KEY,
                frage TEXT NOT NULL, 
                beantwortet BOOLEAN
                tags VARCHAR(32);
                ) """)
    
            create_antwort_table = ("""
                CREATE TABLE IF NOT EXISTS 
                antwort_table (
                antwort_id ID INTEGER PRIMARY KEY ,
                antwort_datum DATE NOT NULL,
                antwort TEXT NOT NULL,
                FOREIGN KEY (fragen_id) REFERENCES frage_table(frage_id); ,
                FOREIGN KEY (nutzer_id) REFERENCES nutzer_table(nutzer_id);
                ) """)

    
            sqlite_cursor.execute(create_nutzer_table) # create antwort_table in sqlite
            print("Table nutzer_table created successfully!")
            sqlite_cursor.execute(create_antwort_table) # create antwort_table in sqlite
            print("Table antwort_table created successfully!")
            sqlite_cursor.execute(create_frage_table) # create nutzer_table in sqlite
            print("Table nutzer_table created successfully")
            print("Database successfully created!")
        except:
            print("Error: Database exists already!")
mysqlite_connection = cnx
### creating the tables in MySQL 8 ###

### NOTE (to self): use this if you have to nuke the database ###
##mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
##mysql_cursor.execute("DROP TABLE IF EXISTS nutzer_table;")
##mysql_cursor.execute("DROP TABLE IF EXISTS frage_table;")
##mysql_cursor.execute("DROP TABLE IF EXISTS antwort_table;")
##mysql_cursor.execute("DROP TABLE IF EXISTS secret_table;")

### this DB will pretty much only be created once NOTE: perhaps move this into a seperate script?###

cnx = mysql.connector.connect(**config)

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


##mysql_cursor.execute(f"INSERT INTO frage_table (frage_id,frage,frage_datum,tags,nutzer_id) VALUES ('1','Was ist FAQEL?','2022-06-07','FAQEL','1');")
##mysql_cursor.execute(f"INSERT INTO frage_table (frage_id,frage,frage_datum,tags,nutzer_id) VALUES ('2','Wer hat FAQEL kreeiert?','2022-06-07','FAQEL','1');")
##mysql_cursor.execute(f"INSERT INTO frage_table (frage_id,frage,frage_datum,tags,nutzer_id) VALUES ('3','Wie wurde FAQEL programmiert?','2022-06-07','FAQEL','1');")

def search_event(): # button event handling function
    print("SEARCH")
    ##search_query = squlite_cursor.execute(f"""SELECT * FROM frage_table, antwort_table, nutzer_table WHERE{searchbox.get()}""")
    ##print("1",search_query)
    tkinter.messagebox.showinfo("Kein Resultat", "Leider ergab Ihre Suche kein Resultat!")

##def add_event():
##    cur.execute("INSERT INTO frage (frage) VALUES (f"{frage}")")

def query_antwort():
    print("BEANTWORTET DURCH")
    ##query_antwort = squlite_cursor.execute("""SELECT * FROM antwort_table""")
    ##print(query_antwort)

def add_question():
    print("FRAGE STELLEN")
    add_question_sql = f"""
    INSERT INTO frage_table (frage,frage_datum,nutzer_id) 
    VALUES ('{str(ask_question_entry.get())}','{current_date}','');
    """
    mysql_cursor.execute(add_question_sql)

def send_register_data():
    print("TRANSMITTING REGISTER DATA")
#    register_

#    insert_frage = cur.execute("""
#        INSERT INTO frage_table (
#        frage,beantwortet,nutzerid) VALUES (?,?,?)
#        """)
#    question = (ask_question_entry.get(),False,)

#    cur.commit()
#    return cur.lastrowid


### function to create new toplevel window for the user to login ###

def login_screen(): # CREATE LOGIN TOPLEVEL WINDOW
    ##app.withdraw()
    login_window = customtkinter.CTkToplevel(app) #create toplevel window

    login_window.geometry("400x300") # window size
    login_window.attributes("-topmost", True)# set topmost
    login_window.title("FAQEL - Einloggen") # window title 

    login_window.grab_set() # set grab focus

    username_frame = customtkinter.CTkFrame(master=login_window) # create login frame for entering username and password
    username_frame.pack(side="top", pady=5, padx=5, fill="both")

    password_frame = customtkinter.CTkFrame(master=login_window) # create login frame for entering username and password
    password_frame.pack(side="top", pady=5, padx=5, fill="both")

    username_label = customtkinter.CTkLabel(master=username_frame, text="Nutzername ") # username label 
    username_label.pack(side="left", pady=5, padx=5, fill="both")

    username = customtkinter.CTkEntry(master=username_frame, placeholder_text="Nutzername eingeben...") #username box 
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
    cancel_button = customtkinter.CTkButton(fg_color="orange",hover_color="red", master=login_window,text="Abbrechen ", text_color="black", command=login_window.destroy) #cancelbutton 
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

    username_label = customtkinter.CTkLabel(master=username_frame, text="Nutzername ") # username label 
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

searchbar_frame_options = customtkinter.CTkFrame(master=searchbar_frame_container, width=screen_width//2, height=30, corner_radius=15) # frame container for searchbar options
searchbar_frame_options.pack(side="top", pady=2, fill="both")

searchbar_frame = customtkinter.CTkFrame(master=searchbar_frame_container, width=screen_width//2, height=30, corner_radius=15) # frame container for the searchbar itself
searchbar_frame.pack(side="top", pady=2, fill="both")

searchbutton = customtkinter.CTkButton(master=searchbar_frame, width=5,text="Suchen ", command=search_event,corner_radius=15) #searchbutton
searchbutton.pack(side="left", pady=5, padx=5)

searchbox = customtkinter.CTkEntry(master=searchbar_frame,width=screen_width//2, placeholder_text="Suchen... ") #searchbox top left
searchbox.pack(side="left", pady=5, padx=5, fill="both")

login_button = customtkinter.CTkButton(master=searchbar_frame_options, width=200,height=30,text="Einloggen/Registrieren", command=login_screen, corner_radius=15) #login button top _right_bottom
login_button.pack(side="right", pady=5, padx=5)

# NOTE: Create a function for a toplevel window for the about page

##about_button = customtkinter.CTkButton(master=searchbar_frame_options, width=40, height=20, text="Über FAQEL", fg_color="grey",text_font=["default_theme", 10])
##about_button.pack( )

##version_label = customtkinter.CTkLabel(master=searchbar_frame_options, width=200,height=30,text=combined_version, corner_radius=15) #login button top _right_bottom
##version_label.pack(side="right", pady=5, padx=5)

optionmenu_1 = customtkinter.CTkOptionMenu(searchbar_frame_options, values=["Alle", "Option 2", "Option 42 long long long...","Test"]) # optionmenu 1
optionmenu_1.pack(side="left", pady=5, padx=5)
optionmenu_1.set("Frage gestellt durch")

optionmenu_2 = customtkinter.CTkOptionMenu(searchbar_frame_options, values=["Alle", "Option 42 long long long...","Test"]) # optionmenu 2
optionmenu_2.pack(side="left", pady=5, padx=5)
optionmenu_2.set("Beantwortet durch")

ask_question_frame = customtkinter.CTkFrame(master=main_container, height=50, corner_radius=15) #frame which stores entry aswell as button(s)
ask_question_frame.pack(side="bottom", pady=5, padx=5, fill="both")

ask_question_entry = customtkinter.CTkEntry(master=ask_question_frame,height=50, placeholder_text="Frage eingeben... ")
ask_question_entry.pack(side="top",pady=10, padx=15, fill="both")

ask_question_button = customtkinter.CTkButton(master=ask_question_frame, width=50,height=35, text="Frage stellen", command=add_question)
ask_question_button.pack(side="bottom", pady=10, padx=10, fill="x")

get_current_wh() # call this function, outside the main/secondary loop, once so the current_wh_list isnt empty. perhaps there's a more elegant solution?

main_content_frame_container = customtkinter.CTkFrame(master=main_container,corner_radius=15) # main content frame container
main_content_frame_container.pack(pady=5,padx=5,fill="both")

main_content_frame_left = customtkinter.CTkFrame(master=main_content_frame_container, height=current_wh_list[1]//2, width=current_wh_list[0]//2, corner_radius=15) #main content frame left
main_content_frame_left.pack(side="left",pady=5, padx=5, fill="both")

tabular_header = customtkinter.CTkLabel()

main_content_frame_right_top = customtkinter.CTkFrame(master=main_content_frame_container, height=current_wh_list[1]//2, width=current_wh_list[0]//2, corner_radius=15) # main content frame "right_top"
main_content_frame_right_top.pack(side="top",pady=5, padx=5)

main_content_frame_right_bottom = customtkinter.CTkFrame(master=main_content_frame_container,height=current_wh_list[1]//2, width=current_wh_list[0]//2, corner_radius=15) #main content frame _right_bottom
main_content_frame_right_bottom.pack(side="bottom",pady=5, padx=5, fill="both")

### set up treeview for displaying data from the database

#tableview_style = tk.ttk.Style()
#tableview_style.configure("mystyle.Treeview",background="gray98",foreground="gray10",rowheight="25", fieldbackground="gray24")
#tableview_style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
#tableview_style.map("Treeview",background=[("selected","gray10")])


##labeltest = customtkinter.CTkLabel(searchbar_frame,text=f"{get_current_wh()}")
##labeltest.pack(side="top",fill="x")

#button_2 = customtkinter.CTkButton(master=contentframe1, width=5, text="create toplevel", command=login_screen)
#button_2.pack(pady=12, padx=10)

#button_3 = customtkinter.CTkButton(master=contentframe1,)
#button_3.pack(pady=12, padx=10)

##rows = squlite_cursor.fetchall() #get all rows in the DB

##for row in rows: 
##    print(row) # print out all the content in the rows

def tasks(): # consider this like a "secondary" loop to run any functions in
    get_current_wh()
    ##print(current_wh_list[0]//2)
    main_content_frame_left.config(width=current_wh_list[0]//2) #dynamically update the width of the given frames
    main_content_frame_right_top.config(width=current_wh_list[0]//2)
    main_content_frame_right_bottom.config(width=current_wh_list[0]//2)

    main_content_frame_right_top.config(height=current_wh_list[1]//2.4)#dynamically update the height of given frames
    main_content_frame_right_bottom.config(height=current_wh_list[1]//2)
    #print(current_wh_list)
    app.after(17,tasks)
    #print(main_content_frame_right_bottom.winfo_width())
    #print(current_wh_list)
if __name__ == "__main__":
    #app.eval('tk::PlaceWindow . right_top')
    app.after(17,tasks)
    print(current_wh_list)
    app.mainloop() #this is the tkinter mainloop, this ensures the program updates all the content/events (atleast anything relating to tkinter), any code after this will not be executed (in the mainloop)