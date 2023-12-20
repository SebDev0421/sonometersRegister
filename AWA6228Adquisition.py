import serial

from time import sleep

import csv
from datetime import datetime

#database connecttion

import mysql.connector


serialDevice = input("Serial device: ")
port = input("Port device: ")
filename = input("Name file:")
filename = filename+str(datetime.now().date)+'.csv'

activationCode = input("Activation code: ")

#token glc_eyJvIjoiOTU5OTM3IiwibiI6InN0YWNrLTc1NzA5MS1pbnRlZ3JhdGlvbi1hZGVzY29uc3VsdG9yaWExMjM0IiwiayI6IkQzMGU2RTFPaUNIN3cyUk05VTRSOEgwYSIsIm0iOnsiciI6InByb2QtdXMtZWFzdC0wIn19
print("Esperando dispositivo.....")
while True:
    try:
        ser = serial.Serial(port,9600)
        break
    except:
        #print('Device no found')
        pass
        

print('Device connect')
try:
 mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="sonometrosAdesConsultoria"
 )
 print(mydb)
 mycursor = mydb.cursor()
except:
   print("Error dataBase not connect!!")

print("Cargando......")
sleep(0.5)

commands = ["AWA0"]

with open(filename,'w') as csvfile:
           
           csvwriter = csv.writer(csvfile)
           csvwriter.writerow(['fecha','SPLZ','SPLC','SPLA','SPLB','SPLD','SPLT','SPLU',' 20kHz',' 16kHz','12k5Hz',' 10kHz','  8kHz',' 6k3Hz','  5kHz','  4kHz','3k15Hz',' 2k5Hz','  2kHz',' 1k6Hz','1k25Hz','  1kHz',' 800Hz',' 630Hz',' 500Hz',' 400Hz',' 315Hz',' 250Hz',' 200Hz',' 160Hz',' 125Hz',' 100Hz','  80Hz','  63Hz','  50Hz','  40Hz','31Hz5','  25Hz','  20Hz','  16Hz','12Hz5','  10Hz','   8Hz',' 6Hz3'])

while True:

    ser.write(commands[0].encode(encoding='ascii'))
    ser.flush()
    while ser.in_waiting:
     trame_read = ser.readline()
     #print(trame_read)
     
     dbM = trame_read.decode('cp850').split(';')
     #print(dbM)
     try:
      if(dbM[1] == "[data]"):
        dateTime =  dbM[2]
        year = dateTime[6:10]
        month =  dateTime[3:5]
        day = dateTime[0:2]
        hour = dateTime[11:]
        dateTime_out = '\''+year+'-'+month+'-'+day+' '+hour+'\'' 

        print(dateTime_out)
        powers = dbM[4]
        
        """ print(dateTime)
        print(powers) """

        arrayPowers = powers.split(',')
        
        val = []
        val.append(dateTime_out)
        

        for x in arrayPowers:
           val.append(x)
        
        print(val)
        
        with open(filename,'w') as csvfile:
           
           csvwriter = csv.writer(csvfile)
           csvwriter.writerow(val)
           

           csvfile.close()

           print("Data was save...")
           
        
        sql = 'INSERT INTO sonometesData (serial_sonometer,fecha,SPLZ,SPLC,SPLA,SPLB,SPLD,SPLT,SPLU, 20kHz, 16kHz,12k5Hz, 10kHz,  8kHz, 6k3Hz,  5kHz,  4kHz,3k15Hz, 2k5Hz,  2kHz, 1k6Hz,1k25Hz,  1kHz, 800Hz, 630Hz, 500Hz, 400Hz, 315Hz, 250Hz, 200Hz, 160Hz, 125Hz, 100Hz,  80Hz,  63Hz,  50Hz,  40Hz,31Hz5,  25Hz,  20Hz,  16Hz,12Hz5,  10Hz,   8Hz, 6Hz3) VALUES ('+serialDevice

        for i in val:
           sql = sql + ',' + i

        
        sql = sql + ')'

        #print(sql)
        
        mycursor.execute(sql)

        mydb.commit()
     except TypeError:
      pass
      

     #trame_read.split(';')

    


    """ try:
        dataRecive = ser.read()
        responseDevice = responseDevice + dataRecive.decode('utf-8')
    except:
        print(responseDevice)
        break """

    sleep(1)
    