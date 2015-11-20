#coding=utf8

import sys

LINE_LIMIT = 10
AND_PREFIX = "AND:"
OR_PREFIX = "OR:"

def build_inverse_index(inverse_idx) :
    line_num = 1
    while line_num < LINE_LIMIT + 1 :
        line = sys.stdin.readline()
        if line == '' :
            break
        words = line.split() 
        for word in words :
            if word in inverse_idx :
                inverse_idx[word].add(line_num)
            else :
                inverse_idx[word] = set([line_num])
        line_num += 1

def print_inverse_idx(inverse_idx) :
    sorted_idx = sorted(inverse_idx.items() , key=lambda tup : tup[0])
    for word , idx_set in sorted_idx :
        line_nums = list(idx_set)
        sorted_line_nums = sorted(line_nums)
        line_nums_str = u', '.join(map(str , sorted_line_nums))
        print u'{word}: {line_nums_str}'.format(**locals()).encode('utf8')

def search_in_mode_AND(inverse_idx , keywords) :
    '''
    operation `and` for every set of inverse index  for cooressponding keyword
    
    return list 
    '''
    candidate_sets = [ inverse_idx.get(keyword , set()) for keyword in keywords ]
    if len(candidate_sets) == 0 : return []
    line_nums =  list(reduce(lambda s1,s2 : s1 & s2 , candidate_sets))
    return sorted(line_nums)

def search_in_mode_OR(inverse_idx , keywords) :
    candidate_sets = [ inverse_idx.get(keyword , set()) for keyword in keywords]
    if len(candidate_sets) == 0 : return []
    line_nums = list(reduce(lambda s1 , s2 : s1 | s2 , candidate_sets))
    return sorted(line_nums)

def print_search_result(result_line_nums) :
    if len(result_line_nums) == 0 :
        print "None"
    else :
        print u", ".join(map(str , result_line_nums)).encode('utf8')

def cmd_handling(cmd_str,inverse_idx) :
    if cmd_str.startswith(AND_PREFIX) :
        keywords_line = cmd_str[len(AND_PREFIX):]
        keywords = keywords_line.strip().split()
        search_result = search_in_mode_AND(inverse_idx , keywords)
        print_search_result(search_result)
    elif cmd_str.startswith(OR_PREFIX) :
        keywords_line = cmd_str[len(OR_PREFIX) :]
        keywords = keywords_line.strip().split()
        search_result = search_in_mode_OR(inverse_idx , keywords)
        print_search_result(search_result)
    elif cmd_str == "PRINT" :
        print_inverse_idx(inverse_idx)
    else :
        keywords = cmd_str.strip().split()
        search_result = search_in_mode_AND(inverse_idx , keywords)
        print_search_result(search_result)

if __name__ == "__main__" :
    inverse_idx = {}
    build_inverse_index(inverse_idx)
    print_inverse_idx(inverse_idx)
    while True :
        try :
            #cmd_str = raw_input("INPUT SEARCH COMMAND\n")
            cmd_str = raw_input()
        except (EOFError,KeyboardInterrupt) , e :
            #print repr(e)
            exit(0)
        cmd_str = cmd_str.strip()
        if cmd_str == '' : continue
        #print cmd_str
        cmd_handling(cmd_str,inverse_idx)
