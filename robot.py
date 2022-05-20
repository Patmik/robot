from Raspi_motorHAT import Raspi_MotorHAT
from gpiozero import DistanceSensor
import atexit
import leds_led_shim
from servos import Servos



class Robot():
    def __init__(self, motorhat_addr=0x6f):
        # inizjalizzacja dnakładki seterownika silniików zanjduącej się po podanym adresem
        self._mh = Raspi_MotoHAT(addr=motorhat_addr)
        
        #zmienne lokalne dla kazdego z silników
        self.left_motor = self._mh.getMotor(1)
        self.right_motor = self._mh.getMotor(2)

        #inicjalizacja czujników
        self.left_distance_sensor = DistanceSensor(echo=17, trigger =27, queue_len=2)
        self.left_distance_sensor = DistanceSensor(echo=5, trigger =6, queue_len=2)
        
        #inicjalizacja paska LED
        self.leds = leds_led_shim.Leds()

        #Ustawienie serwomotorów mechanizmu uchylno-obrotowego
        self.servos = Servos(addr=motorhat_addr)

        #upewnien sie ze silniki sie zatrzymają gdy program przestanie działać
        atexit.register(self.stop_all)

    def convert_speed(self,speed):
        #wybór jazdy
        mode = Raspi_MotorHat.RELEASE
        if speed > 0 :
            mode = Raspi_MotorHAT.FORWORD
        elif speed < 0:
            mode = Raspi_MotorHAT.BACKWARD

        #Przeskalowanie prędkości
        output_speed = (abs(speed)*255) // 100
        return mode, int(output_speed)


    def set_left(self, speed):
        mode , output_speed = self.convert_speed(speed)
        self.left_motor.setSpeed(output_speed)
        self.left_motor.run(mode)

    def set_right(self, speed):
        mode , output_speed = self.convert_speed(speed)
        self.right_motor.setSpeed(output_speed)
        self.right_motor.run(mode)

    def stop_motors(self):
        self.left_motor.run(Raspi_MotoHAT.RELEASE)
        self.right_motor.run(Raspi_MotoHAT.RELEASE) 

    def set_pan(self,angle):
        self.servos.set_servo_angle(1,angle)

    def set_tilt(self,angle):
        self.servos.set_servo_angle(0,angle)

    def stop_all(self):
        self.stop_motors()

        #Wygaszenie wyświetlacza
        self.leds.clear()
        self.leds.show()

        #Reset servomotorów
        self.servos.stop_all()