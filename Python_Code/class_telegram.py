"""
 Module that send and receive message on telgram

"""
import requests
import time
import json

class TelegramMessage:

    def __init__(self):
        self.token = "bot_token"
        self.send_message = "sendMessage?chat_id=chat_id&text"
        self.receive_message = "getUpdates"
        self.old_message_id = self.MessageID()
        self.data_list = []
        self.message_id = 0
        self.message = ""
        
    def MessageID(self):
        try:
            base_url = "https://api.telegram.org/{}/{}".format(self.token,self.receive_message)
            invio = requests.get(base_url)
            api = json.loads(invio.content)
            api["result"].reverse()
            
            self.message_id = api["result"][0]["message"]["message_id"]
            
            return self.message_id
        except:
            time.sleep(5)
            self.message_id = None
            print("Error Connection")

    def Read(self):

        try:
            self.message_id = self.MessageID()
            old = self.message_id > self.old_message_id
            
            if old:
                base_url = "https://api.telegram.org/{}/{}".format(self.token,self.receive_message)
                invio = requests.get(base_url)
                api = json.loads(invio.content)
                api["result"].reverse()
                
                self.message = api["result"][0]["message"]["text"]
                return self.message
            else:
                self.message=""
                return self.message

        except:
            time.sleep(5)
            self.message =  "error"
            print("Error Reading")

    def Send(self,send_msg,button):

        if button == False:
            pass
        else:
            self.old_message_id = self.old_message_id-1
        
        try:
            
            self.message_id = self.MessageID()
            old = self.message_id > self.old_message_id
            
            if old:
                url = "https://api.telegram.org/{}/{}={}".format(self.token,self.send_message,send_msg)
                requests.get(url)
                # updating message id
                self.old_message_id = self.MessageID()
                
        except:
            time.sleep(5)
            print("Error Sending")
