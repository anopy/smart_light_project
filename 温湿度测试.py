import dht
import machine
from time import sleep
from machine import UART,Pin, SoftI2C,PWM
from pn532 import Pn532
import ssd1306
import time
i2c = SoftI2C(scl=Pin(18),sda=Pin(19))

# 宽高设置
oled_width = 128
oled_height = 64

# 创建oled对象
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
def clear(self):
    oled.fill(0)
    oled.show()
def measure_temp(self):  # 数据储存在data中
    d = dht.DHT11(machine.Pin(13))
    d.measure()
    data_temp = "Temp: %s C" % (d.temperature())
    return(data_temp)
def measure_humi(self):  # 数据储存在data中
    d = dht.DHT11(machine.Pin(13))
    d.measure()
    data_humi = "Humi: %s" % (d.humidity())
    return(data_humi)
    
data_temp = measure_temp(0)
data_humi = measure_humi(0)

oled.text(str(data_temp),20,13)
oled.show()
oled.text(str(data_humi),20,33)
oled.show()
time.sleep(3)
clear(0)

