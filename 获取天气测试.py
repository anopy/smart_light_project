import urequests
def fetchWeather():
    result = urequests.get("https://api.seniverse.com/v3/weather/now.json?key=SHm9Uhb8-jKGfVWme&location=zhengzhou&language=zh-Hans&unit=c")       
    return result.text
import dht
import machine
from machine import UART,Pin, SoftI2C,PWM
from pn532 import Pn532
import ssd1306
import ntptime
import ujson
import time
i2c = SoftI2C(scl=Pin(18),sda=Pin(19))
# 继电器gpio针脚：Pin15
p15 = machine.Pin(15,machine.Pin.OUT) 

# oled设置
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

data = fetchWeather()
print(data)
j=ujson.loads(data)
oled.font_load("GB2312-12.fon")# 所使用的字体时12号字体
addr=j['results'][0]['location']['name']
weather=j['results'][0]['now']['text']
temperature=j['results'][0]['now']['temperature']
oled.text("地点：%s"%addr,35,16)
oled.text("天气：%s"%weather,35,32)
oled.text("温度：%s℃"%temperature,35,48)
oled.show()
