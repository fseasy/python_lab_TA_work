#coding=utf-8
import re

VOWELS = ('a' , 'e' , 'i' , 'o' , 'u')
pattern_vowels_start = re.compile(r'[aeiou]')
def piglatinfy(s) :
    s = s.lower() 
    processed_s_list = []
    #s_list = s.split()
    s_list = re.split( r'\s' , s)
    for word in s_list :
        # starts with vowel(元音)
        #if word[0] in VOWELS :
        if pattern_vowels_start.match(word) :
            processed_word = word + 'hay' 
            processed_s_list.append(processed_word)
        # starts with 'qu'
        #elif word.startswith('qu') :
        elif re.match(r'^qu' , word) : 
            processed_word = ''.join( [word[2:] , word[0:2] , 'ay'] )
            processed_s_list.append(processed_word)
        # starts with other conditions .
        #~ we will find a vowel & 'y' at the first place in the str . and move the part(from the begin to the place)
        #~ to the end , the add a 'ay' . if no vowel or y is found , no move . 
        else :
            vowel_search_rst = re.search(r'\w+?([aeiouy])' , word)
            if vowel_search_rst != None :
                vowelplace = vowel_search_rst.start(1) # 0 is the total str , 1 the matched `aeiou` vowel 
                word = word[vowelplace:] + word[:vowelplace]
            processed_word = word + 'ay'
            processed_s_list.append(processed_word)
    return ' '.join(processed_s_list)

if __name__ == "__main__" :
    input_str = raw_input()
    piglatin_str = piglatinfy(input_str)
    print piglatin_str

