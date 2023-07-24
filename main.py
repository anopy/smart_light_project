from machine import I2C,Pin         #从machine模块导入I2C、Pin子模块
from ssd1306 import SSD1306_I2C     #从ssd1306模块中导入SSD1306_I2C子模块
import dht
from lib import urequests
import ntptime
import machine
from machine import UART,Pin, SoftI2C,PWM
from pn532 import Pn532
import time
import ujson
i2c = I2C(1,sda=Pin(19), scl=Pin(18),freq=100000)
oled = SSD1306_I2C(128, 64, i2c,addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c

oled.font_load("GB2312-12.fon")# 所使用的字体时12号字体
oled.fill(0)
# 继电器gpio针脚：Pin15
p15 = machine.Pin(15,machine.Pin.OUT) 

def clear(self):
    oled.fill(0)
    oled.show()
def fetchWeather():
    result = urequests.get("https://api.seniverse.com/v3/weather/daily.json?key=SHm9Uhb8-jKGfVWme&location=zhengzhou&language=zh-Hans&unit=c&start=0&days=3")       
    return result.text
def show_weather():
    result = fetchWeather()
    print(result)
    j=ujson.loads(result)
    print("\r\n\r\n")
    print(j['results'][0]['location']['name'])
    print(j['results'][0]['now']['text'])
    print(j['results'][0]['now']['temperature'])
    addr=j['results'][0]['location']['name']
    weather=j['results'][0]['now']['text']
    temperature=j['results'][0]['now']['temperature']
    oled.text("%s"%addr,35,13)
    oled.text("天气：%s"%weather,35,29)
    oled.text("温度：%s℃"%temperature,35,45)
    oled.show()
def measure_temp(self):  # 数据储存在data中
    d = dht.DHT11(machine.Pin(13))
    d.measure()
    data_temp = "温度: %s" % (d.temperature())+"℃"
    return(data_temp)
def measure_humi(self):  # 数据储存在data中
    d = dht.DHT11(machine.Pin(13))
    d.measure()
    data_humi = "湿度: %s" % (d.humidity())+"%"
    return(data_humi)
def zero_str(str_num):
    num=int(str_num)
    num_str=None
    if num>9:
        num_str=str_num
    else:
        num_str="0"+str(str_num)
    return num_str
def sync_ntp():
    print("connecting to server")
    import ntptime
    try:
        ntptime.NTP_DELTA = 3155644800  # UTC+8时区
        ntptime.host = 'ntp1.aliyun.com'  # 使用阿里ntp服务器授时
        ntptime.settime()  # 获取到的时间赋值给系统
    except Exception as e:
        pass
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('CMCC-dHWL', 'z13592481333')
        while not wlan.isconnected():
            pass
    print('WLAN connected')


# 前摇（
oled.text('欢迎使用！', 35, 20)
oled.show()
time.sleep(1)
oled.text('Developed by anopy', 15, 40)
oled.show()
time.sleep(2)
clear(0)

# 连接网络
oled.text('连接至网络…', 30, 30)
oled.show()
time.sleep(1.5)
do_connect()
clear(0)
oled.text('网络已连接', 32, 30)
oled.show()
time.sleep(2)
clear(0)

# 连接授时服务器
oled.text('连接服务器中…', 18, 30)
oled.show()
result = fetchWeather()
data_temp = measure_temp(0)
data_humi = measure_humi(0)
sync_ntp()
clear(0)
# ----------------------------------------------------main program---------------------------------
# 控制并确认灯光状态
while True:
    localtime_now=time.localtime()
    hr = int(zero_str(localtime_now[3]))
    if hr >= 20 or hr <= 6:
        p15.value(1) # ！！！待调试确定高低！！！
        print('灯为开启')
        sta = "开"
    else:
        p15.value(0)
        print('灯为关闭')
        sta = "关"
    week_arr=["周一","周二","周三","周四","周五","周六","周日"]
    localtime_now=time.localtime()
    week_text=week_arr[localtime_now[6]]
    time_str='%s月%s日   %s:%s'%(zero_str(localtime_now[1]),zero_str(localtime_now[2]),zero_str(localtime_now[3]),zero_str(localtime_now[4]),)
    print(time_str,week_text)
    # Page 1/4
    oled.text(time_str,15,10)
    oled.text(week_text,15,40)
    oled.text(str(data_temp),60,30)
    oled.text(str(data_humi),60,50)
    oled.show()
    time.sleep(3)
    result = fetchWeather()
    j=ujson.loads(result)
    clear(0)

    # Page 2/4
    print("\r\n\r\n")
    addr=j['results'][0]['location']['name']+"天气预报"
    oled.text(addr,15,6)
    to_date=str(j['results'][0]['daily'][1]['date'])
    to_temp = j['results'][0]['daily'][1]['high']+"℃"+"-"+j['results'][0]['daily'][1]['low']+"℃"
    to_sta = j['results'][0]['daily'][1]['text_day']
    oled.text('明天',15,26)
    oled.text(to_date,55,26)
    oled.text(addr,15,6)
    oled.text(to_temp,15,46)
    oled.text(to_sta,80,46)
    oled.show()
    time.sleep(3)
    clear(0)

    # Page 3/4
    addr2=j['results'][0]['location']['name']+"天气预报"
    oled.text(addr2,15,6)
    to_date2=str(j['results'][0]['daily'][2]['date'])
    to_temp2 = j['results'][0]['daily'][2]['high']+"℃"+"-"+j['results'][0]['daily'][2]['low']+"℃"
    to_sta2 = j['results'][0]['daily'][2]['text_day']
    oled.text('后天',15,26)
    oled.text(to_date2,55,26)
    oled.text(addr2,15,6)
    oled.text(to_temp2,15,46)
    oled.text(to_sta2,80,46)
    oled.show()
    time.sleep(3)
    clear(0)

    # Page 4/4
    oled.text('灯光状态：',15,6)
    oled.text(sta,80,6)
    oled.text('应急电源状态：',15,26)
    oled.text("开",100,26)
    oled.text('网络状态：',15,46)
    oled.text('已连接',80,46)
    oled.show()
    result = fetchWeather
    data_temp = measure_temp(0)
    data_humi = measure_humi(0)
    sync_ntp()
    localtime_now=time.localtime()
    time.sleep(2)
    clear(0)
