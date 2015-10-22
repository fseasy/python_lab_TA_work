#coding=utf-8
##@brief : for natual number in range [1 , max ) , sum all numbers which is 3 or 5 's times (将是3或5的倍数的求和)

def sum_3_or_5_times_number(up_bound) :
    sum_val = 0 
    for ite in range(1 , up_bound) :
        if ( ite %3 == 0 ) or (ite %5 == 0) :
            sum_val += ite
    return sum_val

def sum_3_or_5_times_number_pythonic(up_bound) :
    nums = [ x for x in range(1,up_bound) if ( x%3 == 0) or (x % 5 == 0)  ]
    return sum(nums)


if __name__ == "__main__" :
    assert( sum_3_or_5_times_number(10) == sum_3_or_5_times_number_pythonic(10) == 23 )

    print sum_3_or_5_times_number_pythonic(1000)
