"""

     INTERFACCIA GRAFICA ED ELABORAZIONE

"""
# CUSTOM MODULES
from class_FSM import FSM
from class_serial import SerialClass


# LIBRARY
from tkinter import *
import datetime
import time
import requests
import json

## CUSTOM DEFINED FUNCTIONS
def update_label():
    calendar = datetime.datetime.now()
    date = calendar.strftime("%d/%m/%y")
    time = calendar.strftime("%H:%M:%S")
    date_label.configure(text=date)
    time_label.configure(text=time)
    root.after(1000, update_label)

def weather():
    try:
        url_base = "http://api.openweathermap.org/data/2.5/weather?q=Cosenza,Italy&units=metric&"
        key= "appid=key_id"
        url = "{}{}".format(url_base,key)
        richiesta = requests.get(url, timeout=10)
        
        api_resp = json.loads(richiesta.content)
    except:
        api_resp = None
        print("Error API Wether request")

    root.after(100000, weather) # update after 100 seconds
        
    return api_resp
###########################################################################################



##########################################################################################

def status():
    global pushed_button
    
    if pushed_button == 0:
        # ALARM ACTIVE
        pushed_button = 1
        
    else:
        
        def button_click(number):
            current = e.get()
            e.delete(0,END)
            e.insert(0, str(current) + str(number))

        def clear_button():
            e.delete(0, END)

        def button_ok():
            first_number = e.get()
            global f_num
            global pushed_button

            if len(first_number) == 0:
                print("INSERT PASSWORD")
            else:
                f_num = int(first_number)
                
                if (f_num == 1234):
                    global operation 
                    #operation = True
                    print("RIGHT PASSWORD")
                    # ALARM DISABLED
                    pushed_button = 0
                    pw.destroy()
                    
                    
                else:
                    #operation= False
                    print("WRONG PASSWORD")
                    pushed_button = 1
                    pw.destroy()

                    
            #e.delete(0, END)
            #return operation
        
        pw = Toplevel()
        pw.title("Password")

        global operation
        global f_num
        operation= False

        e = Entry(pw, width=40,justify=RIGHT,borderwidth = 5 )
        e.grid(row= 0,column=0,columnspan=5, padx=10,pady=10 )

        button_1 = Button (pw, text ="1", padx=40, pady=20,command=lambda: button_click(1))
        button_2 = Button (pw, text ="2", padx=40, pady=20,command=lambda: button_click(2))
        button_3 = Button (pw, text ="3", padx=40, pady=20,command=lambda: button_click(3))
        button_4 = Button (pw, text ="4", padx=40, pady=20,command=lambda: button_click(4))
        button_5 = Button (pw, text ="5", padx=40, pady=20,command=lambda: button_click(5))
        button_6 = Button (pw, text ="6", padx=40, pady=20,command=lambda: button_click(6))
        button_7 = Button (pw, text ="7", padx=40, pady=20,command=lambda: button_click(7))
        button_8 = Button (pw, text ="8", padx=40, pady=20,command=lambda: button_click(8))
        button_9 = Button (pw, text ="9", padx=40, pady=20,command=lambda: button_click(9))
        button_0 = Button (pw, text ="0", padx=40, pady=20,command=lambda: button_click(0))


        button_pass = Button (pw, text ="OK", padx=38, pady=20,command=lambda:button_ok())
        button_clear = Button (pw, text ="X", padx=40, pady=20,command= lambda: clear_button())
        # password botton
                
        button_1.grid(row= 3,column= 0)
        button_2.grid(row= 3,column= 1)
        button_3.grid(row= 3,column= 2)

        button_4.grid(row=2 ,column= 0)
        button_5.grid(row=2 ,column= 1)
        button_6.grid(row=2 ,column= 2)

        button_7.grid(row=1 ,column= 0)
        button_8.grid(row=1 ,column= 1)
        button_9.grid(row=1 ,column= 2)

        button_clear.grid(row=4 ,column=0)
        button_0.grid(row= 4,column= 1)
        button_pass.grid(row=4,column=2)
        

        
