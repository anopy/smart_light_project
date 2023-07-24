import ntptime
import time
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        clear(0)
        wlan.connect('CMCC-dHWL', 'z13592481333')
        while not wlan.isconnected():
            pass
            return("Connected!")
def sync_ntp():
    print("connecting to server")
    import ntptime
    try:
        ntptime.NTP_DELTA = 3155644800  # UTC+8
        ntptime.host = 'ntp1.aliyun.com'  # 使用阿里服务器
        ntptime.settime()  # 时间赋值给系统
    except Exception as e:
        pass
        
do_connect()
time.sleep(2)
sync_ntp()
def zero_str(str_num):
    num=int(str_num)
    num_str=None
    if num>9:
        num_str=str_num
    else:
        num_str="0"+str(str_num)
    return num_str
week_arr=["Mon","Tues","Wed","Thur","Fri","Sat","Sun"]
localtime_now=time.localtime()
week_text=week_arr[localtime_now[6]]
# time_str='%s-%s-%s-%s:%s:%s'%(localtime_now[0],localtime_now[1],localtime_now[2],localtime_now[3],localtime_now[4],localtime_now[5])
time_str='%s-%s %s:%s'%(zero_str(localtime_now[1]),zero_str(localtime_now[2]),zero_str(localtime_now[3]),zero_str(localtime_now[4]),)
print(time_str,week_text)

