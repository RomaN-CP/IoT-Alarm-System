"""

     CLASS WHICH READ SERIAL USB OF RASPBERRY PIE4
     
"""
import serial

class SerialClass:
    
    def __init__(self,com):
        self.com = com
        self.ser = serial.Serial(self.com,115200)
        self.ser.flushInput()
        self.out_data = [];

    def serial_read(self):

        i = 0
        read_data = []
        read_data.clear();
        
        for i in range(6):
            data = self.ser.readline()        
            read_data.append(data)

        door = read_data[0].decode()
        window = read_data[1].decode()
        PIR = read_data[2].decode()
        lux = read_data[3].decode()
        temp = read_data[4].decode()
        hum = read_data[5].decode()

        self.out_data = [ door,
                     window,
                     PIR,
                     lux,
                     temp,
                     hum
            ]
        
        return self.out_data
        
    def serial_close(self):  
        self.ser.close()



