import robot
from time import sleep

#Jazda prosto
def straight(bot, seconds):
    bot.set_left(100)
    bot.set_right(100)
    sleep(seconds)

#skręt w lewo
def turn_left(bot, seconds):
    bot.set_left(20)
    bot.set_right(80)
    sleep(seconds)

#skręt w prawo
def turn_right(bot, seconds):
    bot.set_left(80)
    bot.set_right(20)
    sleep(seconds)

#obrót w lewo
def spin_left(bot, seconds):
    bot.set_left(-100)
    bot.set_right(100)
    sleep(seconds)


bot = robot.Robot()
straight(bot, 1)
turn_right(bot, 1)
straight(bot, 1)
turn_left(bot, 1)
straight(bot, 1)
turn_left(bot, 1)
straight(bot, 1)
spin_left(bot, 1)