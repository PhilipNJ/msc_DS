import customtkinter
from PIL import Image
import os
import sqlite3
from tkinter import PhotoImage,messagebox, Label, ttk
import pandas as pd
import gc
import tkinter as tk
#User defined functions
from project_functions import *
import datetime
import random
from manager_reports import *

#Custom global variables
usn="username"
wal="balance"
glide="Glidecoins"
st="starttrip location"
dt="endtrip location"
ride=None
vehmov=None
vehcharge=None
vehrepair=None
distance=0.0
min_bal=0.0
total_cost=0.0
VID =0
TID=0

#Set the directory's path for the user running the application
current_path = os.path.dirname(os.path.realpath(__file__))
pathdb=str(os.path.dirname(os.path.abspath(__file__)))

#frame creation
customtkinter.set_appearance_mode("dark")
conn = sqlite3.connect(pathdb+"/register.db")

cursor = conn.cursor()

#Database tables commits for 1st time users

cursor.execute('''CREATE TABLE IF NOT EXISTS logindetails (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                usertype TEXT
               )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS walletdetails (
                id INTEGER PRIMARY KEY,
                username TEXT,
                balance TEXT,
                Glidecoins TEXT
               )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS vehicledetails (
                vehicle_no INTEGER PRIMARY KEY,
                vehicle_type TEXT,
                current_location TEXT,
                charge_status TEXT,
                repair_needed TEXT
               )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tripdetails (
                id INTEGER PRIMARY KEY,
                vehicle_no INTEGER,
                start_location TEXT,
                end_location TEXT,
                trip_start_time TEXT,
                trip_end_time TEXT,
                trip_duration float,
                trip_fare float,
                user_id INTEGER
               )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY,
                ride_rating INTEGER,
                ride_issues TEXT,
                app_rating INTEGER,
                how_found TEXT,
                trip_id INTEGER
               )''')

conn.commit()


###################################################################################################

#Function to return all the vehicledetails table
def getvehicledetails():
    cursor.execute('''Select * from vehicledetails where vehicle_type="bike" order by current_location
                   ''')
    conn.commit()
    
    bk=cursor.fetchall()
    # print("Bike: \n",bk)


    cursor.execute('''Select * from vehicledetails where vehicle_type="cycle" order by current_location
                   ''')
    conn.commit()
    
    cy=cursor.fetchall()
    # print("Cycle: \n",cy)

    cursor.execute('''PRAGMA table_info(vehicledetails)
                   ''')
    conn.commit()
    
    ert=cursor.fetchall()
    cols =[x[1] for x in ert]

    # print("Columns: \n",cols)

    return(cols,bk,cy)


#Function to return the number of available bikes and cycles in the selected start location
def getvehicleavail(startloc):
    sp=startloc.split(", ")
    postcd=sp[1]
    cursor.execute('''Select vehicle_type, count(*) as vno from vehicledetails where current_location = ? 
                    and charge_status="Y" and repair_needed="N"
                   group by vehicle_type
                   ''',(postcd,))
    conn.commit()
    row=cursor.fetchall()
    availb=0
    availc=0
    for t in row:
        if t[0]=="bike":
            availb=t[1]
        else:
            availc=t[1]

    return (availb,availc)


#Function to update the tripdetails table with the details of the trip taken by the user
def updatevehicle_tripdetails(trip_st,trip_et,trip_dur,trip_fare):
    sp=st.split(", ")
    postcd=sp[1]
    cursor.execute('''Select vehicle_no from vehicledetails where current_location = ?
                   and vehicle_type=? 
                   and charge_status="Y" and repair_needed="N" 
                   Order by RANDOM() LIMIT 1
                   ''',(postcd,ride))
    conn.commit()
    r=cursor.fetchone()
    vid=r[0]
    print("Vehicle ID: ",vid)
    global VID
    VID=vid

    ep=dt.split(", ")
    postcd1=ep[1]
    cursor.execute('''Update vehicledetails set current_location=?, charge_status="N"
                   where vehicle_no=?''', (postcd1,vid))
    conn.commit()

    cursor.execute('''Select id from logindetails where username =? ''',(usn,))
    conn.commit()

    u=cursor.fetchone()
    uid=u[0]
    print("User_ID:", uid)
    
    cursor.execute('''INSERT INTO tripdetails (user_id, vehicle_no, start_location, end_location, 
                   trip_start_time, trip_end_time, trip_duration, trip_fare)
                    VALUES (?,?,?,?,?,?,?,?);   
                   ''',(uid,vid,st,dt,trip_st,trip_et,trip_dur,trip_fare))
    conn.commit()

    cursor.execute('''select max(id) from tripdetails ''')
    conn.commit()

    d =cursor.fetchone()
    tid=d[0]
    global TID
    TID =tid


#Function to return information about vehicles that needs Charge for the Operator
def vehiclechargeget():
    cursor.execute('''Select vehicle_no, charge_status from 
                   vehicledetails where charge_status="N" ''')
    conn.commit()

    ty=cursor.fetchall()
    df=[]
    df=ty

    cursor.execute('''Select distinct vehicle_no from 
                   vehicledetails where charge_status="N" ''')
    
    conn.commit()

    we=cursor.fetchall()
    df1=[]

    for item in we:
        df1.append(str(item[0]))
        print(item[0])

    return df,df1


#Function to charge the selected vehicles by the Operator
def vehiclechargeset(id):
    id=int(id)

    cursor.execute('''update vehicledetails set charge_status="Y" where vehicle_no=?  ''',(id,))
    conn.commit()

    global vehcharge
    vehcharge="Charged"
    
    messagebox.showinfo('Success',"Vehicle No "+str(id)+" has been successfully charged")


#Function to return the information about the vehicles that needs repair for the Operator
def vehrepairget():
    cursor.execute('''Select vehicle_no, repair_needed from 
                   vehicledetails where repair_needed="Y" ''')
    conn.commit()

    ty=cursor.fetchall()
    df=[]
    df=ty

    cursor.execute('''Select distinct vehicle_no from 
                   vehicledetails where repair_needed="Y" ''')
    
    conn.commit()

    we=cursor.fetchall()
    df1=[]

    for item in we:
        df1.append(str(item[0]))
        print(item[0])

    return df,df1


#Function that repairs the selected vehicle by the Operator
def vehiclerepairset(id):
    id=int(id)

    cursor.execute('''update vehicledetails set repair_needed="N" where vehicle_no=?  ''',(id,))
    conn.commit()

    global vehrepair
    vehrepair="Repaired"
    
    messagebox.showinfo('Success',"Vehicle No "+str(id)+" has been successfully repaired")

#Function to return the available count of both bikes and cycles for all the locations
def vehicleavailloc():
    file=pd.read_csv(pathdb+"/Glasgow_Codes.csv",delimiter=",")
    #add file to sqlite database
    file.to_sql('Glasgow_Codes', conn, if_exists='replace', index=False)
    conn.commit()
 
    zx=getlocation("postcode")
    # rest_lt=list(set(zx)-set(lt))
 
    rest_lt=list(zx)
    #--------------
    cursor.execute('''SELECT G.PostCode AS location,
                    COALESCE(SUM(CASE WHEN V.vehicle_type = 'cycle' THEN 1 ELSE 0 END), 0) AS cycle_cnt,
                    COALESCE(SUM(CASE WHEN V.vehicle_type = 'bike' THEN 1 ELSE 0 END), 0) AS bike_cnt
                    FROM Glasgow_codes G
                    LEFT JOIN vehicledetails V ON G.PostCode = V.current_location
                    GROUP BY G.PostCode;''')
    conn.commit()

    tr=cursor.fetchall()
    lt=[]

    lt=tr
    print(lt)
    # for item in range(len(tr)):
    #     lt.append(tr[item])
    
    return lt,rest_lt


#Function to move the selected type of vehicle from one location to another
def vehiclesetloc(type,currloc,movloc):
    
    print(type,currloc,movloc)

    cursor.execute('''update vehicledetails set current_location= ?
                   where vehicle_no in (select max(vehicle_no) from vehicledetails where 
                   current_location=? and vehicle_type =?)  ''',(movloc,currloc,type))

    conn.commit()

    global vehmov
    vehmov="Moved"

    messagebox.showinfo("Success",type[0].upper()+type[1:]+" has been successfully moved")

#Function to return postcodes or postcodes with streetnames based on the parameter fed 
def getlocation(para):
    file=pd.read_csv(pathdb+"/Glasgow_Codes.csv",delimiter=",")
    if para.lower()=="streetname":
        lt=list(file["Streetname"]+", "+file["PostCode"])
        #lt.insert(0,"")
        return lt
    elif para.lower()=="postcode":
        lt=list(file["PostCode"])
        return lt

#Function that registers a user into the database, specifically tables logindetails and walletdetails
def register(user, passw):
    u=user
    p=passw
    cursor.execute('''INSERT INTO logindetails (username,password,usertype) VALUES (?,?,"u")''',(u,p))
    cursor.execute('''INSERT INTO walletdetails (username,balance,Glidecoins) VALUES (?,0,0)''',(u,))
    messagebox.showinfo("Success", "Registered Successfully")
    
