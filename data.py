import datetime as dt

class Data:
    def __init__(self,year = None, month = None, day = None, hour = None, minutess = None, secondss = None):
        self.dict_for_month = {
            "Січ":1,
            "Лют":2,
            "Бер":3,
            "Кві":4,
            "Тра":5,
            "Чер":6,
            "Лип":7,
            "Сер":8,
            "Вер":9,
            "Жов":10,
            "Лис":11,
            "Гру":12
        }
        if year and month and day and hour and minutess and secondss:
            while secondss >= 60:
                secondss -= 60
                minutess += 1
            while minutess >= 60:
                minutess -= 60
                hour += 1
            while hour >= 24:
                hour -= 24
                day += 1
            
            while day > self.months_to_num(month,year):
                if month != "Гру":
                    day -= self.months_to_num(month,year)
                    num_month = self.dict_for_month[month]
                    month = list(self.dict_for_month.items())[num_month][0]
                elif month == "Гру":
                    day -= self.months_to_num(month,year)
                    num_month = 0
                    year += 1
                    month = list(self.dict_for_month.items())[num_month][0]
            self.data = dt.datetime(year, self.dict_for_month[month], day, hour, minutess, secondss)
            
        elif year and month and day and hour == None and minutess == None and secondss == None:
            while day > self.months_to_num(month,year):
                if month != "Гру":
                    day -= self.months_to_num(month,year)
                    num_month = self.dict_for_month[month]
                    month = list(self.dict_for_month.items())[num_month][0]
                elif month == "Гру":
                    day -= self.months_to_num(month,year)
                    num_month = 0
                    year += 1
                    month = list(self.dict_for_month.items())[num_month][0]
            self.data = dt.datetime(year, self.dict_for_month[month], day)
    
        else:
            self.data = dt.datetime.now()

    def months_to_num(self, month, year):
        dict_for_values = {
                "Січ":31,
                "Лют":28,
                "Бер":31,
                "Кві":30,
                "Тра":31,
                "Чер":30,
                "Лип":31,
                "Сер":31,
                "Вер":30,
                "Жов":31,
                "Лис":30,
                "Гру":31
            }
        if (year%4 == 0 and year%100 !=0 or year%400 == 0):
            if str(month) == "Лют":
                return dict_for_values[str(month)] + 1
            else:
                return dict_for_values[str(month)]
        else:
            return dict_for_values[str(month)]
    
    def input_month(self, month):
        return self.dict_for_month[str(month)]

    def print_time(self):
        print(self.data.strftime("%A, %d. %B %Y %I:%M%p"))

    def get_year(self):
        return self.data.timetuple()[0]
    
    def get_month(self):
        month = self.data.timetuple()[1]
        return list(self.dict_for_month.items())[month-1][0]

    def get_days(self):
        return self.data.timetuple()[2]
    
    def get_hour(self):
        return self.data.timetuple()[3]

    def get_minute(self):
        return self.data.timetuple()[4]

    def get_seconds(self):
        return self.data.timetuple()[5]

    def add_years(self,year):
        for years in range(self.data.timetuple()[0],self.data.timetuple()[0] + year ):
                if (years%4 == 0 and years%100 !=0 or years%400 == 0):
                    self.data += dt.timedelta(days=366)
                else:
                    self.data += dt.timedelta(days=365)
        
    
    def add_month(self,month):
        dict_for_month = {
                1:31,
                2:28,
                3:31,
                4:30,
                5:31,
                6:30,
                7:31,
                8:31,
                9:30,
                10:31,
                11:30,
                12:31
            }
        while month >= 1:
            year = self.data.timetuple()[0]
            if (year%4 == 0 and year%100 !=0 or year%400 == 0):
                if self.data.timetuple()[1] == 2:
                    self.data += dt.timedelta(days=(dict_for_month[self.data.timetuple()[1]] + 1))
                else:
                    self.data += dt.timedelta(days=(dict_for_month[self.data.timetuple()[1]]))
            else:
                self.data += dt.timedelta(days=(dict_for_month[self.data.timetuple()[1]]))
            month -= 1
    
    def add_days(self,days):
        self.data += dt.timedelta(days=days)
    
    def add_hours(self,hours):
        self.data += dt.timedelta(hours=hours)

    def add_minutes(self,minutes):
        self.data += dt.timedelta(minutes=minutes)

    def add_seconds(self,seconds):
        self.data += dt.timedelta(seconds=seconds)
    
    def to_string(self):
        self.year = self.get_year()
        self.month = self.get_month()
        self.days = self.get_days()
        self.hour = self.get_hour()
        self.minute = self.get_minute()
        self.seconds = self.get_seconds()

        return f"{self.year}-{self.month}-{self.days} {self.hour}:{self.minute}:{self.seconds}"
        

data = Data(2022,"Бер",1)
print(data.to_string())