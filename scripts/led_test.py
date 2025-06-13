from periphery import GPIO
import numpy as np
import time

LED = 120
LED2 = 126
LED3 = 134


GPIO_LED_OUT=GPIO(LED, 'out')
GPIO_LED2_OUT=GPIO(LED2, 'out')
GPIO_LED3_OUT=GPIO(LED3, 'out')

GPIO_LED_OUT.write(True)
GPIO_LED2_OUT.write(True)
GPIO_LED3_OUT.write(True)

time.sleep(10)

GPIO_LED_OUT.close();
GPIO_LED2_OUT.close();
GPIO_LED3_OUT.close();
