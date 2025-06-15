系统包安装：

apt update
apt install -y python3-pip python3.11-dev

--------------------------------------------

python3包安装：

注意：只能在root用户下安装

pip3 install -e . --break-system-packages

----------------------

环境设置：

在root根目录下，执行以下命令创建 .asoundrc 文件：

echo -e 'pcm.!default {\n    type hw\n    card 0\n}\n\nctl.!default {\n    type hw\n    card 0\n}' > /root/.asoundrc

-----------------------------------------------------

管脚对应操作：

1、GPIO out

​    pin15、pin32、pin35

示例：

>>> from periphery import GPIO
>>> gpio_pin_out=15	# GPIO端口
>>> gpio_out=GPIO(gpio_pin_out,'out')
>>> gpio_out.write(True)	# 设为高电平
>>> gpio_out.close()



2、GPIO in

​	pin14、pin30

示例：

>>> from periphery import GPIO
>>> gpio_pin_in=14	# GPIO端口
>>> gpio_in=GPIO(gpio_pin_in,'in')
>>> value = gpio_in.read()
>>> print(value)
>>> gpio_in.close()



3、PWM

​	pin31（pwm2）、pin34（pwm3）

示例：

>>> from periphery import PWM    
>>> pwm2=PWM(2,0)
>>> pwm2.frequency= 1e3
>>> pwm2.duty_cycle = 0.25
>>> pwm3=PWM(3,0)     
>>> pwm3.frequency= 1e3    
>>> pwm3.duty_cycle = 0.75 
>>> pwm2.enable()         
>>> pwm3.enable()
>>> pwm2.disable()
>>> pwm3.disable()



4、I2C  -  用于控制IMU，要配合adafruit-bno055包使用

​	pin4（SDA）、pin6（SCL）



5、串口uart

​	pin7（TXD）、pin10（RXD）



6、声卡播放：

pin11（MCLK）、pin16（SDO）、pin17（LRCK）、pin21（SDI）、pin28（SCLK）

示例：

>>> import pygame                                       

pygame 2.1.2 (SDL 2.26.5, Python 3.11.2)
Hello from the pygame community. https://www.pygame.org/contribute.html

>>> pygame.mixer.init(frequency=48000)                  
>>> pygame.mixer.music.set_volume(1.0)
>>> sound= pygame.mixer.Sound("/home/linaro/sn-48k.wav")
>>> sound.play()
>>> <Channel object at 0x7fa326b630>
>>> sound.stop()



7、rustypot 

示例：

>>> >>> import rustypot
>>>>>> c=rustypot.feetech('/dev/ttyS8', 1000000)            



8、IMU - BNO055

示例：

>>> from adafruit_extended_bus import ExtendedI2C as I2C
>>> import adafruit_bno055                              
>>>
>>> i2c_bus = I2C(3)                                    
>>> /usr/local/lib/python3.11/dist-packages/adafruit_blinka/microcontroller/generic_linux/i2c.py:30: RuntimeWarning: I2C frequency is not settable in python, ignoring!
>>>   warnings.warn(
>>>
>>> imu = adafruit_bno055.BNO055_I2C(i2c_bus) 