def door_status():
    global door_state
    if door_state == 0:
        cdoor_led.itemconfig(door_led, fill="#00FF00")
    else:
        cdoor_led.itemconfig(door_led, fill="#FF0000")
    root.after(100, door_status)
    
def window_status():
    global window_state
    if window_state == 0:
        cwindow_led.itemconfig(window_led, fill="#00FF00")
    else:
        cwindow_led.itemconfig(window_led, fill="#FF0000")
    root.after(100, window_status)
    
def pir_status():
    global pir_state
    if pir_state == 0:
        cpir_led.itemconfig(pir_led, fill="#00FF00")
    else:
        cpir_led.itemconfig(pir_led, fill="#FF0000")
    root.after(100, pir_status)


def log_file():
    global log_button

    file_log = open("log_file.txt",'r')
    top = Toplevel()  
    top.title("Log Window")      
    top.geometry("800x460")
    
    my_label = Label(top,text ="Log File: ", font = ("Helvetica", 15))
    my_label.pack()

    myscroll = Scrollbar(top) 
    myscroll.pack(side = RIGHT, fill = Y) 
 
    mylist = Listbox(top,width = 130,yscrollcommand = myscroll.set)

    rf  = file_log.readlines()
    for i in range(len(rf)):
        mylist.insert(END, rf[i])
        
    mylist.pack(side = LEFT, fill = BOTH )    
    myscroll.config(command = mylist.yview) 
    
    file_log.close()
    
def acquisition_notification():
    
    global state
    global pushed_button
    global door_state
    global window_state
    global pir_state

    ## SERIAL READING
    try:
        read_data = ser.serial_read()
        
        data_list[0] = int(read_data[0].rstrip()) # door_state
        data_list[1] = int(read_data[1].rstrip()) # window_state
        data_list[2] = int(read_data[2].rstrip()) # pir_state
        data_list[3] = int(read_data[3].rstrip()) # lux 
        data_list[4] = int(read_data[4].rstrip()) # temperature
        data_list[5] = int(read_data[5].rstrip()) # humidity
        
    except:
        print("Wrong serial reading")
        time.sleep(2)
        
    door_state = data_list[0]
    window_state = data_list[1]
    pir_state = data_list[2]

    if door_state == 0:
        str_door = "CLOSED"
    else:
        str_door = "OPEN"
        
    if window_state == 0:
        str_window = "CLOSED"
    else:
        str_window = "OPEN"
        
    if pir_state == 0:
        str_pir = "NO"
    else:
        str_pir = "YES"
        
    temp_label.configure(text="Temperature: " + str(data_list[4]) + "\u2103")
    lux_label.configure(text="Luminosity: " + str(data_list[3]) + " lux")
    hum_label.configure(text="Humidity: " + str(data_list[5]) + " %")

    
    print(data_list)#####################################################################################################
    ## STATE TRANSITION HANDLING
    if state == "IDLE":
        state,pushed_button = fsm.idle_state(state, pushed_button, data_list)
        
        can_on_led.itemconfig(on_led, fill="#FF0000") # ROSSO
        alarm_label.configure(text="Alarm Disabled",font=("Helvetica", 11))

        door_label.configure(text="DOOR: {}".format(str_door), font=("Helvetica",20))
        window_label.configure(text="WINDOW: {}".format(str_window),font=("Helvetica",20))
        pir_label.configure(text="MOTION: {}".format(str_pir),font=("Helvetica",20))

    elif state == "ACTIVE":
        state,pushed_button = fsm.active_state(state, pushed_button, data_list)
        
        can_on_led.itemconfig(on_led, fill="#00FF00") # VERDE
        alarm_label.configure(text="Alarm Enabled",font=("Helvetica", 11))

        door_label.configure(text="DOOR: {}".format(str_door), font=("Helvetica",20))
        window_label.configure(text="WINDOW: {}".format(str_window),font=("Helvetica",20))
        pir_label.configure(text="MOTION: {}".format(str_pir),font=("Helvetica",20))

        
    elif state == "ALARM":
        state,pushed_button = fsm.alarm_state(state, pushed_button, data_list)

        calendar = datetime.datetime.now()
        date = calendar.strftime("%d/%m/%y")
        time = calendar.strftime("%H:%M:%S")

        ### FILE LOG REALIZATION
        file_log = open("log_file.txt",'a')
        file_log.write("\nAllarme attivato il giorno: {}  alle ore: {} \n".format(date,time))

        
        can_on_led.itemconfig(on_led, fill="#00FF00") # VERDE
        alarm_label.configure(text="Alarm Enabled",font=("Helvetica", 11))

        door_label.configure(text="DOOR: {}".format(str_door), font=("Helvetica",20))
        window_label.configure(text="WINDOW: {}".format(str_window),font=("Helvetica",20))
        pir_label.configure(text="MOTION: {}".format(str_pir),font=("Helvetica",20))

        file_log.close()
        

    
    print("STATE: {} BUTTON:{}\n".format(state,pushed_button))###########################################################
     
    root.after(100, acquisition_notification)

