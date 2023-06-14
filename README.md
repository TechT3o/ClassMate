# ClassMate

ClassMate is a student-designed AI assistant that makes it effortless and swift for students to create a personalized class schedule.
It provides an easy to use User Interface where courses can be filtered using constraints such as (subject area, number of units, number of hours per week) and the resulting classes are displayed, they can be added to a calendar and the class web page can be loaded. The user can also write a text prompt describing what kind of course they would like to take and the similarity between the text prompt and the course description is displayed and the courses are sorted.

Starting and filtering page: ![Screenshot (20)](https://github.com/TechT3o/ClassMate/assets/87833804/d4046d58-6bc4-43a8-93f9-05fd8d4214f4)

Main Page: ![Screenshot (22)](https://github.com/TechT3o/ClassMate/assets/87833804/ccbddc29-7294-4023-9da2-a857b82a0d95)

## Features

### Constraint Based Filtering

Constraint based filtering is the first filtering stage where the user inputs some constraints such as (subject area, number of units, number of hours per week) and the courses are filtered based on if they meet these constraints. The code for the filtering window UI is found in the ![filtering_window.py](https://github.com/TechT3o/ClassMate/blob/main/gui/filtering_window.py) and the constraint based filter class is found in ![constraint_filtering.py](https://github.com/TechT3o/ClassMate/blob/main/constraint_filtering.py)

### Easy Class Calendar Add / Remove

By clicking on the plus and minus icons on the classbox widgets you can add / remove a class to / from the calendar. The calendar is a custom widget and it's code is in ![calendar_widget.py](https://github.com/TechT3o/ClassMate/blob/main/gui/calendar_widget.py). It includes functions for the visualization of the calendar as well as for adding/ removing classes.

### Webview to see course webpage

The course detail web pages can be shown on the main page by loading the course URL to the webview widget.

### User text input search

For the user text input the ![text_filter.py](https://github.com/TechT3o/ClassMate/blob/main/text_filter.py) was created where a sentence transformer is used to embed the text input and then the cosine similarity between these embeddings and a corpus of embeddings of the course names and descriptions (created in ![course_description_embedder_script.py](https://github.com/TechT3o/ClassMate/blob/main/course_description_embedder_script.py) determines how similar each course is to the text input.

## Installation

## Helping scripts

### Course list webscrapping

### Course detail enrichment

### Course details embeddings
