from robot import Robot
from time import time

class ObstacleAvoidingBehavior:
    """Proste unikanie przeszkód"""
    def __init__(self, the_robot):
        self.robot = the_robot
        self.speed = 60

    def get_motor_speed(self, distance):
        """Ta metoda wybiera predkosc dla silnika w oparciu o odczyt czujnikow"""
        if distance < 0.2:
            return -self.speed
        else:
            return self.speed

    def run(self):
        self.robot.set_pan(0)
        self.robot.set_tilt(0)

        while True:
            #Odczytanie odległości podanej w mterach
            left_distance = self.robot.left_distance_sensor.distance
            right_distance = self.robot.right_distance_sensor.distance

            print ("Lewy: {l:.2f}, Prawy: {r:.2f}".format(l = left_distance, r = right_distance))

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