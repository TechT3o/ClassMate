from keybert import KeyBERT
import time
import json
import streamlit as st
import yake
from heapq import nlargest
import tkinter as tk
from tkinter import simpledialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from gui.class_widget import ClassBox
from typing import List

class TextFilter:

    def __init__(self):
        self.kw_extractor = yake.KeywordExtractor()
        self.keywords = []

        self.scores = []
        
    def extract_keywords(self, doc):
        self.keywords = kw_extractor.extract_keywords(doc)
    
    def rank_classes(course: ClassBox):
        

        # Include something that loads the course dictionary

        # course_data_dict = ... (class dictionary)
    	
        details = course.class_details
        score = 0
        description = details['Description']
        units = details['Units']
        full_text = description +  " " + units

        for word in keywords:
            keyWord = word[0]
            
            if keyWord in full_text:
                score+=1

        if score > 0:
            relevant_classes.append(course)
            course.match_percent(str(score))

            return True
        else:
            return False
                              

        scored_classes = dict(zip(relevant_classes,scores))
        ranked_classes = nlargest(N, scored_classes, key=scored_classes.get)
        print("Recommended classes = " + str(ranked_classes) + "\n")


doc = """
         I want to have a 4 units classes from the Electrical and Computer Engineering department and computer science department with 2 classes on Monday and Wednesday and 1 class on Tuesdays and Thursdays. I have great interest in artificial intelligence and programming. I like to desing filters as well and play with analog signals. Another thing I want to do is work with neural networks and machine learning
    """


# Trying with streamlit

kw_extractor = yake.KeywordExtractor()
keywords = kw_extractor.extract_keywords(doc)
print("The keywords are the following: " + str(keywords))
print("\n")

"""

Fine tuning


kw_model = KeyBERT()

for i in [0.3, 0.5, 0.9]:
    keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 1), stop_words=["class","classes","plan","unit","department","and","have", "great", "with"],
                                use_maxsum=True, diversity=i, nr_candidates=20, top_n=8)
    print(keywords)

"""



#keys = course_data_dict.keys()
relevant_classes = []
scores = []
print(str(len(course_data_dict)) + " Total Classes")

for i in course_data_dict:
    score = 0
    for word in keywords:
        keyWord = word[0]
        description = course_data_dict[i]['Description']
        #department = course_data_dict[i]['Department']
        units = course_data_dict[i]['Units']

        #full_text = description + " " + department + " " + units
        full_text = description +  " " + units


        if keyWord in full_text:
            score+=1
    if score >0:
        relevant_classes.append(i)
        scores.append(score)

scored_classes = dict(zip(relevant_classes,scores))

print("\n")
print("The relevant classes are the following: \n")
print(scored_classes)
print("\n")
print("Number of classes = " + str(len(relevant_classes))+ "\n")
            
           
N=10
ranked_classes = nlargest(N, scored_classes, key=scored_classes.get)
print("Recommended classes = " + str(ranked_classes) + "\n")