# ROOT WIDGET DECLARAION
root = Tk()
root.title("Alarm System")
root.geometry("800x460")
root.configure(bg='#F3F037')

# GLOBAL VARIABLES
global door_state
global window_state
global pir_state

global temp
global lux
global hum

global state
global pushed_button
global log_button


#### INITIALIZATION OF VARIABLES
state = "IDLE"
pushed_button = 0 # ALARM SYSTEM OFF - RED LED
log_button = 0

temp = 0
lux = 0
hum = 0
door_state = 0
window_state = 0
pir_state = 0

com = '/dev/ttyUSB0'
read_data = []

data_list = [
            door_state,
            window_state,
            pir_state,
            lux,
            temp,
            hum]

# INITIALIZATION FINITE STATE MACHINE - FSM CLASS
fsm = FSM(pushed_button,data_list)


"""###########################################################################

    SERIAL INTERFACE

############################################################################"""

# SERIAL INITIALIZATION - SERIAL CLASS
try:
    ser = SerialClass(com)
    print("Serial correctly initialaized")
except:
    print("Wrong serial initialization")
    time.sleep(2)

"""###########################################################################

                                        GUI PASS

############################################################################"""


"""#########################################################################

                    GUI PRINCIPALE

############################################################################"""
# Frame della Data in alto a sinistra
date_frame = LabelFrame(root ,text = "Data e Meteo", bd=5 ,padx=280,pady=80)
date_frame.place(x = 10, y = 10 )

date_label = Label(text="", fg="black", font=("Helvetica", 18))
time_label = Label(text="", fg="black", font=("Helvetica", 18))
date_label.place(x=20,y=30)
time_label.place(x=120,y=30)
root.after(1000, update_label())

my_lab = Label(date_frame,  text=" ")
my_lab.pack()
api_resp = weather()

sun_rise = api_resp['sys']['sunrise']
sun_set = api_resp['sys']['sunset']
sunrise = datetime.datetime.fromtimestamp(sun_rise).strftime("%H:%M:%S")
sunset = datetime.datetime.fromtimestamp(sun_set).strftime("%H:%M:%S")

weather_list = [
                api_resp["name"],
                api_resp["weather"][0]['main'],
                api_resp["weather"][0]['description'],
                api_resp['main']['temp'], # number
                api_resp['main']['temp_min'], #number
                api_resp['main']['temp_max'], # num
                api_resp['main']['pressure'], #num
                api_resp['main']['humidity'], # num
                sunrise,
                sunset]

wfont=("Helvetica", 12)
weather_1 = Label(text="City: "+weather_list[0], fg="black", font=("Helvetica", 18))
weather_2 = Label(text="Weather Condition: " + weather_list[1], fg="black", font=wfont)
weather_3 = Label(text="Weather Description: " + weather_list[2], fg="black",font=wfont)
weather_4 = Label(text="Outside Temperature: " + str(weather_list[3]) + "\u2103", fg="black" ,font=wfont)
weather_5 = Label(text="Daily Min Temp: "+str(weather_list[4]) + "\u2103", fg="black" ,font=wfont)
weather_6 = Label(text="Daily Max Temp: "+str(weather_list[5]) + "\u2103", fg="black" ,font=wfont)
weather_7 = Label(text="Outside Pressure : "+str(weather_list[6]) + "hPa", fg="black" ,font=wfont)
weather_8 = Label(text="Outside Humidity : "+str(weather_list[7]) + "%", fg="black" ,font=wfont)
weather_9 = Label(text="Sunrise Time: " + str(weather_list[8]), fg="black" ,font=wfont)
weather_10 = Label(text="Sunset Time: "+ str(weather_list[9]), fg="black" ,font=wfont)

