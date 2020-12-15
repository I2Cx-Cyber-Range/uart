import serial
import serial.tools.list_ports
from serial import SerialException
import threading
import time

def actions1():
    uart.write(bytes("display 20\n",'utf-8'))


def actions2():
    data1 = bytes("AAA",'utf-8')
    data2 = bytes([0x41,41,0x0D]) # Carriage return \n
    uart.write(data1+data2)

def loop():
    data = bytearray()#A
    for i in range(1, 50,1): #increment by 1
        data.append(0x41)
        uart.write(data + bytes([13]))
        print("Sent: ", len(data))
        time.sleep(0.1)

def searchUART():
    for port in serial.tools.list_ports.comports():
        if( (port.vid==1155) and (port.pid==22336)):
            return(port.device)
    return ""       

def ReceiveThread():
    while True:
        numBytes = uart.inWaiting()
        if numBytes > 0: 
            try:
                print(uart.read(numBytes).decode("utf-8"),end='')
            except UnicodeError as decode_error:
                next
            
        else:
            time.sleep(0.1)
    
def TransmitThread():
    print("Press 1 or 2: Send a command\nPress 3: Send commands within a loop\nCTRL+C: to quit\n\n")
    while True:
        var = input("")
        if(var == "1"):
            actions1()
        
        if(var == "2"):
            actions2()
        
        elif( var == "3"):
            loop()

        else:
            print("This choice does not exist\r\n")
        time.sleep(0.1)

try:
    firstAvailableDevice = searchUART()
    try:
        uart = serial.Serial(firstAvailableDevice, 115200, timeout=0,bytesize=8, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        if uart.isOpen():
            threading.Thread(target=TransmitThread).start()
            threading.Thread(target=ReceiveThread).start() 
        else:
            print("Please connect I²Cx Scanner board.")
    except SerialException:
        print("Please connect I²Cx Scanner board.")
        exit()
except (KeyboardInterrupt, SystemExit):
    exit()