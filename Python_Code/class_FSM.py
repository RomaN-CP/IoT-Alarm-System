"""

    Class which controls the states of the system

"""
from class_telegram import TelegramMessage
import time
import pygame

tm = TelegramMessage()

class FSM:

    def __init__(self, pushed_button, data_list):
        self.pushed_button = pushed_button
        self.data_list = data_list

    def idle_state(self, state, pushed_button, data_list):
    
        pushed_button = pushed_button
        self.data_list = data_list
        state = state
        button_message = False
        
        door_state = self.data_list[0]
        window_state = self.data_list[1]
        pir_state = self.data_list[2]
        lux = self.data_list[3]
        temp = self.data_list[4]
        hum = self.data_list[5]
        
        if door_state == 0:
            str_door = "Closed"
        else:
            str_door = "Open"
            
        if window_state == 0:
            str_window = "Closed"
        else:
            str_window = "Open"
            
        if pir_state == 0:
            str_pir = "No"
        else:
            str_pir = "Yes"
        
        message = tm.Read()
        
        data_message = "Luminosity: {} lux \nTemperature: {} \u2103\nRel. Humidity: {} %".format(lux,temp,hum)
        state_message = "Door state: {}\nWindow State: {}\nMotion: {}".format(str_door,str_window,str_pir)
        legend_message = """Bot can receive following comands:\n
/active - Activation of Antitheft system.\n
/deactive - Deactivation of Antitheft system.\n
/data - List of data of sensors\n
/state - State of system (On/Off)\n"""

        if pushed_button == 0:
            if message == "/data":
                tm.Send(data_message,button_message)
                state = "IDLE"
                pushed_button = 0
                return state , pushed_button
                
            elif message == "/state":
                tm.Send(state_message,button_message)
                state = "IDLE"
                pushed_button = 0
                return state , pushed_button
            
            elif message == "/active":
                tm.Send("Alarm correctly activated",button_message)
                ## PASSAGGIO IN ACTIVE
                state = "ACTIVE"
                pushed_button = 1
                return state , pushed_button
                
            elif message != "/date" and message!= "/state" and message!= "/activate":
                tm.Send(legend_message,button_message)
                state = "IDLE"
                pushed_button = 0
                return state , pushed_button
            
            elif message =="":
                pass
            
            else:
                pass
        elif pushed_button == 1:
            tm.Send("Alarm Correctly Activated",True)
            ## PASSAGGIO IN ACTIVE
            state = "ACTIVE"
            pushed_button = 1
            return state , pushed_button
                
        

    def active_state(self, state, pushed_button, data_list):

        
        pushed_button = pushed_button
        self.data_list = data_list
        state = state
        button_message = False

        print("active"," button: ",pushed_button)
        
        door_state = self.data_list[0]
        window_state = self.data_list[1]
        pir_state = self.data_list[2]
        lux = self.data_list[3]
        temp = self.data_list[4]
        hum = self.data_list[5]

        if door_state == 0:
            str_door = "Closed"
        else:
            str_door = "Open"
            
        if window_state == 0:
            str_window = "Closed"
        else:
            str_window = "Open"
            
        if pir_state == 0:
            str_pir = "No"
        else:
            str_pir = "Yes"
        
        message = tm.Read()
        
        data_message = "Luminosity: {} lux \nTemperature: {} \u2103\nRel. Humidity: {} %".format(lux,temp,hum)
        state_message = "Door state: {}\nWindow State: {}\nMotion: {}".format(str_door,str_window,str_pir)
        legend_message = """Bot can receive following comands:\n
/active - Activation of Antitheft system.\n
/deactive - Deactivation of Antitheft system.\n
/data - List of data of sensors\n
/state - State of system (On/Off)\n"""

        alarm_level_1 = door_state  and pushed_button == 1
        alarm_level_2 = window_state and pushed_button == 1
        alarm_level_3 = (alarm_level_1 or alarm_level_2) and pir_state and pushed_button == 1
        
        ## Gestione Allarme
        if alarm_level_1 == 1 and alarm_level_2 != 1 and alarm_level_3 != 1:
            state = "ALARM"
            pushed_button = 1
            return state, pushed_button
        elif alarm_level_1 != 1 and alarm_level_2 == 1 and alarm_level_3 != 1:
            state = "ALARM"
            pushed_button = 1
            return state, pushed_button
        elif alarm_level_1 == 1 and alarm_level_2 == 1 and alarm_level_3 != 1:
            state = "ALARM"
            pushed_button = 1
            return state, pushed_button
        elif alarm_level_3:
            state = "ALARM"
            pushed_button = 1
            return state, pushed_button
            
        ###################################################################

        if pushed_button == 1:
            if message == "/data":
                tm.Send(data_message,button_message)
                state = "ACTIVE"
                pushed_button = 1
                return state, pushed_button
                
            elif message == "/state":
                tm.Send(state_message,button_message)
                state = "ACTIVE"
                pushed_button = 1
                return state, pushed_button

            elif message == "/deactive":
                tm.Send("Alarm Correctly Deactivated",button_message)
                ## PASSAGGIO IN IDLE
                state = "IDLE"
                pushed_button = 0
                return state, pushed_button
                
            elif message!="/deactive" and message !="/data" and message!="/state":
                tm.Send(legend_message,button_message)
                state = "ACTIVE"
                pushed_button = 1
                return state, pushed_button

            elif message =="":
                pass
     
            else:
                pass
        elif pushed_button == 0:
                tm.Send("Alarm Correctly Deactivated",True)
                ## PASSAGGIO IN IDLE
                state = "IDLE"
                pushed_button = 0
                return state, pushed_button


    def alarm_state(self, state, pushed_button, data_list):

        pushed_button = pushed_button
        self.data_list = data_list
        state = state
        button_message = False

        door_state = self.data_list[0]
        window_state = self.data_list[1]
        pir_state = self.data_list[2]
        
        message = tm.Read()
        print("alarm", " button: ",pushed_button)
        alarm_level_1 = door_state == 1
        alarm_level_2 = window_state == 1
        alarm_level_3 = (door_state == 1 or window_state == 1)  and pir_state == 1

        if pushed_button == 1:
            
            if message =="/deactive": 
                # passaggio in IDLE
                tm.Send("Alarm Correctly Deactivated",button_message)
                state = "IDLE"
                pushed_button = 0
                return state, pushed_button
            
            elif message =="":
                
                if alarm_level_1 == 1 and alarm_level_2 != 1 and alarm_level_3 != 1:
                    tm.Send("ALRM! THE DOOR IS OPEN",True)
                    state = "ALARM"
                    pushed_button = 1
                    return state, pushed_button
                
                elif alarm_level_1 != 1 and alarm_level_2 == 1 and alarm_level_3 != 1:
                    tm.Send("ALARM! THE WINDOW IS OPEN",True)
                    state = "ALARM"
                    pushed_button = 1
                    return state, pushed_button

                elif alarm_level_1 == 1 and alarm_level_2 == 1 and alarm_level_3 != 1:
                    tm.Send("ALARM! THE DOOR AND WINDOW ARE OPEN",True)
                    state = "ALARM"
                    pushed_button = 1
                    return state, pushed_button
                
                elif alarm_level_3:
                    tm.Send("ALARM! INTRUDER IN HOUSE",True)
                    #playsound('//home//pi//Desktop//TelosB_Finale//b.mp3')
                    
                    pygame.mixer.init()
                    pygame.mixer.music.load("c_2.mp3")
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy() == True:
                        continue
                    
                    
                    state = "ALARM"
                    pushed_button = 1
                    return state, pushed_button


        elif pushed_button == 0:
            tm.Send("Alarm Correctly Deactivated",True)
            state = "IDLE"
            pushed_button = 0
            return state, pushed_button

   
        
            
            





        
        
        
        
        

        

