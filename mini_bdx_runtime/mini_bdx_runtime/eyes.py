from periphery import GPIO
import numpy as np
import time
from threading import Thread

LEFT_EYE_GPIO = 133
RIGHT_EYE_GPIO = 119

LEFT_EYE=GPIO(LEFT_EYE_GPIO, 'out')
RIGHT_EYE=GPIO(RIGHT_EYE_GPIO, 'out')

class Eyes:
    def __init__(self):

        LEFT_EYE.write(True)
        RIGHT_EYE.write(True)

        self.blink_duration = 0.1

        Thread(target=self.run, daemon=True).start()

    def run(self):
        while True:
            LEFT_EYE.write(False)
            RIGHT_EYE.write(False)
            time.sleep(self.blink_duration)
            LEFT_EYE.write(True)
            RIGHT_EYE.write(True)

            next_blink = np.random.rand() * 4  # seconds

            time.sleep(next_blink)


if __name__ == "__main__":
	e = Eyes()
	while True:
		time.sleep(1)
