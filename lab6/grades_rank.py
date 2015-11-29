#coding=utf8

GradeIdx2Name = ( u'语文' , u'数学' , u'英语',u'物理' , u'化学' , u'总成绩' , '平均分')
GradeName2Idx = { name:idx for idx , name in enumerate(GradeIdx2Name) }

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
    '''
    if reverse : cmp_func = lambda d1,d2 : - cmp_func(d1 , d2)
    sorted_data = data[:]
    for i in range(len(sorted_data)) :
        right_idx = i # means the actually element position in the i-th position
        for j in range(i+1 , len(sorted_data)) :
            if cmp_func(sorted_data[right_idx] , sorted_data[j]) > 0 :
                right_idx = j
        sorted_data[i] , sorted_data[right_idx] = sorted_data[right_idx] , sorted_data[i]

    return sorted_data

def bubble_sort(data , cmp_func=cmp , reverse=False) :
    '''
    a basic sort method
    like a bubble , alway from bottom up-wards . 
    if  i > i+1 , the swap i , i+1 , then i = i+1 to len -1 - soted_num ; so top part is ordered firstly .
    This is a bit different from select_sort or insert_sort
    '''
    if reverse : cmp_func = labmda d1 , d2 : - cmp_func(d1 , d2)
    sorted_data = data[:]
    for ite_nums in range( len(sorted_data) -1 ) :
        for swap_idx in range( 0 , len(sorted_data) -1 - ite_nums) :
            if cmp_func(data[swap_idx] , data[swap_idx+1]) > 0 :
                data[swap_idx] , data[swap_idx+1] = data[swap_idx+1] , data[swap_idx]
    return sorted_data





