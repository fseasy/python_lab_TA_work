#coding=utf-8
##@brief list all prime in range[2 , max) and sum it !
## In question , calc sum(prime_in_range(2,000,000)) , right result is  142,913,828,922
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

## For Fast-linear-generate-prime-number algorithm
def generate_prime_number(up_bound) :
    candidate_nums_is_prime = [ True for i in range(0 , up_bound) ]
    candidate_nums_is_prime[0:2] = [False , False]
    prime_nums = []
    prime_nums_cnt = 0
    logging.debug("start generate all prime numbers in range [2 , {:,}) with mode fast".format(up_bound))
    for num in range(2 , up_bound) :
        if candidate_nums_is_prime[num] : 
            prime_nums.append(num)
            prime_nums_cnt += 1
        prime_num_idx = 0
        while prime_num_idx < prime_nums_cnt :
        #for prime_num_idx in xrange(0,prime_nums_cnt) :
            cur_prime_num = prime_nums[prime_num_idx]
            to_be_filtered_num_idx = num * cur_prime_num
            if to_be_filtered_num_idx >= up_bound : 
                break
            candidate_nums_is_prime[to_be_filtered_num_idx] = False
            if num % cur_prime_num == 0 :
                break
            prime_num_idx += 1
        #if num % 100000 == 0 :
        #    logging.debug('processing number [{:,} ,{:,} )done'.format(num - 100000 , num))
    return prime_nums

## normal-linear-generate-prime-number algorithm
def generate_prime_number_normal(up_bound) :
    candidate_nums_is_prime = [True for i in range(0 , up_bound)]
    candidate_nums_is_prime[0:2] = [False , False ]
    prime_nums = []
    logging.debug("start generate all prime numbers in range [2 , {:,}) with mode normal".format(up_bound))
    for num in range(2 , up_bound) :
        if candidate_nums_is_prime[num] :
            prime_nums.append(num)
            for filter_num in range(num ** 2 , up_bound , num) :
                candidate_nums_is_prime[filter_num] = False
    return prime_nums


def get_sum_value_for_prime_number_in_range(up_bound , mode) :
    if mode == "fast" :
        prime_nums = generate_prime_number(up_bound)
    else :
        prime_nums = generate_prime_number_normal(up_bound)
    return sum(prime_nums)

########So Interesting ! the normal-linear-filter is much much faster than fast-linear-filter !!! ######

if __name__ == "__main__" :
    assert(get_sum_value_for_prime_number_in_range(10 , "normal") == get_sum_value_for_prime_number_in_range(10,"fast") == 17)
    if len(sys.argv) < 2 :
        print >>sys.stderr , "Usage : %s [number_up_bound]" %(sys.argv[0])
        exit(1)
    try :
        upbound = int(sys.argv[1])
    except ValueError , e :
        print >> sys.stderr , "Usage : %s [number_up_bound]" %(sys.argv[1])
        exit(1)
    mode = sys.argv[2] if len(sys.argv) >= 3 else "normal"

    print '{:,}'.format(get_sum_value_for_prime_number_in_range(upbound , mode))
