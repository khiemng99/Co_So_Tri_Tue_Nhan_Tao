# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:29:24 2019

@author: ngtrk
"""


from KnowledgeBase import KnowledgeBase
from PL_Resolution import PL_Resolution
from File_process import read_file

def main():
    a = read_file("input.txt")
    if a==0:
        return
    else:
        KB, alpha = a
    f = open("output.txt", "w")
#    input = ["-A OR B", "B OR -C", "A OR -B OR C", "-B"]
#    alpha = "-A"
    
#    KB = KnowledgeBase()
#    KB.add_all_sentences(input)

    
    PL = PL_Resolution()
    check = PL.pl_resolution(KB, alpha, f)
    if check == True:
        print("YES")
        f.write("YES")
    else:
        print("NO")
        f.write("NO")
    f.close()

if __name__ == '__main__':
    main()