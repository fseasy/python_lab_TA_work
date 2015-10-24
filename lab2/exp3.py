#coding=utf-8
##@brief how may days which satisfied the condition : day is 1 and week day is 7 . answer is 171 in the question
class DayAndWeek(object) :
    __31_days_months = (1,3,5,7,8,10,12)
    __30_days_months = (4,6,9,11)
    __day_name = ("周一","周二","周三","周四","周五","周六","周日")
    @classmethod
    def is_leap_year(cls , year) :
        return ( ( year %4 == 0 and year % 100 != 0 ) or (year % 400 == 0) )

    @classmethod
    def get_days_of_month(cls , year , month) :
        if month in cls.__31_days_months :
            return 31
        elif month in cls.__30_days_months :
            return 30
        else :
            if cls.is_leap_year(year) :
                return 29
            else :
                return 28

    @classmethod
    def get_days_of_year(cls , year) :
        return 366 if cls.is_leap_year(year) else 365 
    
    @classmethod
    def _get_offset_days_from_starting_year(cls , year , month , day) :
        days_in_whole_months = [ cls.get_days_of_month(year , m) for m in range(1 , month)]
        days = sum(days_in_whole_months) + day 
        return days
        
    @classmethod
    def days_between2date_point(cls , s_y , s_m , s_d , t_y , t_m , t_d) :
        ## regularize the date to start of the year : 2015-10-22 -> 2015.01.10 + pass_days 
        later_year , former_year , later_month , former_month , later_day , former_day ,  is_negative = ( 
                                   t_y , s_y , t_m , s_m , t_d , s_d , False )
        if s_y > t_y or ( s_y == t_y and s_m > t_m  ) or (s_y == t_y and s_m == t_m and s_d > t_d) :
            later_year , former_year , later_month , former_month , later_day , former_day , is_negative = ( 
                                   s_y , t_y , s_m , t_m , s_d , t_d ,  True )
        former_year_passed_days = cls._get_offset_days_from_starting_year(former_year , former_month , former_day)
        later_year_passed_days = cls._get_offset_days_from_starting_year(later_year , later_month , later_day)
        days_in_whole_years = sum([cls.get_days_of_year(y) for y in range(former_year , later_year) ])
        
        all_days = days_in_whole_years - former_year_passed_days + later_year_passed_days
        if is_negative : 
            all_days = - all_days
        
        return all_days

    @classmethod
    def what_day_is_the_day(cls , base_day , passed_days) :
        passed_days %= 7 
        day = base_day + passed_days
        return day if day <= 7 else day%7
    @classmethod
    def format_day(cls , day_num) :
        if not 1 <= day_num <= 7 :
            return "Invalid"
        else :
            return cls.__day_name[day_num-1]


if __name__ == "__main__" :
    ## 1900.1.1 是 星期一
    init_year , init_month , init_day = 1900 , 1 , 1
    base_day = 1

    year , month , day = 2015 , 10 , 22
    passed_days = DayAndWeek.days_between2date_point(init_year , init_month , init_day , year , month , day)
    day_num = DayAndWeek.what_day_is_the_day(1 , passed_days )
    ## 2015年10月22日 是 周四
    assert(day_num == 4)
    day_name = DayAndWeek.format_day(day_num)
    print "{year}年{month}月{day}日 是 {day_name}".format(**locals())
    
    ## solving question
    ### 1901.01.01 -> 2000.12.31 , how may monday located at the start of a month ? 
    ### we enumerate every month ** day 1 , and judge whether it is equas to monday
    date_satisfied = []
    for year_ite in range(1901,2001) :
        for month_ite in range(1 , 13) :
            day = 1
            passed_days = DayAndWeek.days_between2date_point(init_year , init_month , init_day , year_ite , month_ite , day )
            day_num = DayAndWeek.what_day_is_the_day(1 , passed_days)
            if day_num == 7 :
                date_satisfied.append((year_ite , month_ite , 1))

    print date_satisfied
    print len(date_satisfied)