#Function that return the password for the user for login check
def getpassword(username):
    u=username
    cursor.execute("Select password from logindetails where username = ?",(u,))
    conn.commit()
    row= cursor.fetchall()
    try:
        pw= row[0]
        return pw[0]
    except:
        return ""

#Function to return the usertype of the username entered while login
def get_usertype(username):
    cursor.execute("Select usertype from logindetails where username = ?", (username,))
    conn.commit()
    row = cursor.fetchall()
    try:
        usertype = row[0][0]
        return usertype
    except:
        return ""

#Function that checks whether a user exists in the database or not
def checkUID(username):
    u=username
    cursor.execute("Select id from logindetails where username = ?",(u,))
    conn.commit()
    row= cursor.fetchall()
    try:
        pw= row[0]
        return pw[0]
    except:
        return ""

#Function that at any given point returns the wallet balance for the customer
def getbalance(username):
    u=username
    cursor.execute("Select balance from walletdetails where username = ?",(u,))
    conn.commit()
    row = cursor.fetchall()
    return row[0][0]

#Function that adds balance of the wallet of the customer
def addbalance(topup, username):
    u =username
    cursor.execute("Select balance from walletdetails where username = ?",(u,))
    conn.commit()
    row = cursor.fetchall()
    print("Current balance: "+str(row[0]))
    t = row[0]
    r = t[0]
    r = float(r)
    if topup=='':
        topup=0
    else:
        topup=float(topup)
    new_bal = str(r+topup)

    cursor.execute("Update walletdetails set balance=? where username=?",(new_bal,u))
    conn.commit()
    global wal
    wal=new_bal
    if float(new_bal)>0:
        messagebox.showinfo("Balance", "Your Wallet balance is "+new_bal)


#Function that returns the distance in Kilometers for the selected startpoint(st) and endpoint(dt)
def fetch_coordinates_from_csv(st,dt):
    file=pd.read_csv(pathdb+"/Glasgow_Codes.csv",delimiter=",")
    start_streetname = st.split(',')[0]
    end_streetname = dt.split(',')[0]

    selected_start_streets = file[(file['Streetname'] == start_streetname)]
    selected_end_streets = file[(file['Streetname'] == end_streetname)]
    print("Start Streetname:", start_streetname)
    print("End Streetname:", end_streetname)

    start_street_lat = selected_start_streets['Latitude'].iloc[0]
    start_street_long = selected_start_streets['Longitude'].iloc[0]
    end_street_lat = selected_end_streets['Latitude'].iloc[0]
    end_street_long = selected_end_streets['Longitude'].iloc[0]
    print('start lat:', start_street_lat, 'start long:', start_street_long)
    print('end lat:', end_street_lat, 'end long:', end_street_long)
    distance = get_distance(start_street_lat, end_street_lat, start_street_long, end_street_long)
    return distance

#Function to return all the start dates from tripdetails table
def gettripstartdates():
    cursor.execute('''select distinct date(trip_start_time) from tripdetails
                    order by date(trip_start_time)''')
    conn.commit()

    ty=cursor.fetchall()
    startdate =[]

    for _ in ty:
        if str(_[0])!="None":
            startdate.append(str(_[0]))
    
    return startdate

#Function to return all the end dates from tripdetails table
def gettripenddates():
    cursor.execute('''select distinct date(trip_end_time) from tripdetails
                    order by date(trip_end_time)''')
    conn.commit()

    ty=cursor.fetchall()
    enddate =[]

    for _ in ty:
        if str(_[0])!="None":
            enddate.append(str(_[0]))
    
    return enddate



#Function that defines the About Us section
def about():
    messagebox.showinfo('About us',"Here at GlideVolt, sustainability and style coexist. \nWe are a movement that supports clean, green commuting and were founded amidst Scotland's breathtaking scenery. \nWe are more than just a scooter rental service. Our environmentally friendly two-wheelers change urban mobility, appealing to millennials and Generation Z. \nJoin us in the effort to promote responsible transportation, making each trip a mindful excursion.")

#Function that defines the Product section
def product():
    messagebox.showinfo('Product',"We provide two services: \n1. Bike \n2. Cycle. \nPick from any point and drop off any point per your convience. \nOur inbui wallet will make your paymetns hassle free and your ride experience smooth")
 
#Function that defines the Contact Us section
def contactus():
    messagebox.showinfo('Contact us',"Get in touch with us for any queries. \nEmail:contactus@glidevolt.com \nPhone: 0141 123 4567 \nAddress: 123, Glasgow, G1 1AA")


###################################################################################################

