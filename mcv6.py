#!/usr/bin/python
import time
import os
import RPi.GPIO as GPIO # always needed with RPi.GPIO    
import sys, termios, atexit
import mpu6050
from select import select

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select


class KBHit:
    
    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        if os.name == 'nt':
            pass
        
        else:
    
            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)
    
            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
    
            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)
    
    
    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''
        
        if os.name == 'nt':
            pass
        
        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''
        
        s = ''
        
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        
        else:
            return sys.stdin.read(1)
                        

    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''
        
        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]
            
        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]
        
        return vals.index(ord(c.decode('utf-8')))
        

    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()
        
        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []
    
    

initial=36

min = 36
max = 52

motor1=initial
motor2=initial
motor3=initial
motor4=initial


variacion=1

mhz=400

GPIO.setmode(GPIO.BOARD)  # choose BCM or BOARD numbering schemes. I use BCM    

GPIO.setup(7, GPIO.OUT)# set GPIO 25 as an output. You can use any GPIO port    
qm1 = GPIO.PWM(7, mhz)    # create an object p for PWM on port 25 at 50 Hertz  
qm1.start(motor1)

GPIO.setup(11, GPIO.OUT)# set GPIO 25 as an output. You can use any GPIO port    
qm2 = GPIO.PWM(11, mhz)    # create an object p for PWM on port 25 at 50 Hertz  
qm2.start(motor2)

GPIO.setup(13, GPIO.OUT)# set GPIO 25 as an output. You can use any GPIO port    
qm3 = GPIO.PWM(13, mhz)    # create an object p for PWM on port 25 at 50 Hertz  
qm3.start(motor3)

GPIO.setup(15, GPIO.OUT)# set GPIO 25 as an output. You can use any GPIO port    
qm4 = GPIO.PWM(15, mhz)    # create an object p for PWM on port 25 at 50 Hertz  
qm4.start(motor4)

def setMotor1f():
	global motor1
	global qm1
	global max
	if motor1<max:
		motor1=motor1+variacion
		qm1.ChangeDutyCycle(motor1)

def setMotor1r():
	global motor1
	global qm1
	global min
	if motor1>min:
		motor1=motor1-variacion
		qm1.ChangeDutyCycle(motor1)

			
def setMotor2f():
	global motor2
	global qm2
	global max
	if motor2<max:
		motor2=motor2+variacion
		qm2.ChangeDutyCycle(motor2)

def setMotor2r():
	global motor2
	global qm2
	global min
	if motor2>min:
		motor2=motor2-variacion
		qm2.ChangeDutyCycle(motor2)

def setMotor3f():
	global motor3
	global qm3
	global max
	if motor3<max:
		motor3=motor3+variacion
		qm3.ChangeDutyCycle(motor3)

def setMotor3r():
	global motor3
	global qm3
	global min
	if motor3>min:
		motor3=motor3-variacion
		qm3.ChangeDutyCycle(motor3)
		
def setMotor4f():
	global motor4
	global qm4
	global max
	if motor4<max:
		motor4=motor4+variacion
		qm4.ChangeDutyCycle(motor4)
			
def setMotor4r():
	global motor4
	global qm4
	global min
	if motor4>min:
		motor4=motor4-variacion
		qm4.ChangeDutyCycle(motor4)

def setMotor12f():	
	setMotor1f()
	setMotor2f()

def setMotor12r():
	setMotor1r()
	setMotor2r()
	
def setMotor34f():
	setMotor3f()
	setMotor4f()

def setMotor34r():
	setMotor3r()
	setMotor4r()
			
def setMotor1234f():
	global min
	min=min+1
	setMotor1f()
	setMotor2f()
	setMotor3f()
	setMotor4f()
	
def setMotor1234r():
	setMotor1r()
	setMotor2r()
	setMotor3r()
	setMotor4r()

options = {"a": setMotor1f,"z": setMotor1r,"s": setMotor2f,"x": setMotor2r,"d": setMotor3f,"c": setMotor3r,"f": setMotor4f,"v": setMotor4r,"h": setMotor12f,"n": setMotor12r, "j": setMotor34f,"m": setMotor34r,"o": setMotor1234f,"l": setMotor1234r}
	
def updateEngine(keyr):	
	global options
	if keyr=="a" or keyr=="z" or keyr=="s" or keyr=="x" or keyr=="d" or keyr=="c" or keyr=="f" or keyr=="v" or keyr=="h" or keyr=="n" or keyr=="j" or keyr=="m" or keyr=="o" or keyr=="l":
		func = options[keyr]
		func()

def pidX(anguloX):
	if anguloX>0:
		setMotor1f()
		setMotor2r()
	else:
		setMotor2f()
		setMotor1r()
		
def pidY(anguloY):
	if anguloY>0:
		setMotor3f()
		setMotor4r()
	else:
		setMotor4f()
		setMotor3r()
try:
	print("*** Disconect EXC ower")
	res=raw_input()
	print("Connect power to ESC and wait beep-beep and press enter")
	res=raw_input()

	kb = KBHit()
	while True:
		os.system("clear");
		print("start controls:");
		print("motor 1:",motor1);
		print("motor 2:",motor2);
		print("motor 3:",motor3);
		print("motor 4:",motor4);
		
		if kb.kbhit():
			keyr = kb.getch()
			updateEngine(keyr)
			
		angulos = mpu6050.getAnglesXY()
		pidX(angulos[0])
		pidY(angulos[1])
		print("anguloX",angulos[0])
		print("anguloY",angulos[1])

		
except KeyboardInterrupt:
	pass
qm1.stop()
qm2.stop()
qm3.stop()
qm4.stop()
GPIO.cleanup()
