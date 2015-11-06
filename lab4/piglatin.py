#coding=utf-8

VOWELS = ('a' , 'e' , 'i' , 'o' , 'u')

def piglatinfy(s) :
    s = s.lower() 
    processed_s_list = []
    s_list = s.split()
    for word in s_list :
        # starts with vowel(元音)
        if word[0] in VOWELS :
            processed_word = word + 'hay' 
            processed_s_list.append(processed_word)
        # starts with 'qu'
        elif word.startswith('qu') :
            processed_word = ''.join( [word[2:] , word[0:2] , 'ay'] )
            processed_s_list.append(processed_word)
        # starts with other conditions .
        #~ we will find a vowel & 'y' at the first place in the str . and move the part(from the begin to the place)
        #~ to the end , the add a 'ay' . if no vowel or y is found , no move . 
        else :
            vowelplace = -1
            for i in range(1,len(word)) : # search from the 2rh char
                cur_char = word[i]
                if cur_char in VOWELS or cur_char == 'y' :
                    vowelplace = i
                    break
            if vowelplace != -1 :
                word = word[vowelplace:] + word[:vowelplace]
            processed_word = word + 'ay'
            processed_s_list.append(processed_word)
    return ' '.join(processed_s_list)

if __name__ == "__main__" :
    input_str = raw_input()
    piglatin_str = piglatinfy(input_str)
    print piglatin_str

