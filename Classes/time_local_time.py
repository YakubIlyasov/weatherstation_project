from datetime import datetime  # libraries


class time_local_time:  # class for getting local time
    def __init__(self, time_zone=1, season_hour=1):  # init object
        self.__time_zone = time_zone  # hours to add (x) or decrease (-x) for your time zone
        self.__season_hour = season_hour  # winter (-1) or summer (1) hour

    def get_local_time(self):  # returns string of local time
        time_hours = str(datetime.now())[11:13]
        time_minutes = str(datetime.now())[14:16]
        time_hours = str(int(time_hours) + self.__time_zone + self.__season_hour)
        time_now = time_hours + ":" + time_minutes
        return time_now  # return local time

    def get_local_date(self):  # returns string of local date
        date_now = str(datetime.now())[0:11]  # get date
        # if time now is below 24 hours and the time (including time zone and season hour)
        # is below the sum of time zone and season hour (is it still yesterday?)
        # use the date of the next day
        if int(str(datetime.now())[11:13]) > (24 - self.__time_zone - self.__season_hour) \
                and int(self.get_local_time()[0:2]) < (self.__time_zone + self.__season_hour):
            date_now = date_now[0:8] + str(int(date_now[8:10]) + 1)  # increase day
        return date_now  # return local date
