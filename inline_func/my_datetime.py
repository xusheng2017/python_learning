

from datetime import datetime,timedelta,timezone

now = datetime.now()
print('now = %s type = %s ' % (now , type(now)))
print('datetime to timestamp:' , now.timestamp())
print('timestamp to datetime:' , datetime.fromtimestamp(now.timestamp()))

dt = datetime(2018,6,3,19,12,20)
print(dt)

cday = datetime.strptime('2018-6-3 14:14:59' , '%Y-%m-%d %H:%M:%S')
print('strptime:' , cday)
print('timepstr:' , cday.strftime('%a,%m %d %H:%M'))


print('current time is :' , cday)
print('current time +10hours + 7days :' , cday + timedelta(days = 7 , hours = 10))



