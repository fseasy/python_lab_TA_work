#coding=utf-8

import math

def sum_3_or_5_times_number(up_bound) :
    sum_val = 0 
    for ite in xrange(1 , up_bound) :
        if ( ite %3 == 0 ) or (ite %5 == 0) :
            sum_val += ite
    return sum_val

def sum_3_or_5_times_number_pythonic(up_bound) :
    nums = [ x for x in range(1,up_bound) if ( x%3 == 0) or (x % 5 == 0)  ]
    return sum(nums)

def generate_prime_number_normal(up_bound) :
    candidate_nums_is_prime = [True for i in range(0 , up_bound)]
    candidate_nums_is_prime[0:2] = [False , False ]
    prime_nums = []
    num = 2
    while num < up_bound :
        if candidate_nums_is_prime[num] :
            prime_nums.append(num)
            filter_num = num ** 2
            while filter_num < up_bound :
                candidate_nums_is_prime[filter_num] = False
                filter_num += num
        num += 1
    return prime_nums

class DayAndWeek(object) :
    __31_days_months = (1,3,5,7,8,10,12)
    __30_days_months = (4,6,9,11)
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

def get_num_bits(num) :
    if num == 0 :
        return 1
    assert( num > 0 )
    #return int(math.floor(math.log10(num) + 1))
    bits = 0
    tmp_num = num
    while tmp_num >= 1 :
        bits += 1
        tmp_num = tmp_num / 10
    return bits 

def generate_circular_numbers(num):
    num_bits = get_num_bits(num)
    curcular_nums = [ num ]
    pre_num = num
    base_num = 10 ** ( num_bits - 1 ) 
    for i in range(num_bits - 1 ) :
        first_bit = pre_num / base_num
        left_num = pre_num % base_num
        cur_num = left_num * 10 + first_bit
        curcular_nums.append(cur_num)
        pre_num = cur_num
    return list(set(curcular_nums))


def find_circular_prime_in_primes(prime_nums) :
    prime_nums_cnt = len(prime_nums)
    is_visited = [False] * prime_nums_cnt
    circular_prime_nums = []
    prime_num2idx = {prime_nums[idx] : idx for idx in xrange(0,prime_nums_cnt)}
    for cur_prime_num_idx in xrange(0,prime_nums_cnt) :
        if is_visited[cur_prime_num_idx] :
            continue
        cur_prime_num = prime_nums[cur_prime_num_idx]
        # is_visited[cur_prime_num_idx] = True ## Later we'll do it at loops 
        ## get all circular nums  
        circular_nums = generate_circular_numbers(cur_prime_num)
        #print circular_nums
        ## if all circular nums is prime ? we just need to find if it is in prime_num2idx !!
        # all_is_prime = reduce(lambda x , y  : ( x in prime_num2idx) and ( y in prime_num2idx) , circular_nums )
        all_is_prime = True
        for test_num in circular_nums :
            if test_num not in prime_num2idx :
                all_is_prime = False
                break
        if all_is_prime :
            circular_prime_nums.extend(circular_nums)
        for test_num in circular_nums :
            if test_num in prime_num2idx :
                num_idx = prime_num2idx[test_num]
                is_visited[num_idx] = True
    return sorted(circular_prime_nums) ## it is not in order

def get_circular_prime(up_bound) :
    prime_nums = generate_prime_number_normal(up_bound)
    circular_prime_nums = find_circular_prime_in_primes(prime_nums)
    return circular_prime_nums

if __name__ == "__main__" :
    ## 1
    print sum_3_or_5_times_number(1000)
    ## 2
    print ( sum(generate_prime_number_normal(2000000)))
    ## 3
    
    init_year , init_month , init_day = 1900 , 1 , 1
    base_day = 1
    year , month , day = 2015 , 10 , 22
    date_satisfied_num  = 0
    for year_ite in xrange(1901,2001) :
        for month_ite in xrange(1 , 13) :
            day = 1
            passed_days = DayAndWeek.days_between2date_point(init_year , init_month , init_day , year_ite , month_ite , day )
            day_num = DayAndWeek.what_day_is_the_day(1 , passed_days)
            if day_num == 7 :
                date_satisfied_num += 1
    print date_satisfied_num
    
    ## 4
    print len(get_circular_prime(1000000))
