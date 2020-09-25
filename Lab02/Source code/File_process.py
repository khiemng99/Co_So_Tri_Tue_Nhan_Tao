# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 17:11:17 2019

@author: ngtrk
"""
from KnowledgeBase import KnowledgeBase

def read_file(file):
    """
    Read KB and alpha from input file.
    Return KB and alpha (in tuple) if success, else 0
    param:
        file(str) : name of file
        KB: KnowledgeBase()
        alpha: str
    """
    try:
        f = open(file, "r")
    except IOError:
        print("Could not open file!!!")
        return 0
    with f:
        alpha = f.readline().replace("\n", "")
        KB = KnowledgeBase()
        lenKB = int(f.readline())
        for i in range(lenKB):
            KB.add_sentence(f.readline().replace("\n",""))
        f.close()
        return KB, alpha

def write_file(f, lst):
    """
    Write sentences in lst to output file
    Return none
    pram:
        file: str
        lst: list
    """
#    try:
#        f = open(file, "a")
#    except IOError:
#        print("Could not open file!!!")
#    with f:
    f.write(str(len(lst)))
    for i in lst:
        f.write("\n" + " OR ".join(i))
    f.write("\n")
        