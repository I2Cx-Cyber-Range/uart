import serial
import serial.tools.list_ports
from serial import SerialException
import threading
import time

def actions():
    uart.write(b'commande')

def boucle():
    for i in range(0, 10):
        uart.write(bytes("Command " + str(i),'utf-8'))
        time.sleep(0.1)

def searchUART():
    for port in serial.tools.list_ports.comports():
        if( (port.vid==1155) and (port.pid==22352)):
            return(port.device)
    return ""       

def ReceiveThread():
    while True:
        numBytes = uart.inWaiting()
        if numBytes > 0: 
            print(uart.read(numBytes).decode("utf-8"))
        else:
            time.sleep(0.1)
    
def TransmitThread():
    print("Press 1: Send a command\nPress 2: Send commands within a loop\nCTRL+C: to quit\n\n")
    while True:
        var = input("")
        if(var == "1"):
            actions()
        
        elif( var == "2"):
            boucle()

        else:
            print("Ce choix n'existe pas\n")
        time.sleep(0.1)

try:
    firstAvailableDevice = searchUART()
    try:
        uart = serial.Serial(firstAvailableDevice, 115200, timeout=0,bytesize=8, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        if uart.isOpen():
            threading.Thread(target=TransmitThread).start()
            threading.Thread(target=ReceiveThread).start() 
        else:
            print("Veuillez brancher la carte I²Cx Scanner.")
    except SerialException:
        print("Veuillez brancher la carte I²Cx Scanner.")
        exit()
except (KeyboardInterrupt, SystemExit):
    exit()