class App(customtkinter.CTk):
    width = 1200
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("GlideVolt⚡")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.trip_start_time = None
        self.trip_cost = 0
        self.trip_timer_frame = None
        self.billing_frame = None

        # load and create background image
        
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/test_images/bg_gradient.jpg"),
                                               size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=2)
        self.login_frame.grid(row=0, column=0)

        self.login_label = customtkinter.CTkLabel(self.login_frame, text="GlideVolt⚡", font=customtkinter.CTkFont(size=40, weight="bold"))
        self.login_label.grid(row=0, column=0, columnspan=2, padx=30, pady=10)

        self.login_label2 = customtkinter.CTkLabel(self.login_frame, text="Login Page", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.login_label2.grid(row=1, column=0, columnspan=2, padx=30)

        self.role_var = tk.StringVar()  # create a variable to store the selected role
        self.role_var.set("Select your role")  # set the default selected role
        
        self.role_dropdown = customtkinter.CTkOptionMenu(self.login_frame, variable=self.role_var, values=["Customer", "Operator", "Manager"])
        self.role_dropdown.grid(row=2, column=1, padx=30, pady=10)

        self.about_button1 = customtkinter.CTkButton(self.login_frame, text="About", command=about, width=50, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.about_button1.grid(row=2, column=0, padx=30, pady=10)

        self.product_button1 = customtkinter.CTkButton(self.login_frame, text="Products", command=product, width=50, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.product_button1.grid(row=3, column=0, padx=30, pady=10)

        self.contact_button1 = customtkinter.CTkButton(self.login_frame, text="Contact Us", command=contactus, width=50, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.contact_button1.grid(row=4, column=0, padx=30, pady=10)

        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=3, column=1, pady=(5, 15))

        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=4, column=1, padx=30, pady=(0, 15))

        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=5, column=1, padx=30, pady=(0, 15))

        self.register_button = customtkinter.CTkButton(self.login_frame, text="New? Register", command=self.register_button_pressed, width=200)
        self.register_button.grid(row=6, column=1, padx=30, pady=(0, 15))




        # create register frame
        self.register_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.register_frame.grid(row=0, column=0)
        self.register_label = customtkinter.CTkLabel(self.register_frame, text="GlideVolt⚡",
                                                  font=customtkinter.CTkFont(size=40, weight="bold"))

        self.register_label.grid(row=1, column=0, padx=30,pady=10)
       
        self.register_label2 = customtkinter.CTkLabel(self.register_frame, text="Customer Register Page",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))

        self.register_label2.grid(row=2, column=0, padx=30)
        self.register_username_entry = customtkinter.CTkEntry(self.register_frame, width=200, placeholder_text="username")
        self.register_username_entry.grid(row=3, column=0, padx=30, pady=(15, 15))
        self.register_password_entry = customtkinter.CTkEntry(self.register_frame, width=200, show="*", placeholder_text="password")
        self.register_password_entry.grid(row=4, column=0, padx=30, pady=(0, 15))
        self.register_button = customtkinter.CTkButton(self.register_frame, text="Register", command=self.register_event, width=200)
        self.register_button.grid(row=5, column=0, padx=30, pady=(15, 15))
        self.register_login_button = customtkinter.CTkButton(self.register_frame, text="Back to Login", command=self.logout, width=200)
        self.register_login_button.grid(row=7, column=0, padx=30, pady=(15, 15))



        # create main frame
        
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=2)
        self.main_frame.grid(row=0, column=0)
        self.main_label = customtkinter.CTkLabel(self.main_frame, text="Welcome to GlideVolt⚡",
                                                  font=customtkinter.CTkFont(size=40, weight="bold"))
        self.main_label.grid(row=0, column=0,columnspan=2, padx=30, pady=10)

        self.profile_button = customtkinter.CTkButton(self.main_frame, text="Wallet", command = self.show_profile_details, width=50, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.profile_button.grid(row=1, column=0, padx=30, pady=10)

        self.about_button2 = customtkinter.CTkButton(self.main_frame, text="About", command=about, width=50, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.about_button2.grid(row=2, column=0, padx=30, pady=10)

        self.product_button2 = customtkinter.CTkButton(self.main_frame, text="Products", command=product, width=50, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.product_button2.grid(row=3, column=0, padx=30, pady=10)

        self.contact_button2 = customtkinter.CTkButton(self.main_frame, text="Contact Us", command=contactus, width=50, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.contact_button2.grid(row=4, column=0, padx=30, pady=10)


        self.main_label2 = customtkinter.CTkLabel(self.main_frame, text="Please select trip Origin",
                                                  font=customtkinter.CTkFont(size=18, weight="bold"))
        self.main_label2.grid(row=1, column=1, padx=30, pady=10)

        self.start_var = tk.StringVar()  
        self.start_var.set("<Start point>")

        self.starttripdropdown = customtkinter.CTkOptionMenu(self.main_frame,variable=self.start_var, dynamic_resizing=True,
                                                        values=getlocation("streetname"))
        self.starttripdropdown.grid(row=2, column=1, padx=20)


        self.main_label3 = customtkinter.CTkLabel(self.main_frame, text="Please select trip Destination",
                                                  font=customtkinter.CTkFont(size=18, weight="bold"))
        self.main_label3.grid(row=3, column=1, padx=30, pady=10)

        self.end_var = tk.StringVar()  
        self.end_var.set("<End point>")

        self.endtripdropdown = customtkinter.CTkOptionMenu(self.main_frame,variable=self.end_var, dynamic_resizing=True,
                                                        values=getlocation("streetname"))
        self.endtripdropdown.grid(row=4, column=1, padx=20)

        self.next_button = customtkinter.CTkButton(self.main_frame, text="Next →", command=self.tripdetail, width=80, font=customtkinter.CTkFont(size=25, weight="bold"))
        self.next_button.grid(row=5, column=1, padx=30, pady=50)

        self.back_button = customtkinter.CTkButton(self.main_frame, text="Logout", command=self.logout, width=50)
        self.back_button.grid(row=5, column=0, padx=5, pady=10)


         # create pseudo tripcal frame
        self.tripcal_frame =customtkinter.CTkFrame(self,corner_radius=2)
        self.tripcal_frame.grid(row=0, column=0)

        #create pseudo profile frame
        self.profile_frame =customtkinter.CTkFrame(self,corner_radius=2)
        self.profile_frame.grid(row=0, column=0)

        #Frames forget section for initial Login page space
        self.register_frame.grid_forget()
        self.main_frame.grid_forget()
        self.tripcal_frame.grid_forget()
        self.profile_frame.grid_forget()



    def login_event(self):
        print("Login pressed - username:", self.username_entry.get(), "password:", self.password_entry.get(), "roletype:", self.role_dropdown.get())
    
      # Get usertype from database
        stored_usertype = get_usertype(self.username_entry.get())
        role_to_usertype = {
          "Customer": "u",
          "Operator": "o",
          "Manager": "m"
      }

        #Checks the type and validity of the user
        if self.username_entry.get()=="" or self.username_entry.get()==None:
            messagebox.showinfo("Error", "Username Field cannot be empty")
        elif self.password_entry.get()=="" or self.password_entry.get()==None:
            messagebox.showinfo("Error", "Password Field cannot be empty")
        elif self.role_dropdown.get() == "Select your role" or self.role_dropdown.get() is None:
            messagebox.showinfo("Error", "Role Field cannot be empty")
        else:
            pw =getpassword(self.username_entry.get())

        print(pw)
        
        #Password Validation and user direct logic
        if pw=="":
            messagebox.showinfo("Failure", "User Doesnt exist.\nPlease Register")
        elif pw==self.password_entry.get():
            # Check if role selected matches usertype in the database
            if stored_usertype != role_to_usertype.get(self.role_dropdown.get()):
                messagebox.showinfo("Failure", "The role is wrong")
            else:
                global usn 
                usn= self.username_entry.get()
                self.login_frame.grid_forget()  # remove login frame
                if stored_usertype=="o":
                    self.operatorpagemain() #operator frame
                elif stored_usertype=="m":
                    self.managerpagemain() #manager frame
                else:
                    self.main_frame.grid(row=0, column=0)  # show main frame (customer)
        else:
            messagebox.showinfo("Failure", "Wrong Username/Password")


    #Function that forgets the login and main frames and brings up register page
    def register_button_pressed(self):
        print("Registered Button pressed")
        self.login_frame.grid_forget()
        self.main_frame.grid_forget()
        self.register_frame.grid(row=0,column=0)
        self.register_username_entry.delete(0,customtkinter.END)
        self.register_password_entry.delete(0,customtkinter.END)
        

    #Function that checks validity for entries made in register page and the registers the user
    def register_event(self):
        print("Register pressed - username:", self.register_username_entry.get(), "password:", self.register_password_entry.get())

        us=self.register_username_entry.get()

        if self.register_username_entry.get()=="" or self.register_username_entry.get()==None:
            messagebox.showinfo("Error", "Username Field cannot be empty")
        elif self.register_password_entry.get()=="" or self.register_password_entry.get()==None:
            messagebox.showinfo("Error", "Password Field cannot be empty")
        elif isinstance(checkUID(us),int):
            messagebox.showinfo("Error", "User already exist, please choose different username")
        else:
            register(self.register_username_entry.get(),self.register_password_entry.get())
            self.register_frame.grid_forget()
            self.username_entry.delete(0,customtkinter.END)
            self.password_entry.delete(0,customtkinter.END)
            self.login_frame.grid(row=0,column=0)

    #Function to logout from any frame and bring up login frame
    def logout(self):
        try:
            self.main_frame.grid_forget()  # remove main frame
        except:
            pass
        try:
            self.login_frame.grid_forget()
        except:
            pass
        try:
            self.register_frame.grid_forget()
        except:
            pass
        try:
            self.tripcal_frame.grid_forget()
        except:
            pass
        try:
            self.operator_main_frame.grid_forget()
        except:
            pass
        try:
            self.optrack_frame.grid_forget()
        except:
            pass
        try:
            self.opmove_frame.grid_forget()
        except:
            pass
        try:
            self.opcharge_frame.grid_forget()
        except:
            pass
        try:
            self.oprepair_frame.grid_forget()
        except:
            pass
        try:
            self.manager_main_frame.grid_forget()
        except:
            pass
        # self.starttrip.set(getlocation("streetname")[0])
        # self.endtrip.set(getlocation("streetname")[0])
        self.starttripdropdown.set("<Start point>")
        self.endtripdropdown.set("<End point>")
        self.login_frame.grid(row=0, column=0)  # show login frame
        self.username_entry.delete(0,customtkinter.END)
        self.password_entry.delete(0,customtkinter.END)
        self.role_dropdown.set("Select your role")
        self.username_entry.focus()
        gc.collect()

    #Function to call the main frame(Homepage) for customer
    def call_mainframe(self):
        self.login_frame.grid_forget()
        self.register_frame.grid_forget()
        self.profile_frame.grid_forget()
        self.tripcal_frame.grid_forget()
        self.main_frame.grid(row=0, column=0)  # show main frame
        global ride
        ride = None

    #Function to add the balance
    def addbalance2(self):
        topup = self.topup_amount.get()
        addbalance(topup,usn)
        self.login_frame.grid_forget()
        self.register_frame.grid_forget()
        self.profile_frame.grid_forget()
        self.tripcal_frame.grid_forget()
        self.main_frame.grid(row=0, column=0)  # show main frame
        
    #Function to Create the wallet frame
    def show_profile_details(self):
        self.main_frame.grid_forget() 
        self.login_frame.grid_forget()
        self.register_frame.grid_forget()
        global wal
        # create wallet frame
        self.profile_frame =customtkinter.CTkFrame(self,corner_radius=2)
        self.profile_frame.grid(row=0, column=0)

        # Labels displaying user details
        self.nameLabel =customtkinter.CTkLabel(self.profile_frame,text="Hey "+usn[0].upper()+usn[1:]+",\n \nBelow are your Wallet details: ", 
                                                  font=customtkinter.CTkFont(size=20))
        self.nameLabel.grid(row=0,column=0,padx=30, pady=10)
        wal = getbalance(usn)
        self.walletbalance =customtkinter.CTkLabel(self.profile_frame,text="Your wallet balance: "+wal , 
                                                  font=customtkinter.CTkFont(size=20))
        self.walletbalance.grid(row=1,column=0,padx=30, pady=10)

        self.topup_amount = customtkinter.CTkEntry(self.profile_frame, width=200, placeholder_text="Enter Amount here ")
        self.topup_amount.grid(row=2, column=0, padx=30, pady=(15, 15))
        
        #Set topup amount for user session
        global topup
        topup = self.topup_amount.get()

        self.add_balance = customtkinter.CTkButton(self.profile_frame, text= "Topup Your Wallet", command=self.addbalance2, width=50)
        self.add_balance.grid(row=3, column=0, padx=5, pady=30)        

        self.back_button1 = customtkinter.CTkButton(self.profile_frame, text="Back", command=self.call_mainframe, width=50)
        self.back_button1.grid(row=4, column=0, padx=5, pady=30)
    

    #Sets global variable for the ride selected (Cycle)
    def start_cycle_trip(self):
        global ride
        ride="cycle"
        self.select_trip_mode("cycle")


    #Sets global variable for the ride selected (Bike)
    def start_bike_trip(self):
        global ride
        ride="bike"
        self.select_trip_mode("bike")


    #Function to dynamically set message for selected mode on Trip Calculation frame
    def select_trip_mode(self, mode):
        self.trip_mode = mode
        self.tripcalLabel4.configure(text=f"Selected mode of ride: {mode}")



    #Function that validates Minimum Balance required as well as sets ride mode selection dynamically based on its availability
    def start_trip_time(self):  
        global distance
        distance = fetch_coordinates_from_csv(st,dt)

        global min_bal
        min_bal=0.0
        addbalance(0,usn)
        if ride is None:
            messagebox.showinfo("Select", "Please select the ride mode")
        elif ride=="noavail":
            messagebox.showinfo("NA", "No rides are available at this moment, please try again at some later time")
        else:
            if ride =='cycle':
                min_bal = 0.5 * float(distance)
                print('Minimum balance is:' , min_bal)
            elif ride =='bike':
                min_bal = 1 * float(distance)
                print('Minimum balance is:' , min_bal)

        if ride is not None and ride!="noavail":
                if float(wal)>float(min_bal):
                    self.register_frame.grid_forget()
                    self.main_frame.grid_forget()
                    self.tripcal_frame.grid_forget()
                    self.profile_frame.grid_forget()
                    # get the time
                    self.trip_start_time = datetime.datetime.now()
                    self.trip_cost = 0  # renew the money

                    # create the time counting page
                    self.trip_timer_frame = customtkinter.CTkFrame(self, corner_radius=2)
                    self.trip_timer_frame.grid(row=0, column=0)

                    # Create timer label
                    self.timer_label = customtkinter.CTkLabel(self.trip_timer_frame, text="Time Elapsed: 0 seconds", font=customtkinter.CTkFont(size=18))
                    self.timer_label.grid(row=0, column=0, padx=30, pady=10)

                    # Create a fee tag
                    self.cost_label = customtkinter.CTkLabel(self.trip_timer_frame, text="Cost: £0.00", font=customtkinter.CTkFont(size=18))
                    self.cost_label.grid(row=1, column=0, padx=30, pady=10)

                    # Create the "End Trip" button
                    self.end_trip_button = customtkinter.CTkButton(self.trip_timer_frame, text="End Trip", width=80, 
                                                                   font=customtkinter.CTkFont(size=25, weight="bold"), command=self.end_trip)
                    self.end_trip_button.grid(row=2, column=0, padx=5, pady=30)

                    # start the timer label
                    self.update_timer()
                else:
                    messagebox.showinfo('Error',"Insufficient Minimum balance, please topup")
                    self.min_bal_topup_frame()



    def update_timer(self):
        # Update timer label
        if self.trip_start_time is not None:
            current_time = datetime.datetime.now()
            elapsed_time = current_time - self.trip_start_time
            elapsed_seconds = elapsed_time.total_seconds()
            self.timer_label.configure(text=f"Time Elapsed: {elapsed_seconds:.1f} seconds")

            # Renewal cost
            trip_cost = elapsed_seconds * self.get_trip_cost()
            self.trip_cost = trip_cost
            self.cost_label.configure(text=f"Cost: £{trip_cost:.2f}")
            self.trip_timer_frame.after(1000, self.update_timer)


    def end_trip(self):
        end_time = datetime.datetime.now()
        #Calculate the total time
        elapsed_time = end_time - self.trip_start_time
        elapsed_seconds = elapsed_time.total_seconds()

        # Calculate the total cost
        global total_cost
        total_cost = self.get_trip_cost() * elapsed_seconds* distance

        #Create billing page
        self.trip_timer_frame.grid_forget()
        self.billing_frame = customtkinter.CTkFrame(self, corner_radius=2)
        self.billing_frame.grid(row=0, column=0)

        # Displays total time and total cost
        self.thank= customtkinter.CTkLabel(self.billing_frame, text="Thank you for using our Service", font=customtkinter.CTkFont(size=18))
        self.thank.grid(row=1, column=0, padx=30)
        self.total_time_label = customtkinter.CTkLabel(self.billing_frame, text=f"Total Duration: {elapsed_seconds:.1f} seconds", font=customtkinter.CTkFont(size=18))
        self.total_time_label.grid(row=2, column=0, padx=30, pady=10)
        self.total_cost_label = customtkinter.CTkLabel(self.billing_frame, text=f"Total Cost: £{total_cost:.2f}", font=customtkinter.CTkFont(size=18))
        self.total_cost_label.grid(row=3, column=0, padx=30, pady=10)
        self.start_time_label = customtkinter.CTkLabel(self.billing_frame, text=f"Start Time: {self.trip_start_time}", font=customtkinter.CTkFont(size=18))
        self.start_time_label.grid(row=4, column=0, padx=30, pady=10)
        self.end_time_label = customtkinter.CTkLabel(self.billing_frame, text=f"End Time: {end_time}", font=customtkinter.CTkFont(size=18))
        self.end_time_label.grid(row=5, column=0, padx=30, pady=10)
        close_button = customtkinter.CTkButton(self.billing_frame, text="X", width=20, font=customtkinter.CTkFont(size=15), command=self.close_billing)
        close_button.grid(row=0, column=1, padx=5, pady=10)
        #Update tripdetails
        updatevehicle_tripdetails(self.trip_start_time,end_time,elapsed_seconds,total_cost)


    #Create Minimum balance frame
    def min_bal_topup_frame(self):
        self.tripcal_frame.grid_forget()
        self.min_bal_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.min_bal_frame.grid(row=0, column=0)
        self.min_top_up_label = customtkinter.CTkLabel(self.min_bal_frame, text="Minimum Balance required: "+str(round(min_bal,2))+
                                                        "\nPlease top up your wallet with any desired amount:",
                                                  font=customtkinter.CTkFont(size=20))
        self.min_top_up_label.grid(row=1, column=0, padx=30,pady=10)
        self.min_top_up_entry = customtkinter.CTkEntry(self.min_bal_frame, width=200, placeholder_text="Top_up_amount")
        self.min_top_up_entry.grid(row=3, column=0, padx=30, pady=(15, 15))
        self.min_top_up_button = customtkinter.CTkButton(self.min_bal_frame, text="Top Up", command=self.min_top_up_wallet, width=200)
        self.min_top_up_button.grid(row=4,column=0,padx=30,pady=30)

    #Top ups the wallet with minimum balance user entered
    def min_top_up_wallet(self):
        topup=self.min_top_up_entry.get()
        addbalance(topup,usn)
        self.min_bal_frame.grid_forget()
        self.tripcal_frame.grid(row=0, column=0)
        
    #End Trip Frame showing trip details
    def end_trip_topup_frame(self):
        self.end_trip_bal_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.end_trip_bal_frame.grid(row=0, column=0)
        self.end_trip_top_up_label = customtkinter.CTkLabel(self.end_trip_bal_frame, text="Insufficient Balance\nWallet balance = "+str(wal)+
                                                            "\nTrip Cost = "+str(total_cost)+
                                                            "\nPlease add money to complete trip:",
                                                  font=customtkinter.CTkFont(size=20))
        self.end_trip_top_up_label.grid(row=1, column=0, padx=30,pady=10)
        self.end_trip_top_up_entry = customtkinter.CTkEntry(self.end_trip_bal_frame, width=200, placeholder_text="Amount")
        self.end_trip_top_up_entry.grid(row=3, column=0, padx=30, pady=(15, 15))
        self.end_trip_top_up_button = customtkinter.CTkButton(self.end_trip_bal_frame, text="Top Up", command=self.end_trip_db_topup, width=200)
        self.end_trip_top_up_button.grid(row=4,column=0,padx=30,pady=30)
    
    #End Trip frame for topup, if the wallet amount<end trip amount
    def end_trip_db_topup(self):
        end_trip_top_up_amount = self.end_trip_top_up_entry.get()
        self.end_trip_bal_frame.grid_forget()
        addbalance(end_trip_top_up_amount,usn)
        if float(total_cost)>float(wal):
            self.end_trip_topup_frame()
        else:
            self.close_billing()

    #Function to close the end trip frame and deduct amount from wallet
    def close_billing(self):
        if float(total_cost)>float(wal):
            self.billing_frame.grid_forget()
            self.end_trip_topup_frame()
        else:
            addbalance(-total_cost,usn)
            self.billing_frame.grid_forget()
            self.starttripdropdown.set("<Start point>")
            self.endtripdropdown.set("<End point>")
            global ride
            ride = None
            self.open_feedback_form()

    #Function to save the feedback to the database
    def save_feedback_to_database(self, answer_1, answer_2, answer_3, answer_4):
        
        query = "INSERT INTO feedback (user_id,ride_rating, ride_issues, how_found, app_rating,trip_id) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (usn, answer_1, answer_2, answer_3, answer_4, int(TID)))
        conn.commit()

        #len is 2 as string of empty list has length 2 because of [ and ]
        if len(answer_2)>2:
            cursor.execute('''update vehicledetails set repair_needed="Y" where vehicle_no=? ''',(VID,))
            conn.commit()


    #Create feedback form frame
    def open_feedback_form(self):
        # create a new feedback window
        
        self.feedback_window = customtkinter.CTkFrame(self,corner_radius=0)
        self.feedback_window.grid(row=0,column=0)
        

        # 1 question：How would you rate the ride? (Dropdown)
        feedback_question_1 = customtkinter.CTkLabel(self.feedback_window, text="How would you rate the ride?", font=("Arial", 14))
        feedback_question_1.grid(row=1, column=0, padx=10, pady=10)
        self.feedback_answer_1 = customtkinter.CTkOptionMenu(self.feedback_window, values=["1", "2", "3", "4", "5"])
        self.feedback_answer_1.grid(row=2, column=0, padx=10, pady=10)

        # 4 question：How would you rate this app? (Dropdown)
        feedback_question_4 = customtkinter.CTkLabel(self.feedback_window, text="How would you rate this app?", font=("Arial", 14))
        feedback_question_4.grid(row=1, column=2, padx=10, pady=10)
        self.feedback_answer_4 = customtkinter.CTkOptionMenu(self.feedback_window, values=["1", "2", "3", "4", "5"])
        self.feedback_answer_4.grid(row=2, column=2, padx=10, pady=10)
        
        # 2 question：Was there any issue with the ride? (Checkboxes)
        feedback_question_2 = customtkinter.CTkLabel(self.feedback_window, text="Was there any issue with the ride?", font=("Arial", 14))
        feedback_question_2.grid(row=3, column=0, padx=10, pady=10)
        # self.feedback_answer_2 = [] 
        self.feedback_answer_2_1 = customtkinter.CTkCheckBox(self.feedback_window, text="Wheel problem")
        self.feedback_answer_2_1.grid(row=4, column=0, padx=10, pady=10)
          
        self.feedback_answer_2_2 = customtkinter.CTkCheckBox(self.feedback_window, text="Body problem")
        self.feedback_answer_2_2.grid(row=5, column=0, padx=10, pady=10)
          
        self.feedback_answer_2_3 = customtkinter.CTkCheckBox(self.feedback_window, text="Saddle problem")
        self.feedback_answer_2_3.grid(row=6, column=0, padx=10, pady=10)
         
        self.feedback_answer_2_4 = customtkinter.CTkCheckBox(self.feedback_window, text="Battery problem")
        self.feedback_answer_2_4.grid(row=7, column=0, padx=10, pady=10)
         

        # 3 question：How did you get to know about this app? (Checkboxes)
        self.feedback_question_3 = customtkinter.CTkLabel(self.feedback_window, text="How did you get to know about this app?", font=("Arial", 14))
        self.feedback_question_3.grid(row=3, column=2, padx=10, pady=10)
          
        self.feedback_answer_3_1 = customtkinter.CTkCheckBox(self.feedback_window, text="Friend")
        self.feedback_answer_3_1.grid(row=4, column=2, padx=10, pady=10)
         
        self.feedback_answer_3_2 = customtkinter.CTkCheckBox(self.feedback_window, text="Social Media")
        self.feedback_answer_3_2.grid(row=5, column=2, padx=10, pady=10)
        
        self.feedback_answer_3_3 = customtkinter.CTkCheckBox(self.feedback_window, text="Advertising")
        self.feedback_answer_3_3.grid(row=6, column=2, padx=10, pady=10)
          
        self.feedback_answer_3_4 = customtkinter.CTkCheckBox(self.feedback_window, text="Vlogger")
        self.feedback_answer_3_4.grid(row=7, column=2, padx=10, pady=10)
          

        save_button = customtkinter.CTkButton(self.feedback_window, text="Save", width=10, command=self.save_and_close_feedback)
        save_button.grid(row=8, column=0, columnspan=3, padx=10, pady=20)
        
        # "×" to close the feedback page
        close_button = customtkinter.CTkButton(self.feedback_window, text="X", width=10, font=customtkinter.CTkFont(size=15), command=self.close_feedback)
        close_button.grid(row=0, column=4, sticky="ne", padx=10, pady=10)

        self.update_idletasks()




    def close_feedback(self):
        # close the feedback page
        self.feedback_window.destroy()
        self.call_mainframe()

    # Create a function to save the feedback data to the database
    def save_and_close_feedback(self):
        answer_1 = self.feedback_answer_1.get() 


        
        answer_22=[]
        if(self.feedback_answer_2_1.get()==1):
            answer_22.append("Wheel problem")
        if(self.feedback_answer_2_2.get()==1):
            answer_22.append("Body problem")
        if(self.feedback_answer_2_3.get()==1):
            answer_22.append("Saddle problem")
        if(self.feedback_answer_2_4.get()==1):
            answer_22.append("Battery problem")
        
        
        answer_32=[]
        if(self.feedback_answer_3_1.get()==1):
            answer_32.append("Friend")
        if(self.feedback_answer_3_2.get()==1):
            answer_32.append("Social Media")
        if(self.feedback_answer_3_3.get()==1):
            answer_32.append("Advertising")
        if(self.feedback_answer_3_4.get()==1):
            answer_32.append("Vlogger")


        answer_2 = str(answer_22)
        answer_3 = str(answer_32)
        answer_4 = self.feedback_answer_4.get() 


        self.save_feedback_to_database(answer_1, answer_2, answer_3, answer_4)
        print(answer_1,answer_2,answer_3,answer_4)
        # Thank you page
        close_button = customtkinter.CTkButton(self.feedback_window, text="X", width=10, font=customtkinter.CTkFont(size=15), command=self.close_feedback)
        close_button.grid(row=0, column=4, sticky="ne", padx=10, pady=10)

        thank_message = customtkinter.CTkLabel(self.feedback_window, text="Thank you for your feedback!", font=("Arial", 20))
        thank_message.grid(row=9, column=0, columnspan=5, padx=10, pady=20)


    
    def get_trip_cost(self):
        if self.trip_mode == "cycle":
            return 0.5  # 0.5£/s
        elif self.trip_mode == "bike":
            return 1.0  # 1.0£/s
        return 0.0  # default 0£/s
    

    
    def tripcal(self):
            
            # create trip calculate frame
            
            self.tripcal_frame =customtkinter.CTkFrame(self,corner_radius=2)
            self.tripcal_frame.grid(row=0, column=0)

            self.tripcalLabel0 =customtkinter.CTkLabel(self.tripcal_frame,text="Hey "+usn[0].upper()+usn[1:]+",\nBelow are your trip details: ", 
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
            self.tripcalLabel0.grid(row=0,column=0,padx=30, pady=8)

            self.tripcalLabel =customtkinter.CTkLabel(self.tripcal_frame,text="Your Chosen Start Point: ", 
                                                    font=customtkinter.CTkFont(size=18, weight="bold"))
            self.tripcalLabel.grid(row=1,column=0,padx=30, pady=10)

            self.tripcalLabel1 =customtkinter.CTkLabel(self.tripcal_frame,text=st, 
                                                    font=customtkinter.CTkFont(size=15, weight="normal"))
            self.tripcalLabel1.grid(row=2,column=0,padx=30)

            self.tripcalLabel2 =customtkinter.CTkLabel(self.tripcal_frame,text="Your Chosen End Point: ", 
                                                    font=customtkinter.CTkFont(size=18,weight="bold"))
            self.tripcalLabel2.grid(row=3,column=0,padx=30, pady=10)

            self.tripcalLabel3 =customtkinter.CTkLabel(self.tripcal_frame,text=dt, 
                                                    font=customtkinter.CTkFont(size=15))
            self.tripcalLabel3.grid(row=4,column=0,padx=30)

            self.tripcalLabel4 =customtkinter.CTkLabel(self.tripcal_frame,text="Please select your mode of ride: ", 
                                                    font=customtkinter.CTkFont(size=18,weight="bold"))
            self.tripcalLabel4.grid(row=5,column=0,padx=30, pady=30)

            self.ebike_image = customtkinter.CTkImage(dark_image=Image.open(pathdb + "/test_images/ebike.png"), size=(30, 30))
            self.ecycle_image = customtkinter.CTkImage(dark_image=Image.open(pathdb + "/test_images/ecycle.png"), size=(30, 30))

            self.tripmodec = customtkinter.CTkButton(self.tripcal_frame, text="E-Cycle" + "\t\t" + "£0.5/sec", width=100,
                                             font=customtkinter.CTkFont(size=20, weight="bold"), anchor="w", 
                                             image=self.ecycle_image, command=self.start_cycle_trip)
            self.tripmodec.grid(row=6, column=0, padx=30)

            self.tripmodeb = customtkinter.CTkButton(self.tripcal_frame, text="E-Bike" + "\t\t" + "£1.0/sec", width=100,
                                                    font=customtkinter.CTkFont(size=20, weight="bold"), anchor="w", 
                                                    image=self.ebike_image, command=self.start_bike_trip)
            self.tripmodeb.grid(row=7, column=0, padx=30, pady=8)


            # Modify the command of the start_trip button to start the timer:
            self.start_trip = customtkinter.CTkButton(self.tripcal_frame, text="Start Trip ->", width=80, 
                                                    font=customtkinter.CTkFont(size=25, weight="bold"), 
                                                    command=self.start_trip_time)  
            self.start_trip.grid(row=8, column=0, padx=5, pady=20) 

            #Added Back button for location re-selection
            self.main_back_button = customtkinter.CTkButton(self.tripcal_frame, text="Back", width=60, 
                                                        font=customtkinter.CTkFont(size=25, weight="bold"), 
                                                        command=self.call_mainframe)  #-- New command added
            self.main_back_button.grid(row=10, column=0, padx=5, pady=20) 


            self.back_button = customtkinter.CTkButton(self.tripcal_frame, text="Logout", command=self.logout, width=40)
            self.back_button.grid(row=12, column=0, padx=5, pady=10)
            self.update_idletasks()

            bikeavail,cycleavail=getvehicleavail(st)
#check to grey out buutton if conditions are not met
            if int(bikeavail)==0 and int(cycleavail)==0:
                self.tripmodeb.configure(state="disabled", text="No Bikes available")
                self.tripmodec.configure(state="disabled", text="No Cycles available")
                global ride
                ride = "noavail"
            elif int(bikeavail)==0:
                self.tripmodeb.configure(state="disabled", text="No Bikes available")
            elif int(cycleavail)==0:
                self.tripmodec.configure(state="disabled", text="No Cycles available")


#get teh trip start and end details from the dropdown 
    def tripdetail(self):
                print("Start: " + self.starttripdropdown.get())
                print("End: " + self.endtripdropdown.get())

                if self.starttripdropdown.get() == "<Start point>" or self.starttripdropdown.get() == None:
                    messagebox.showinfo("Error", "Please select appropriate START location")
                elif self.endtripdropdown.get() == "<End point>" or self.endtripdropdown.get() == None:
                    messagebox.showinfo("Error", "Please select appropriate END location")
                elif self.starttripdropdown.get() == self.endtripdropdown.get():
                    messagebox.showinfo("Error", "START and END locations cannot be same")
                else:
                    global st, dt
                    st = self.starttripdropdown.get()
                    dt = self.endtripdropdown.get()
                    self.main_frame.grid_forget() 
                    self.login_frame.grid_forget()
                    self.register_frame.grid_forget()
                    self.tripcal()



#######################################################################################################################################################################
############################################ OPERATOR PAGE ########################################################

#define the home page for operator
    def operatorpagemain(self):
        #create operator frame

        self.operator_main_frame = customtkinter.CTkFrame(self, corner_radius=2)
        self.operator_main_frame.grid(row=0, column=0)
        self.operator_main_label = customtkinter.CTkLabel(self.operator_main_frame, text="Hey Operator "+usn+",\nPlease select your task from given option: ",
                                                  font=customtkinter.CTkFont(size=35, weight="bold"))
        self.operator_main_label.grid(row=0, column=0, padx=30, pady=10)

        self.operator_track = customtkinter.CTkButton(self.operator_main_frame, text="Track vehicles", width=80, 
                                                    font=customtkinter.CTkFont(size=20, weight="bold"), 
                                                    command=self.op_trackveh)  
        self.operator_track.grid(row=1, column=0, padx=5, pady=20) 

        self.operator_charge = customtkinter.CTkButton(self.operator_main_frame, text="Charge vehicles", width=80, 
                                                    font=customtkinter.CTkFont(size=20, weight="bold"), 
                                                    command=self.op_chargeveh)  
        self.operator_charge.grid(row=2, column=0, padx=5, pady=20) 

        self.operator_repair = customtkinter.CTkButton(self.operator_main_frame, text="Repair vehicles", width=80, 
                                                    font=customtkinter.CTkFont(size=20, weight="bold"), 
                                                    command=self.op_repairveh)  
        self.operator_repair.grid(row=3, column=0, padx=5, pady=20) 

        self.operator_mveh = customtkinter.CTkButton(self.operator_main_frame, text="Move Vehicles", width=80, 
                                                    font=customtkinter.CTkFont(size=20, weight="bold"), 
                                                    command=self.op_movveh)  
        self.operator_mveh.grid(row=4, column=0, padx=5, pady=20)

        self.operator_logout = customtkinter.CTkButton(self.operator_main_frame, text="Logout", command=self.logout, width=50)
        self.operator_logout.grid(row=5, column=0, padx=5, pady=50)


        
#Function for Operator to track vehicles

    def op_trackveh(self):
        
        self.operator_main_frame.grid_forget()
        
        cols=()
        cols,bike,cycle=getvehicledetails()

        self.optrack_frame = customtkinter.CTkFrame(self, corner_radius=2)
        self.optrack_frame.grid(row=0, column=0)

        style=ttk.Style()
        style.configure("Treeview",font=(None, 14))
        style.configure("Treeview.Heading",font=(None, 14))

        self.optrack_label=customtkinter.CTkLabel(self.optrack_frame,text="Bike Details: ",
                                                  font=customtkinter.CTkFont(size=35, weight="bold"))
        self.optrack_label.grid(row=0, column=0, padx=30, pady=10)

        tree=ttk.Treeview(self.optrack_frame,columns=cols,displaycolumns=cols)

        vsb= ttk.Scrollbar(self.optrack_frame,orient="vertical",command=tree.yview)
        tree.configure(xscrollcommand=vsb.set)
        

        for item in bike:
            tree.insert("","end",values=item)

        tree.heading("#1",text=cols[0])
        tree.heading("#2",text=cols[1])
        tree.heading("#3",text=cols[2])
        tree.heading("#4",text=cols[3])
        tree.heading("#5",text=cols[4])

        tree.column("#0", width=0)
        tree.column("#1", width=150,anchor="center")
        tree.column("#2", width=150,anchor="center")
        tree.column("#3", width=150,anchor="center")
        tree.column("#4", width=150,anchor="center")
        tree.column("#5", width=150,anchor="center")

        tree.grid(row=1,column=0,padx=10,pady=5)
        vsb.grid(row=1,column=1)

        ###########
        self.optrack_label2=customtkinter.CTkLabel(self.optrack_frame,text="Cycle Details: ",
                                                  font=customtkinter.CTkFont(size=35, weight="bold"))
        self.optrack_label2.grid(row=3, column=0, padx=30, pady=10)

        tree1=ttk.Treeview(self.optrack_frame,columns=cols,displaycolumns=cols)

        vsb1= ttk.Scrollbar(self.optrack_frame,orient="vertical",command=tree1.yview)
        tree1.configure(xscrollcommand=vsb1.set)
        

        for item in cycle:
            tree1.insert("","end",values=item)

        tree1.heading("#1",text=cols[0])
        tree1.heading("#2",text=cols[1])
        tree1.heading("#3",text=cols[2])
        tree1.heading("#4",text=cols[3])
        tree1.heading("#5",text=cols[4])

        tree1.column("#0", width=0)
        tree1.column("#1", width=150,anchor="center")
        tree1.column("#2", width=150,anchor="center")
        tree1.column("#3", width=150,anchor="center")
        tree1.column("#4", width=150,anchor="center")
        tree1.column("#5", width=150,anchor="center")

        tree1.grid(row=4,column=0,padx=10,pady=5)
        vsb1.grid(row=4,column=1)

        self.optrack_back = customtkinter.CTkButton(self.optrack_frame, text="X",width=20, 
                                                    command=self.operatorforget)
        self.optrack_back.grid(row=0, column=1, padx=5, pady=5)


#Function for operator to move vehicles       

    def op_movveh(self):
        self.operator_main_frame.grid_forget()

        self.opmove_frame = customtkinter.CTkFrame(self, corner_radius=2)
        self.opmove_frame.grid(row=0, column=0)

        self.opmove_label=customtkinter.CTkLabel(self.opmove_frame,text="Hey Operator "+usn,
                                                  font=customtkinter.CTkFont(size=35, weight="bold"))
        self.opmove_label.grid(row=0, column=0,columnspan=3, padx=30, pady=10)

        self.opmove_label1=customtkinter.CTkLabel(self.opmove_frame,text="Please check the current allocation of vehicles and move them if required",
                                                  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.opmove_label1.grid(row=1, column=0,columnspan=3, padx=30, pady=10)

        style=ttk.Style()
        style.configure("Treeview",font=(None, 10))
        style.configure("Treeview.Heading",font=(None, 10))

        tree1=ttk.Treeview(self.opmove_frame,columns=["Locations","Cycle Count", "Bike Count"],displaycolumns=["Locations","Cycle Count", "Bike Count"])

        vsb1= ttk.Scrollbar(self.opmove_frame,orient="vertical",command=tree1.yview)
        tree1.configure(xscrollcommand=vsb1.set)
        
        all_data,all_loc=vehicleavailloc()

        for item in all_data:
            tree1.insert("","end",values=item)



        tree1.heading("#1",text="Locations")
        tree1.heading("#2",text="Cycle Count")
        tree1.heading("#3",text="Bike Count")

        tree1.column("#0", width=0)
        tree1.column("#1", width=100,anchor="center")
        tree1.column("#2", width=100,anchor="center")
        tree1.column("#3", width=100,anchor="center")

        tree1.grid(row=2,column=1,padx=10,pady=5)
        vsb1.grid(row=2,column=2)

        self.opmove_label3=customtkinter.CTkLabel(self.opmove_frame,text="Vehicle:",
                                                  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.opmove_label3.grid(row=3, column=0, padx=30, pady=10)

        self.opmove_label5=customtkinter.CTkLabel(self.opmove_frame,text="Move From:",
                                                  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.opmove_label5.grid(row=3, column=1, padx=30, pady=10)

        self.opmove_label6=customtkinter.CTkLabel(self.opmove_frame,text="Move To:",
                                                  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.opmove_label6.grid(row=3, column=2, padx=30, pady=10)
        


        self.type_var = tk.StringVar()  
        self.type_var.set("<Location>")

        self.type_var_mf = tk.StringVar()  
        self.type_var_mf.set("<Type>")


        self.opmove_vehdp = customtkinter.CTkOptionMenu(self.opmove_frame,variable=self.type_var_mf, dynamic_resizing=True,
                                                        values=["Cycle", "Bike"])
        self.opmove_vehdp.grid(row=4, column=0, padx=20)

        self.opmove_movefromdp = customtkinter.CTkOptionMenu(self.opmove_frame,variable=self.type_var, dynamic_resizing=True,
                                                        values=all_loc)
        self.opmove_movefromdp.grid(row=4, column=1, padx=20)

        self.type_var_mt = tk.StringVar()  
        self.type_var_mt.set("<Location>")

        self.opmove_movetodp = customtkinter.CTkOptionMenu(self.opmove_frame,variable=self.type_var_mt, dynamic_resizing=True,
                                                        values=all_loc)
        self.opmove_movetodp.grid(row=4, column=2, padx=20)

        
        
        self.opnext_btn = customtkinter.CTkButton(self.opmove_frame, text="Move",width=50, 
                                                    command=self.opmove_fxn)
        self.opnext_btn.grid(row=6, column=0,columnspan=3, padx=5, pady=20)


        self.opmov_back = customtkinter.CTkButton(self.opmove_frame, text="X",width=20, 
                                                    command=self.operatorforget)
        self.opmov_back.grid(row=0, column=3, padx=5, pady=5)


    def opmove_fxn(self):


        tp=self.opmove_vehdp.get()
        mf=self.opmove_movefromdp.get()
        mt=self.opmove_movetodp.get()
        
        if tp=="<Type>":
                messagebox.showinfo('Error',"Please select a vehicle type to move")
        elif mf=="<Location>" and mt =="<Location>":
                messagebox.showinfo('Error',"Please select a location from [Move from] and [Move to]")
        elif mf!="<Location>" and mt =="<Location>":
                 messagebox.showinfo('Error',"Please select appropriate [Move To] location")
        elif mt!="<Location>" and mf=="<Location>":
                 messagebox.showinfo('Error',"Please select appropriate [Move From] location")
        elif mf!="<Location>" and mt!="<Location>" and tp!="<Type>":
            vehiclesetloc(str(tp).lower(),mf,mt)

        if vehmov=="Moved":
            self.opmove_frame.grid_forget()
            self.op_movveh()


#function for operator to charge the vehicles 
    def op_chargeveh(self):
        self.operator_main_frame.grid_forget()

        self.opcharge_frame = customtkinter.CTkFrame(self, corner_radius=2)
        self.opcharge_frame.grid(row=0, column=0)

        self.opcharge_label=customtkinter.CTkLabel(self.opcharge_frame,text="Hey Operator "+usn,
                                                  font=customtkinter.CTkFont(size=35, weight="bold"))
        self.opcharge_label.grid(row=0, column=0,columnspan=2, padx=30, pady=10)

        self.opcharge_label1=customtkinter.CTkLabel(self.opcharge_frame,text="Please charge the below vehicles:",
                                                  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.opcharge_label1.grid(row=1, column=0,columnspan=2, padx=30, pady=10)

        style=ttk.Style()
        style.configure("Treeview",font=(None, 10))
        style.configure("Treeview.Heading",font=(None, 10))

        tree1=ttk.Treeview(self.opcharge_frame,columns=["Vehicle ID","Charge Status"],displaycolumns=["Vehicle ID","Charge Status"])

        vsb1= ttk.Scrollbar(self.opcharge_frame,orient="vertical",command=tree1.yview)
        tree1.configure(xscrollcommand=vsb1.set)
        
        chg,ids=vehiclechargeget()

        for item in chg:
            tree1.insert("","end",values=item)



        tree1.heading("#1",text="Vehicle ID")
        tree1.heading("#2",text="Charge Status")
        
        tree1.column("#0", width=0)
        tree1.column("#1", width=150,anchor="center")
        tree1.column("#2", width=150,anchor="center")

        tree1.grid(row=2,column=0,padx=10,pady=5)
        vsb1.grid(row=2,column=1)

        self.opcharge_label3=customtkinter.CTkLabel(self.opcharge_frame,text="Vehicle ID:",
                                                  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.opcharge_label3.grid(row=3, column=0,columnspan=2, padx=30, pady=10)

        self.id_var = tk.StringVar()  
        self.id_var.set("<ID>")


        self.opcharge_vehdp = customtkinter.CTkOptionMenu(self.opcharge_frame,variable=self.id_var, dynamic_resizing=True,
                                                        values=ids)
        self.opcharge_vehdp.grid(row=4, column=0,columnspan=2, padx=20)

        self.opcharge_btn = customtkinter.CTkButton(self.opcharge_frame, text="Charge",width=50, 
                                                    command=self.opcharge_fxn)
        self.opcharge_btn.grid(row=6, column=0,columnspan=2, padx=5, pady=20)

        self.opcharge_close=customtkinter.CTkButton(self.opcharge_frame,text="X",width=20, 
                                                    command=self.operatorforget)
        self.opcharge_close.grid(row=0, column=1, padx=5, pady=5)


    def opcharge_fxn(self):
        ch_sel=self.opcharge_vehdp.get()

        if ch_sel=="<ID>":
            messagebox.showinfo('Error',"No Vehicle to charge")
        else:
            vehiclechargeset(ch_sel)
        
        if vehcharge=="Charged":
            self.opcharge_frame.grid_forget()
            self.op_chargeveh()

## function to repair the vehicles
    def op_repairveh(self):
        self.operator_main_frame.grid_forget()

        self.oprepair_frame = customtkinter.CTkFrame(self, corner_radius=2)
        self.oprepair_frame.grid(row=0, column=0)

        self.oprepair_label=customtkinter.CTkLabel(self.oprepair_frame,text="Hey Operator "+usn,
                                                  font=customtkinter.CTkFont(size=35, weight="bold"))
        self.oprepair_label.grid(row=0, column=0,columnspan=2, padx=30, pady=10)

        self.oprepair_label1=customtkinter.CTkLabel(self.oprepair_frame,text="Please repair the below vehicles:",
                                                  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.oprepair_label1.grid(row=1, column=0,columnspan=2, padx=30, pady=10)

        style=ttk.Style()
        style.configure("Treeview",font=(None, 10))
        style.configure("Treeview.Heading",font=(None, 10))

        tree1=ttk.Treeview(self.oprepair_frame,columns=["Vehicle ID","Repair Status"],displaycolumns=["Vehicle ID","Repair Status"])

        vsb1= ttk.Scrollbar(self.oprepair_frame,orient="vertical",command=tree1.yview)
        tree1.configure(xscrollcommand=vsb1.set)
        
        rpr,ids=vehrepairget()

        for item in rpr:
            tree1.insert("","end",values=item)



        tree1.heading("#1",text="Vehicle ID")
        tree1.heading("#2",text="Repair Status")
        
        tree1.column("#0", width=0)
        tree1.column("#1", width=150,anchor="center")
        tree1.column("#2", width=150,anchor="center")

        tree1.grid(row=2,column=0,padx=10,pady=5)
        vsb1.grid(row=2,column=1)

        self.oprepair_label3=customtkinter.CTkLabel(self.oprepair_frame,text="Vehicle ID:",
                                                  font=customtkinter.CTkFont(size=15, weight="bold"))
        self.oprepair_label3.grid(row=3, column=0,columnspan=2, padx=30, pady=10)

        self.id_var = tk.StringVar()  
        self.id_var.set("<ID>")


        self.oprepair_vehdp = customtkinter.CTkOptionMenu(self.oprepair_frame,variable=self.id_var, dynamic_resizing=True,
                                                        values=ids)
        self.oprepair_vehdp.grid(row=4, column=0,columnspan=2, padx=20)

        self.oprepair_btn = customtkinter.CTkButton(self.oprepair_frame, text="Repair",width=50, 
                                                    command=self.oprepair_fxn)
        self.oprepair_btn.grid(row=6, column=0,columnspan=2, padx=5, pady=20)

        self.oprepair_close=customtkinter.CTkButton(self.oprepair_frame,text="X",width=20, 
                                                    command=self.operatorforget)
        self.oprepair_close.grid(row=0, column=1, padx=5, pady=5)


    def oprepair_fxn(self):
        rp_sel=self.oprepair_vehdp.get()

        if rp_sel=="<ID>":
            messagebox.showinfo('Error',"No Vehicle to repair")
        else:
            vehiclerepairset(rp_sel)
        
        if vehrepair=="Repaired":
            self.oprepair_frame.grid_forget()
            self.op_repairveh()


#define forget frames to clear cache    
    def operatorforget(self):
        try:
            self.optrack_frame.grid_forget()
        except:
            pass
        try:
            self.opmove_frame.grid_forget()
        except:
            pass
        try:
            self.opcharge_frame.grid_forget()
        except:
            pass
        try:
            self.oprepair_frame.grid_forget()
        except:
            pass
        self.operatorpagemain()


#######################################################################################################################################################################
############################################ MANAGER PAGE ########################################################
#create the manager homepage

    def managerpagemain(self):
        #create Manager frame

        self.manager_main_frame = customtkinter.CTkFrame(self, corner_radius=2)
        self.manager_main_frame.grid(row=0, column=0)
        self.manager_main_label = customtkinter.CTkLabel(self.manager_main_frame, text="Hey Manager "+usn,
                                                  font=customtkinter.CTkFont(size=35, weight="bold"))
        self.manager_main_label.grid(row=0, column=0,columnspan=2, padx=30, pady=10)

        self.manager_main_label_1 = customtkinter.CTkLabel(self.manager_main_frame, text="Choose from the options on the left\nAND\nView reports respectively on the right",
                                                  font=customtkinter.CTkFont(size=22, weight="bold"))
        self.manager_main_label_1.grid(row=1, column=0,columnspan=2, padx=30, pady=10)

        report_list=["Trip Duration Distribution","Trip Fare Distribution", "Trip Duration and Fare Statistics","Most Frequent Selections",
                     "User Type Distribution","User Wallet Balance Distribution",
                     "Most Common Ride Issues","Most Common Referral","Vehicle Charge Status","Vehicle Repair Status",
                     "Ride Ratings","App Ratings"]

        report_var = tk.StringVar()  
        report_var.set("<Select Report>")

        sd_var=tk.StringVar()
        sd_var.set("<Range Start Date>")

        ed_var=tk.StringVar()
        ed_var.set("<Range End Date>")

        sd =gettripstartdates()
        ed =gettripenddates()

        sd.insert(0,"ALL")
        ed.insert(0,"ALL")

        self.manager_report_dpdwn = customtkinter.CTkOptionMenu(self.manager_main_frame,variable=report_var, dynamic_resizing=True,
                                                        values=report_list)
        self.manager_report_dpdwn.grid(row=3, column=0,columnspan=2, padx=10,pady=20)

        self.manager_label_2 = customtkinter.CTkLabel(self.manager_main_frame, text="Dates are available only for Trip related Reports",
                                                  font=customtkinter.CTkFont(size=15))
        self.manager_label_2.grid(row=4, column=0,columnspan=2, padx=10,pady=10)

        self.manager_report_startdate_dpdw = customtkinter.CTkOptionMenu(self.manager_main_frame,variable=sd_var, dynamic_resizing=True,
                                                        values=sd)
        self.manager_report_startdate_dpdw.grid(row=5, column=0,pady=5)

        self.manager_report_enddate_dpdw = customtkinter.CTkOptionMenu(self.manager_main_frame,variable=ed_var, dynamic_resizing=True,
                                                        values=ed)
        self.manager_report_enddate_dpdw.grid(row=5, column=1,pady=5)

        self.manager_select_btn = customtkinter.CTkButton(self.manager_main_frame,text="Generate Report",width=50, 
                                                    command=self.manager_generatereport)
        self.manager_select_btn.grid(row=6, column=0,columnspan=2, padx=10, pady=20)

        self.manager_logout_btn = customtkinter.CTkButton(self.manager_main_frame,text="Logout",width=50, 
                                                    command=self.logout)
        self.manager_logout_btn.grid(row=8, column=0,columnspan=2, padx=10, pady=20)


#create the dropdown for various reports
    def manager_generatereport(self):
        report_sel= self.manager_report_dpdwn.get()

        sd =self.manager_report_startdate_dpdw.get()
        ed=self.manager_report_enddate_dpdw.get()

        # Load data from SQLite into Pandas DataFrames
        logindetails_df, tripdetails_df, vehicledetails_df, walletdetails_df,feedback_df = fetch_data_from_db()


        if report_sel=="<Select Report>":
            messagebox.showinfo('Error',"Please select a valid report from dropdown")
        elif report_sel=="Trip Duration Distribution":
            if sd =="<Range Start Date>" or ed =="<Range End Date>":
                messagebox.showerror("Error","Please select appropriate Date or 'ALL' for both")
            elif sd =="ALL" and ed =="ALL":
                logindetails_df1, tripdetails_df1, vehicledetails_df1, walletdetails_df1,feedback_df1 = fetch_data_from_db()
                plot_trip_duration_distribution(tripdetails_df1)
            elif ((sd !="<Range Start Date>" or sd!="ALL") and ed =="ALL") or ((ed !="<Range Start Date>" or ed!="ALL") and st =="ALL"):
                messagebox.showerror("Error","Please select appropriate Date or 'ALL' for both")
            else:
                logindetails_df1, tripdetails_df1, vehicledetails_df1, walletdetails_df1,feedback_df1 = fetch_data_from_db(sd,ed)
                plot_trip_duration_distribution(tripdetails_df1)

        elif report_sel == "Trip Fare Distribution":
            if sd =="<Range Start Date>" or ed =="<Range End Date>":
                messagebox.showerror("Error","Please select appropriate Date or 'ALL' for both")
            elif sd =="ALL" and ed =="ALL":
                logindetails_df1, tripdetails_df1, vehicledetails_df1, walletdetails_df1,feedback_df1 = fetch_data_from_db()
                plot_trip_fare_distribution(tripdetails_df1)
            elif (sd not in ("<Range Start Date>","ALL") and ed =="ALL") or (ed not in ("<Range Start Date>","ALL") and st =="ALL"):
                messagebox.showerror("Error","Please select appropriate Date or 'ALL' for both")
            else:
                logindetails_df1, tripdetails_df1, vehicledetails_df1, walletdetails_df1,feedback_df1 = fetch_data_from_db(sd,ed)
                plot_trip_fare_distribution(tripdetails_df1)

        elif report_sel == "Trip Duration and Fare Statistics":
            if sd =="<Range Start Date>" or ed =="<Range End Date>":
                messagebox.showerror("Error","Please select appropriate Date or 'ALL' for both")
            elif sd =="ALL" and ed =="ALL":
                logindetails_df1, tripdetails_df1, vehicledetails_df1, walletdetails_df1,feedback_df1 = fetch_data_from_db()            
                table_stats(tripdetails_df1)
            elif (sd not in ("<Range Start Date>","ALL") and ed =="ALL") or (ed not in ("<Range Start Date>","ALL") and st =="ALL"):
                messagebox.showerror("Error","Please select appropriate Date or 'ALL' for both")
            else:
                logindetails_df1, tripdetails_df1, vehicledetails_df1, walletdetails_df1,feedback_df1 = fetch_data_from_db(sd,ed)
                table_stats(tripdetails_df1)
                
        elif report_sel =="Most Frequent Selections":
            table_mostfreq(tripdetails_df)
        elif report_sel == "User Type Distribution":
            plot_user_type_distribution(logindetails_df)
        elif report_sel == "User Wallet Balance Distribution":
            plot_wallet_balance_distribution(walletdetails_df)
        elif report_sel == "Most Common Ride Issues":
            ride_issues_word_cloud(feedback_df)
        elif report_sel == "Most Common Referral":
            referral_word_cloud(feedback_df)
        elif report_sel == "App Ratings":
            app_rating_distribution(feedback_df)
        elif report_sel == "Ride Ratings":
            ride_rating_distribution(feedback_df)
        elif report_sel == "Vehicle Repair Status":
            plot_repair_status(vehicledetails_df)
        elif report_sel =="Vehicle Charge Status":
            plot_charge_status(vehicledetails_df)

    
#Main Function to run the application on loop till its manually closed
if __name__ == "__main__":
    app = App()
    app.mainloop()
