from mini_bdx_runtime.antennas import Antennas
import random
import time

antennas = Antennas()

while True:

    trigger = random.random()
    antennas.set_position_left(trigger)
    antennas.set_position_right(trigger)

    time.sleep(1 / 50)