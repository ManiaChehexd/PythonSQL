import time
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata
import mysql.connector
import datetime

run_count = 0
ADAFRUIT_IO_USERNAME = "Andreastest1"
ADAFRUIT_IO_KEY = "aio_PRBw64ceO1JW4lEMb4ZXChCR4SvB"


aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

board = pyfirmata.Arduino('COM4') 			#Dette er hvilken USB port jeg bruker til Arduinoen 

it = pyfirmata.util.Iterator(board)			#Denne gjør at pyfirmata kan brukes til Arduino
it.start()

digital_output = board.get_pin('d:13:o') #Dette er for output pinnen til LED 
analog_input = board.get_pin('a:0:i')  #Dette er input for Potensiometeret

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="test123456",
	database="3elda1"
)

mycursor = mydb.cursor()

print("Connected..")

sql = "INSERT INTO sensor(verdi,tid) VALUES (%s,%s)"

try:
	digital = aio.feeds('digital')
	print('Done')
except RequestError:
	feed = Feed(name='digital')
	digital = aio.create_feed(feed)
	print('Feed Error')

print(digital)




while True:
	print('Sending count:', run_count)
	aio.send_data('counter', run_count)				#Disse tre linjene med kode er der for å kommunisere med adafruit dashboardet
	aio.send_data('chart', analog_input.read())
	run_count += 1

	data = aio.receive(digital.key)

	print('Data: ', data.value)

	if data.value == "ON":
		digital_output.write(True)
	else:
		digital_output.write(False)

	time.sleep(2)
	
	verdi = analog_input.read()
	tid = datetime.datetime.now()

	val = (verdi, tid)

	print("Executing...")

	mycursor.execute(sql, val)
	mydb.commit()

	print("Done")