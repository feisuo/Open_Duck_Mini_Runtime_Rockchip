from periphery import GPIO
import numpy as np
import time

LEFT_EYE = 119
RIGHT_EYE = 125
DIRECTOR = 133


GPIO_LEFT_EYE_OUT=GPIO(LEFT_EYE, 'out')
GPIO_RIGHT_EYE_OUT=GPIO(RIGHT_EYE, 'out')
GPIO_DIRECTOR_OUT=GPIO(DIRECTOR, 'out')

GPIO_LEFT_EYE_OUT.write(True)
GPIO_RIGHT_EYE_OUT.write(True)
GPIO_DIRECTOR_OUT.write(True)

time.sleep(10)

GPIO_LEFT_EYE_OUT.write(False)
GPIO_RIGHT_EYE_OUT.write(False)
GPIO_DIRECTOR_OUT.write(False)

GPIO_LEFT_EYE_OUT.close()
GPIO_RIGHT_EYE_OUT.close()
GPIO_DIRECTOR_OUT.close()
