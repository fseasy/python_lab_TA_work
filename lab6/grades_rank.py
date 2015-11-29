#coding=utf8

GradeIdx2Name = ( u'语文' , u'数学' , u'英语',u'物理' , u'化学' , u'总成绩' , '平均分')
GradeName2Idx = { name:idx for idx , name in enumerate(GradeIdx2Name) }

class stage :
    STAGE_READ_DATA = 1
    STAGE_SINGLE_RANK = 2
    STAGE_SEARCH_ID = 3

def add_student_grade_info(grade_info , grade_info_str) :
    '''
    parse the grade_info_str , add the info to the grade_info struct
    grade_info : dict , { 'ID' : {'name' : str  , 'grades' : [grade1,grade2,...] , 'rank' : int } }
    grade_info_str : str , format like :  19020090040,秦心芯,123,131,100,95,100 
                           it is : ID,Name,5grades
                     NOTE ! unicode encoded!!
    '''
    parts = grade_info_str.strip().split(u',')
    if len(parts) != 7 : return
    grades = map(int , parts[2:])
    total_grades = sum(grades)
    avg_grades = float(total_grades) / len(grades)
    grades.extend([total_grades , avg_grades])
    ID = parts[0]
    name = parts[1]
    grade_info[ID] = {'name':name , 'grades':grades , 'rank': -99}

def select_sort(data , cmp_func=cmp , reverse=False) :
    '''
    a basic sort method. 
    first , set 1st elements as the min , and then to traversal the 2 ~ n elements to find the really min value .
    then ,  set the 2rd , 3th , .. n-th
    data : list
    '''
    if reverse : inner_cmp_func = lambda d1,d2 : - cmp_func(d1 , d2)
    else :inner_cmp_func = cmp_func
    sorted_data = data[:]
    for i in range(len(sorted_data)) :
        right_idx = i # means the actually element position in the i-th position
        for j in range(i+1 , len(sorted_data)) :
            if inner_cmp_func(sorted_data[right_idx] , sorted_data[j]) > 0 :
                right_idx = j
        sorted_data[i] , sorted_data[right_idx] = sorted_data[right_idx] , sorted_data[i]

    return sorted_data

def bubble_sort(data , cmp_func=cmp , reverse=False) :
    '''
    a basic sort method
    like a bubble , alway from bottom up-wards . 
    if  i > i+1 , the swap i , i+1 , then i = i+1 to len -1 - soted_num ; so top part is ordered firstly .
    This is a bit different from select_sort or insert_sort
    data : list
    '''
    if reverse : inner_cmp_func = lambda d1 , d2 : - cmp_func(d1 , d2)
    else : inner_cmp_func = cmp_func
    sorted_data = data[:]
    for ite_nums in range( len(sorted_data) -1 ) :
        for swap_idx in range( 0 , len(sorted_data) -1 - ite_nums) :
            if inner_cmp_func(data[swap_idx] , data[swap_idx+1]) > 0 :
                data[swap_idx] , data[swap_idx+1] = data[swap_idx+1] , data[swap_idx]
    return sorted_data

def generage_cmp_func(sorted_name) :
    assert (sorted_name in GradeName2Idx)
    grade_idx = GradeName2Idx[sorted_name]
    valid_end = len(GradeName2Idx) -1 -1 # remove the '平均分'
    assert( 0 <= grade_idx <= valid_end)
    def cmp_func(tuple_info1 , tuple_info2) :
        '''
        tuple_info* : ('ID' , {'name' , 'grades' , 'rank'})
        '''
        grades1 = tuple_info1[1]['grades']
        grades2 = tuple_info2[1]['grades']
        if grades1[grade_idx] != grades2[grade_idx] :
            return cmp(grades1[grade_idx] , grades2[grade_idx])
        else :
            for idx in range(0 , valid_end + 1) :
                if idx == grade_idx :
                    continue
                if grades1[idx] != grades2[idx] :
                    return cmp(grades1[idx] , grades2[idx])
                else :
                    continue # it is redundent ! but is more clearly ~ 
        return cmp(tuple_info1[1]['name'] , tuple_info2[1]['name2']) # final compare factor
    return cmp_func

def set_rank_value(data) :
    sorted_data = select_sort(data.items() , generage_cmp_func(u'总成绩'))
    rank = 1
    for key , value in sorted_data  :
        data[key]['rank'] = rank
        rank += 1

def print_all_grades_sorted(data , console_encoding='utf8') :
    sorted_data = select_sort(data.items() , generage_cmp_func(u'总成绩'))
    formated_line = u"{rank} {ID} {name} {grade[0]} {grade[1]} {grade[2]} {grade[3]} {grade[4]} {grade[5]} {grade[6]:.1}"
    for key , value in sorted_data :
        ID = key 
        name = value['name']
        rank = value['rank']
        grade = value['grades']
        print formated_line.format(**locals()).encode(console_encoding)

def print_single_grades_sorted(data , subject , console_encoding='utf8') :
    sorted_data = bubble_sort(data.items() , generage_cmp_func(subject))
    formated_line = u'{rank} {ID} {name} {score}'
    rank = 1
    for key , value in sorted_data :
        ID = key 
        name = value['name']
        score = value['grades'][GradeName2Idx[subject]]
        print formated_line.format(**locals()).encoding(console_encoding)
        rank += 1

def binary_search(data , ID) :
    items = data.items()
    items = map(lambda item : (int(item[0]) , item[1]) , items)
    items = sorted(items , key=lambda item : item[0])
    search_id = int(ID)
    low = 0 
    high = len(items) -1 
    while(low <= high) :
        mid = low + ( high - low ) / 2 
        if data[mid][0] == search_id : 
            return data[mid][1]
        elif data[mid][0] < search_id : 
            low = mid + 1
        else : 
            high = mid - 1
    return None

if __name__ == '__main__' :
    cur_stage = stage.STAGE_READ_DATA
    console_encoding = 'utf8'
    candidate_encoding = set(['utf8' , 'gb18030'])
    grades_data = {}
    while True :
        line = sys.stdin.readline().strip()
        try :
            line = line.decode(console_encoding)
        except UnicodeDecodeError , e :
            another_encoding = str(ist(candidate_encoding - set([console_encoding]))[0])
            line = line.decode(another_encoding ) # if Exception again , do not processing it ~ 
            console_encoding = another_encoding
        if line == u"======" :
            if cur_stage == stage.STAGE_READ_DATA :
                cur_stage = stage.STAGE_SINGLE_RANK
                # set rank , print sorted result .
                set_rank_value(grades_data)
                print_all_grades_sorted(grades_data , console_encoding)
            elif cur_stage == stage.STAGE_SINGLE_RANK :
                cur_stage = stage.STAGE_SEARCH_ID
            else :
                break
            continue
        
        if cur_stage == stage.STAGE_READ_DATA :
            add_student_grade_info(grades_data , line)
        elif cur_stage == stage.STAGE_SINGLE_RANK :
            subject = line
            print_single_grades_sorted(grades_data , subject , console_encoding)
        else :
            search_id_line = line
            binary_search(data , search_id_line)
            formated_line = u"{search_id_line} {name} {grade[0]} {grade[1]} {grade[2]} {grade[3]} {grade[4]} {grade[5]} {grade[6]:.1} {rank}"
