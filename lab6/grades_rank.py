#coding=utf8

GradeIdx2Name = ( u'语文' , u'数学' , u'英语',u'物理' , u'化学' , u'总成绩' , '平均分')
GradeName2Idx = { name:idx for idx , name in enumerate(GradeIdx2Name) }

def add_student_grade_info(grade_info , grade_info_str) :
    '''
    parse the grade_info_str , add the info to the grade_info struct
    '''