weather_1.place(x= 300, y = 30)
weather_2.place(x= 20, y = 70)
weather_3.place(x= 20, y = 100)
weather_4.place(x= 20, y = 130)
weather_5.place(x= 20, y = 160)
weather_6.place(x= 20, y = 180)
weather_7.place(x= 300, y = 70)
weather_8.place(x= 300, y = 100)
weather_9.place(x= 300, y = 130)
weather_10.place(x= 300, y = 160)

# Frame Controllo padx=100,pady=25
control_frame = LabelFrame(root ,text = "Control" ,bd=5, padx=80,pady=80)
control_frame.place(x = 610, y = 10 )

alarm_label = Label(text="Alarm Disabled",font=("Helvetica", 11))
alarm_label.place(x= 650, y=25)

can_on_led = Canvas(width = 50, height = 50)
can_on_led.place(x = 680, y = 50)
on_led = can_on_led.create_oval(3,3,40,40)
can_on_led.itemconfig(on_led, fill="#FF0000")

control_button = Button(text="Start/Stop", command = status ,padx = 45, pady=10,bg="#D9B035")
control_button.place(x = 620, y = 100)

log_button = Button(text ="Log", padx=62, command = log_file, pady=10,fg="#000000",bg="#87878A")
log_button.place(x = 620, y= 155)

my_lab = Label(control_frame)
my_lab.pack(side=TOP)

# sensing frame 
sensing_frame = LabelFrame(root ,text = "Sensing" , bd = 5 ,padx=180,pady=75)
sensing_frame.place(x = 10, y = 230 )

temp_label = Label(text="", font=("Helvetica",20))
lux_label = Label(text="",font=("Helvetica",20))
hum_label = Label(text="",font=("Helvetica",20))

temp_label.place(x = 50 , y =255)
lux_label.place(x = 50, y = 315)
hum_label.place(x = 50, y = 375)

my_lab = Label(sensing_frame,  text="")
my_lab.pack()

# detection frame 
detection_frame = LabelFrame(root ,text = "Detection" , bd = 5 ,padx=185,pady=75)
detection_frame.place(x = 400, y = 230 )

door_label = Label(text="DOOR: ", font=("Helvetica",20))
window_label = Label(text="WINDOW: ",font=("Helvetica",20))
pir_label = Label(text="MOTION: ",font=("Helvetica",20))

door_label.place(x = 420 , y =255)
window_label.place(x = 420, y = 315)
pir_label.place(x = 420, y = 375)

# DOOR LED
cdoor_led = Canvas(width = 50, height = 50)
cdoor_led.place(x = 700, y = 250)
door_led = cdoor_led.create_oval(3,3,40,40)
cdoor_led.itemconfig(door_led, fill="#FF0000")

# WINDOW LED
cwindow_led = Canvas(width = 50, height = 50)
cwindow_led.place(x = 700, y = 310)
window_led = cwindow_led.create_oval(3,3,40,40)
cwindow_led.itemconfig(window_led, fill="#FF0000")

# PIR LED
cpir_led = Canvas(width = 50, height = 50)
cpir_led.place(x = 700, y = 368)
pir_led = cpir_led.create_oval(3,3,40,40)
cpir_led.itemconfig(pir_led, fill="#FF0000")


############ FUNZIONI #######################################################
# updating sensing and notification
acquisition_notification()
door_status()
window_status()
pir_status()

#############################################################################

my_lab = Label(detection_frame,  text=" " )
my_lab.pack()

root.mainloop()


### SERIAL CLOSING
try:
    ser.serial_close()
    print("Serial correctly closed")
except:
    print("Wrong serial close")


