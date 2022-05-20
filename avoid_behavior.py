from robot import Robot
from time import time
from led_rainbow import show_rainbow

class ObstacleAvoidingBehavior:
    """Proste unikanie przeszkód"""
    def __init__(self, the_robot):
        self.robot = the_robot
        self.speed = 60
        #obliczanie liczby diod dal słupków
        self.led_half = int(self.robot.leds.leds_count/2)
        self.sense_colour = 255,0,0,

    def distance_to_led_bar(self,distance):
        #odwórcenie wartości tak aby mniejsza odległość przekładała się na większą liczbę diod
        inverted = max(0, 1.0 - distance)
        led_bar = int(round(inverted *self.led_half))
        return led_bar

    def display_state(self,lef_distance, right_distance):
        #Zgaszenie wszystkich diod LED
        self.robot.leds.clear()
        
        #Lewa strona
        led_bar = self.distance_to_led_bar(left_distance)
        show_rainbow(self.robot.leds,range(led_bar))
        self.robot.leds.set_range(range(led_bar),self.sense_colour)
        
        #prawa strona
        led_bar = self.distance_to_led_bar(right_distance)
        #Bardziej skomplikowane - zakres diod musi zaczynać się od adresu ostatniej diody
        #w słupku, a kończuyć na adresie ostaniej didoy w pwasku LED
        start = (self.robot.leds.count-1) - led_bar
        right_range = range(self.robot.leds.count-1, start, -1)
        show_rainbow(self.robot.leds, right_range)
        self.robot.leds.set_range(range(start,self.robot.leds.count-1),self.sense_colour)

        #zapalenie ustawionych diod LED
        self.robot.leds.show()


    def get_speeds(self, nearest_distance):
        if nearest_distance >=10:
            nearest_speed = self.speed
            furthest_speed = self.speed
            delay = 100
        elif nearest_distance >0.5:
            nearest_speed = self.speed
            furthest_speed = self.speed *0.8
            delay = 100
        elif nearest_distance > 0.2:
            nearest_speed = self.speed
            furthest_speed = self.speed*0.6
            delay = 100
        elif nearest_distance >0.1:
            nearest_speed = -self.speed *0.4
            furthest_speed = -self.speed
            delay = 100   
        else: #Kolizja
            nearest_speed = -self.speed
            furthest_speed = -self.speed
            delay = 250
        return nearest_speed, furthest_speed, delay


    def run(self):
        self.robot.set_pan(0)
        self.robot.set_tilt(0)

        while True:
            #Odczytanie odległości podanej w mterach
            left_distance = self.robot.left_distance_sensor.distance
            right_distance = self.robot.right_distance_sensor.distance
            #wyświetlanie odczytów z czujników
            self.display_state(left_distance, right_distance)

            print ("Lewy: {l:.2f}, Prawy: {r:.2f}".format(l = left_distance, r = right_distance))

            #ustalenie predkości silników na podstawei odległości
            nearest_speed, furthest_speed, delay = self. get_speed(min(left_distance,   right_distance ))
            print(f"Odległośći : l {left_distance :.2f}, r{right_distance :.2f}.\
                Prędkości: n: {nearest_speed}, f:{furthest_speed}. Pauza: {delay}")

            #ustawienie prędkości silników
            if left_distance < right_distance:
                self.robot.set_left(nearest_speed)
                self.robot.set_right(furthest_speed)
            else:
                self.robot.set_right(nearest_speed)
                self.robot.set_left(furthest_speed)

            #Zatrzymanie programu na czas okreslony przez zmianną delay
            sleep(delay * 0.001)

            #odczytanie odległości podanej w metrach
            left_speed = self.get_motor_speed(left_distance)
            self.robot.set_left(left_speed)
            right_speed = self.get_motor_speed(right_distance)
            self.robot.set_right(right_speed)

            #krótkie zatrzymanie robota
            sleep(0.05)

bot = Robot()
behavior = ObstacleAvoidingBehavior(bot)
behavior.run()