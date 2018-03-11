# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 14:28:31 2018

@author: Gnaneshwar
"""

def businessDuration(startdate,enddate,starttime=None,endtime=None,weekendlist=[5,6],holidaylist=None,unit='min'):
    import pandas as pd
    from datetime import date, time, timedelta, datetime
    import numpy as np
    #Checking whether supplied startdate & enddate is date or datetime
    if type(startdate) is date:
        startdate = pd.to_datetime(startdate)
    if type(enddate) is date:
        enddate = datetime.combine(enddate,time(23,59,59))
    if starttime==None and endtime==None:
        starttime=time(0,0,0)
        endtime=time(23,59,59)
    if starttime==None or endtime==None:
        return np.nan
    if pd.isnull(startdate) or pd.isnull(enddate) or startdate>enddate:
        return np.nan
    else:
        deltatime = enddate-startdate
        days_diff = deltatime.components.days
        working_days = []
        for i in range(0,days_diff+1):
            tmp = pd.to_datetime(startdate+timedelta(i)).date()
            working_days.append(tmp)
        if holidaylist != None: #Remove public holidays
            working_days = [ibd for ibd in working_days if ibd not in holidaylist]
        if weekendlist != None: #Remove weekends
            working_days = [ibd for ibd in working_days if ibd.weekday() not in weekendlist]
        len_working_days = len(working_days)
        if len_working_days == 0: #no working days
            return np.nan
        elif len_working_days == 1: #1 working day
            if startdate.date() not in working_days:
                startdate = datetime.combine(working_days[0],time(0,0,0))
            if enddate.date() not in working_days:
                enddate = datetime.combine(working_days[0],time(23,59,59))
            if starttime <= endtime: #Eg. 9AM - 6PM
                #Calculate Starting day time in seconds
                if startdate.time() < starttime:
                    open_time = starttime
                elif startdate.time() >= starttime and startdate.time() <= endtime: 
                    open_time = startdate.time()
                else:
                    #open_time = time(0,0,0)
					return np.nan
                #Calculate Closing day time in seconds
                if enddate.time() < starttime:
                    #close_time = time(0,0,0)
					return np.nan
                elif enddate.time() >= starttime and enddate.time() <= endtime:
                    close_time = enddate.time()
                else:
                    close_time = endtime
            else: #Eg. 9PM - 3AM
                #Calculate Starting day time in seconds
                midnight_time = time(23,59,59)
                if startdate.time() < starttime:
                    open_time = starttime
                    close_time = midnight_time
                else:
                    open_time = startdate.time()
                    close_time = midnight_time
            add_seconds = ((close_time.hour*60*60)+(close_time.minute*60)+close_time.second) - ((open_time.hour*60*60)+(open_time.minute*60)+open_time.second)
        elif len_working_days == 2: #2 working day
            add_seconds = 0
            if starttime<=endtime: #Eg. 9AM - 6PM
                #Calculate Starting day time in seconds
                if startdate.time() < starttime:
                    open_time = starttime
                    close_time = endtime
                elif startdate.time() >= starttime and startdate.time() <= endtime: 
                    open_time = startdate.time()
                    close_time = endtime
                else:
                    open_time = time(0,0,0)
                    close_time = time(0,0,0)
                add_seconds += ((close_time.hour*60*60)+(close_time.minute*60)+close_time.second) - ((open_time.hour*60*60)+(open_time.minute*60)+open_time.second)
                #Calculate Closing day time in seconds
                if enddate.time() < starttime:
                    open_time = time(0,0,0)
                    close_time = time(0,0,0)
                elif enddate.time() >= starttime and enddate.time() <= endtime:
                    open_time = starttime
                    close_time = enddate.time()
                else:
                    open_time = starttime
                    close_time = endtime
                add_seconds += ((close_time.hour*60*60)+(close_time.minute*60)+close_time.second) - ((open_time.hour*60*60)+(open_time.minute*60)+open_time.second)
            else: #Eg. 9PM - 3AM
                #Calculate Starting day time in seconds
                midnight_time = time(23,59,59)
                if startdate.time() < starttime:
                    open_time = starttime
                    close_time = midnight_time
                else:
                    open_time = startdate.time()
                    close_time = midnight_time
                add_seconds += ((close_time.hour*60*60)+(close_time.minute*60)+close_time.second) - ((open_time.hour*60*60)+(open_time.minute*60)+open_time.second)
                #Calculate Closing day time in seconds
                if enddate.time() <= endtime:
                    open_time = time(0,0,0)
                    close_time = enddate.time()
                else:
                    open_time = time(0,0,0)
                    close_time = endtime
                add_seconds += ((close_time.hour*60*60)+(close_time.minute*60)+close_time.second) - ((open_time.hour*60*60)+(open_time.minute*60)+open_time.second)
        else: #more than 2 working day
            add_seconds = 0
            if startdate.date() not in working_days:
                startdate = datetime.combine(working_days[0],time(0,0,0))
            if enddate.date() not in working_days:
                enddate = datetime.combine(working_days[len_working_days-1],time(23,59,59))
            in_between_days = len_working_days-2
            if starttime<=endtime: #Eg. 9AM - 6PM
                #Calculate Starting day time in seconds
                if startdate.time() < starttime:
                    open_time = starttime
                    close_time = endtime
                elif startdate.time() >= starttime and startdate.time() <= endtime: 
                    open_time = startdate.time()
                    close_time = endtime
                else:
                    open_time = time(0,0,0)
                    close_time = time(0,0,0)
                add_seconds += ((close_time.hour*60*60)+(close_time.minute*60)+close_time.second) - ((open_time.hour*60*60)+(open_time.minute*60)+open_time.second)
                #Calculate Closing day time in seconds
                if enddate.time() < starttime:
                    open_time = time(0,0,0)
                    close_time = time(0,0,0)
                elif enddate.time() >= starttime and enddate.time() <= endtime:
                    open_time = starttime
                    close_time = enddate.time()
                else:
                    open_time = starttime
                    close_time = endtime
                add_seconds += ((close_time.hour*60*60)+(close_time.minute*60)+close_time.second) - ((open_time.hour*60*60)+(open_time.minute*60)+open_time.second)
                #Calculate in between days time in seconds
                in_between_days_seconds = in_between_days*(((endtime.hour*60*60)+(endtime.minute*60)+endtime.second) - ((starttime.hour*60*60)+(starttime.minute*60)+starttime.second))
                add_seconds += in_between_days_seconds
            else: #Eg. 9PM - 3AM
                #Calculate Starting day time in seconds
                midnight_time = time(23,59,59)
                if startdate.time() < starttime:
                    open_time = starttime
                    close_time = midnight_time
                else:
                    open_time = startdate.time()
                    close_time = midnight_time
                add_seconds += ((close_time.hour*60*60)+(close_time.minute*60)+close_time.second) - ((open_time.hour*60*60)+(open_time.minute*60)+open_time.second)
                #Calculate Closing day time in seconds
                if enddate.time() <= endtime:
                    open_time = time(0,0,0)
                    close_time = enddate.time()
                else:
                    open_time = time(0,0,0)
                    close_time = endtime
                add_seconds += ((close_time.hour*60*60)+(close_time.minute*60)+close_time.second) - ((open_time.hour*60*60)+(open_time.minute*60)+open_time.second)
                #Calculating business hrs between days in seconds
                half1 = ((midnight_time.hour*60*60)+(midnight_time.minute*60)+midnight_time.second) - ((starttime.hour*60*60)+(starttime.minute*60)+starttime.second)
                half2 = ((close_time.hour*60*60)+(close_time.minute*60)+close_time.second)
                in_between_days_seconds = in_between_days*(half1+half2)
                add_seconds += in_between_days_seconds
        if unit=='sec':
            bd = add_seconds
        elif unit=='min':
            bd = add_seconds/60
        elif unit=='hour':
            bd = (add_seconds/60)/60
        elif unit=='day':
            bd = ((add_seconds/60)/60)/24
        else:
            bd = np.nan
        return bd
