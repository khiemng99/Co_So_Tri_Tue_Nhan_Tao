# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 21:19:09 2019

@author: ngtrk
"""


#from KnowledgeBase import add_sentence
from File_process import write_file


class PL_Resolution:
    def __init__(self):
        pass
        
        
    def pl_resolution(self, KB, alpha, f):
        self._create_resolution_sentence(KB, alpha)
        clauses = KB.sentences
        clauses_new = clauses
        
        while True:
            new = []
            check = 0
            for ci in clauses_new:
                for cj in clauses:
                    if equal(ci, cj) == 0:
                        resolvent = self._pl_solve(ci, cj)
                        if len(resolvent) != 0:
                            if _contain_empty(resolvent) == 1:
                                check = 1
                            new = union(new, [resolvent])
                            
            clauses_new = diff(clauses, new)
            write_file(f, clauses_new)
            if check==1:
                return True
            
            #if sub_list(new, clauses) == True:
            if len(clauses_new)==0:
                return False
            clauses = union(clauses, new)
    
    def _create_resolution_sentence(self, KB, alpha):
        """
        Add negative of alpha in to KB
        """
        temp = alpha
        if "-" in temp:
            temp = temp.replace("-", "")
        else:
            temp = "-" + temp
        KB.add_sentence(temp)
    
    def _pl_solve(self, ci, cj):
        rt = []
        check = 0
#        idx1 = 0
#        idx2 = 0
        lst1 = ci.copy()
        lst2 = cj.copy()
        len1 = len(lst1)
        len2 = len(lst2)
        for i in range(len1):
            for j in range(len2):
                if ((lst1[i] in lst2[j]) or (lst2[j] in lst1[i])) and lst1[i] != lst2[j]:
                    check+=1
                    if check>1:
                        return rt
                    idx1 = i
                    idx2 = j
                    break
        if check==1:
            del lst1[idx1]
            del lst2[idx2]
            rt = add_sentence(lst1, lst2)
            if len(rt)==0:
                rt.append("{}")
        del lst1
        del lst2
        return rt
    
def _contain_empty(l):
    for ele in l:
        if ele == "{}":
            return 1
    return 0
def sub_list(lst1, lst2):
    """
    return lst1 is sublist(lst2)
    """
    if (len(lst1)!=0 and len(lst2)!=0):
        for ele1 in lst1:
            for ele2 in lst2:
                if equal(ele1, ele2)==0:
                    return False
    return True
def union(lst1, lst2):
    """
    union of two lists
    """
    for ele in lst2:
        if not_in(ele, lst1):
            lst1.append(ele)
    return lst1

def equal(ci, cj):
    if len(ci)==len(cj):
        for ele in ci:
            if not (ele in cj):
                return 0
        return 1
    return 0
def not_in(ele, lst):
    for ele1 in lst:
        if equal(ele, ele1):
            return 0
    return 1

def add_sentence(c1, c2):
    rt=c1
    for ele in c2:
        if not ele in c1:
            rt.append(ele)
    return rt

def diff(lst1, lst2):
    lst=[]
    for ele in lst2:
        if not_in(ele, lst1):
            lst.append(ele)
    return lst