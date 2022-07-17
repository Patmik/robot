import pyfirmata

class Servos:
    def __init__(self,arduino='/dev/ttyACM0'):
        self._servo = pyfirmata.Arduino(arduino)
        self.servo1 = self._servo.get_pin('d:8:s')
        self.servo2 = self._servo.get_pin('d:7:s')
        

    def stop_all(self):
        self.servo1.write(65)
        self.servo2.write(0)

    
    def set_servo_angle(self,motor,angle):

        if angle>180 or angle <0:
            raise ValueError("kąt spoza zakresu")
        elif motor == 'servo1':
            self.servo1.write(angle)
        elif motor == 'servo2':
            self.servo2.write(angle)

      
