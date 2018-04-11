# Business_Duration
Calculates business duration in days, hours, minutes and seconds by excluding weekends, public holidays and non-business hours

# How to install the package
pip install business-duration

# Example 1
```python
from business_duration import businessDuration
import pandas as pd
import holidays as pyholidays
from datetime import time

#Start date must be in standard python datetime format
start_date = pd.to_datetime('2017-07-01 02:02:00')

#Start date must be in standard python datetime format
end_date = pd.to_datetime('2017-07-07 04:48:00')

#Business open hour must be in standard python time format-Hour,Min,Sec
biz_open_time=time(7,0,0)

#Business close hour must be in standard python time format-Hour,Min,Sec
biz_close_time=time(17,0,0)

#US public holidays
US_holiday_list = pyholidays.US(state='CA')

#Business duration can be 'day', 'hour', 'min', 'sec'
unit_hour='hour'

#Printing output
print(businessDuration(startdate=start_date,enddate=end_date,starttime=biz_open_time,endtime=biz_close_time,holidaylist=US_holiday_list,unit=unit_hour))

#Result
#30.0

#Result is 30 hours because July 1st, 2nd are weekends and 4th is US public holiday. So 3 days remains with 10 business hours per day. 3 days*10 hours = 30 Hours
```

# Example 2
```python
from business_duration import businessDuration
from datetime import datetime

start_date = datetime.strptime("2018-01-01","%Y-%m-%d").date()
end_date = datetime.strptime("2018-03-31","%Y-%m-%d").date()

print(businessDuration(startdate=start_date,enddate=end_date,unit='day'))

#Result
65.0
```
