# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 20:10:06 2019

@author: ngtrk
"""

#from Sentences import *

class KnowledgeBase:
    """
    Knowledge base that stores information in propositional logic
    """
    def __init__(self):
        self.sentences = []
    
    def add_sentence(self, str):
        """
        Add new statement to KB
        sen: Sentences
        """
        sentence = str.split(' OR ')
        self.sentences.append(sentence)
    
    def add_all_sentences(self, strs):
        """
        Add several statements to KB
        sens: a set of Sentences
        """
        for str in strs:
            self.add_sentence(str)
    
    def size(self):
        return len(self.sentences)
    