from turtle import circle
import pyfirmata
import atexit
from servos import Servos
import time as time

class Robot():
    def __init__(self,arduino='/dev/ttyACM0'):
        #inizjazliacja arduino
        self._ard = pyfirmata.Arduino(arduino)

        #zmienne dla każdego z silników      
        
        self.l_pwm = self._ard.get_pin('d:5:p')     #moc
        self.l_dir=self._ard.get_pin('d:4:o')       #kierunek
        self.r_pwm=self._ard.get_pin('d:6:p')       #moc
        self.r_dir=self._ard.get_pin('d:9:o')       #kierunek

        #ustawienie serwomotorów mechanizmu uchylno-obrotowego
        self.servos = Servos(arduino='/dev/ttyACM0')

        #upewnienie się ze silnisi się zatrzymają gdy prograzm przestanie działać
        atexit.register(self.stop_all)
   
    
    def convert_speed(self,speed):
        #wybor jazdy
        mode = 1
        if speed > 0:
            mode = 1
        elif speed < 0:
            mode = 0

        #przeskalowanie prędkości
        output_speed = (abs(speed)*50)//100
        return mode, int(output_speed)
    
    def set_left(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.l_pwm.write(output_speed)
        self.l_dir.write(mode)
    
    def set_right(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.r_pwm.write(output_speed)
        self.r_dir.write(mode)

    def stop_motors(self):
        self.l_pwm.write(0)   
        self.l_dir.write(1)      
        self.r_pwm.write(0)     
        self.r_dir.write(1)  


    #serwomechanizmy
    def set_pan(self,angle):
        self.servos.set_servo_angle('servo1',angle)
    
    def set_tilt(self,angle):
        self.servos.set_servo_angle('servo2',angle)

    
    def stop_all(self):
        self.stop_motors()
        self.servos.stop_all()


