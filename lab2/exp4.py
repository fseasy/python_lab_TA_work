#coding=utf-8
##@brief : get circular prime number . the question's answer is 55
import math
from exp2 import generate_prime_number_normal

def get_num_bits(num) :
    if num == 0 :
        return 1
    assert( num > 0 )
    #return int(math.floor(math.log10(num) + 1))
    bits = 0
    tmp_num = num
    while tmp_num >= 1 :
        bits += 1
        tmp_num = tmp_num / 10 ##!! I do get it wrong ~~ be more careful 
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
    prime_num2idx = {prime_nums[idx] : idx for idx in range(0,prime_nums_cnt)}
    for cur_prime_num_idx in range(0,prime_nums_cnt) :
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
    #print get_circular_prime(100)
    ## Bad Case : [2, 3, 5, 7, 11, 11, 13, 17, 31, 37, 71, 73, 79, 97] !! we need to remove reduplicative elements
    assert(len(get_circular_prime(100)) == 13)
    print len(get_circular_prime(1000000))
