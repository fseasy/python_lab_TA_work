#coding=utf-8
'''
This code is for Evaluation of ISBN with 10 bits only . it is redundant , but may be robust .
'''
INVALID_FORMAT_TIPS = "Invalid ISBN Format"
INVALID_TIPS = "Invalid ISBN"
VALID_TIPS = "Valid ISBN"

def check_isbn_format(isbn_str) :
    if type(isbn_str) != str :
        return False
    isbn_parts = isbn_str.split('-')
    ## 4 parts
    if len(isbn_parts) != 4 :
        return False
    ## previous 3 parts length >= 1 , the last part length == 1 ;
    for pre_part in isbn_parts[0:3] :
        if len(pre_part) < 1 :
            return False
    if len(isbn_parts[-1]) != 1 :
        return False
    ## total length is 10
    if sum(map(len , isbn_parts)) != 10 :
        return False
    ## previous 9 characters are number , while the last is 'X' or 'x' or number
    for pre_char in ''.join(isbn_parts[0:3]) :
        #if not ( 0 <= int(pre_char) <= 9 ) : #! int() may be dangerous 
        if not ( '0' <= pre_char <= '9' ) :
            return False
    last_char = isbn_parts[3]
    if ( not '0' <= last_char <= '9' ) and  ( last_char not in ('X' , 'x') ) :
        return False
    
    return True

def trans_isbn2digits(isbn_str) :
    # assert isbn_str is valid in format
    isbn_parts = isbn_str.split('-')
    digits = map(int , ''.join(isbn_parts[0:3]) )
    if isbn_parts[-1] in ('X' , 'x') :
        digits.append(10)
    else :
        digits.append(int(isbn_parts[-1]))
    return digits

def verify_isbn_digits(isbn_digits) :
    # assert right isbn_digits
    idx = 10
    verify_sum = 0
    while idx > 0 :
        verify_sum += idx * isbn_digits[10 - idx]
        idx -= 1
    return verify_sum % 11 == 0

if __name__ == "__main__" :
    input_str = raw_input()
    check_format_status = check_isbn_format(input_str)
    if check_format_status == False :
        print INVALID_FORMAT_TIPS
        exit(0) ## Exit with 0
    digits = trans_isbn2digits(input_str)
    verify_status = verify_isbn_digits(digits)
    if verify_status :
        print VALID_TIPS
    else :
        print INVALID_TIPS
