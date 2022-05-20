from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM

class Servos:
    def __init__(self, addr=0x6f, deflect_90_in_ms=0.6):
        """addr: Adres l2C cnipu PWM.
        odeflect_90_in_ms: zmienna do kalibracji serwomotorów,
        odchylenie o 90 wyrażone jako czas trwania impulsu
        w milisekundach"""
        self._pwm = PWM(addr)
        #ustawienie częstotliwości dla wszyzstkich silników
        pwm_frequency = 100
        self._pwm.setPWMFreq(pwm_frequency)
        #Czas trwania w milisekundach impulsu potrzebnego do ustawienia serwomotoru 
        #w środkowej pozycji
        servo_mid_point_ms = 1.5
        #Częstotliwość to 1 podzielone przez okres, ale jako że używamy milisekund, zostosujemy 1000
        period_in_ms = 1000/pwm_frequency
        #Nasz chip ma 4096 kroków w każdym okresie
        pulse_steps = 4096
        #Liczba kroków na milisekunde
        steps_per_ms = pulse_steps/ period_in_ms
        #Kroki na stopień
        self.steps_per_degree = (deflect_90_in_ms*steps_per_ms)/90
        #Środkowe ustawienie wurażone w liczbie kroków
        self.servo_mid_point_steps = servo_mid_point_ms*steps_per_ms
        #Mapa kanałów
        self.channels =[0,1,14,15]
    
    def stop_all(self):
        #0 na początku oznacza brak impulstu
        off_bit = 4096 # bit 12 to bit wyłaczający
        self._pwm.setPWM(self.channels[0], 0, off_bit)
        self._pwm.setPWM(self.channels[1], 0, off_bit)
        self._pwm.setPWM(self.channels[2], 0, off_bit)
        self._pwm.setPWM(self.channels[3], 0, off_bit)

    def _convert_degrees_to_steps(self,position):
        return int(self.servo_mid_point_steps+(position*self.steps_per_degree))

    def set_servo_angle(self, channel,angle):
        """position: Pozycja w stopniach, liczona od środka. od -90 do 90"""
        #Sprwadzenie
        if angle>90 or angle <-90:
            raise ValueError("kąt spoza zakresu")
        #Ustawienie pozycji
        off_step = self._convert_degrees_to_steps(angle)
        self._pwm.setPWM(self.channels[channel], 0, off_step)

