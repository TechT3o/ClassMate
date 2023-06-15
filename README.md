# ClassMate

ClassMate is a student-designed AI assistant that makes it effortless and swift for students to create a personalized class schedule.
It provides an easy to use User Interface where courses can be filtered using constraints such as (subject area, number of units, number of hours per week) and the resulting classes are displayed, they can be added to a calendar and the class web page can be loaded. The user can also write a text prompt describing what kind of course they would like to take and the similarity between the text prompt and the course description is displayed and the courses are sorted. The code that creates the app is found in the [main_gui.py](https://github.com/TechT3o/ClassMate/blob/main/gui/main_gui.py).

Starting and filtering page: ![Screenshot (20)](https://github.com/TechT3o/ClassMate/assets/87833804/d4046d58-6bc4-43a8-93f9-05fd8d4214f4)

Main Page: ![Screenshot (22)](https://github.com/TechT3o/ClassMate/assets/87833804/ccbddc29-7294-4023-9da2-a857b82a0d95)

## Features

### Class widgets

Custom made class widgets that have a dictionary that includes all class details such as number of units, subject area, class webpage URL, schedule etc. The widget has a plus and a minus icon that allows class to be added/removed to/from calendar when clicked, it's body is a button that loads the class webpage and a label that can display the similarity score between the user prompt and the course descriptions. The code can be found in [class_widget.py](https://github.com/TechT3o/ClassMate/blob/main/gui/class_widget.py).

### Constraint Based Filtering

Constraint based filtering is the first filtering stage where the user inputs some constraints such as (subject area, number of units, number of hours per week) and the courses are filtered based on if they meet these constraints. The code for the filtering window UI is found in the [filtering_window.py](https://github.com/TechT3o/ClassMate/blob/main/gui/filtering_window.py) and the constraint based filter class is found in [constraint_filtering.py](https://github.com/TechT3o/ClassMate/blob/main/constraint_filtering.py).

### Easy Class Calendar Add / Remove

By clicking on the plus and minus icons on the classbox widgets you can add / remove a class to / from the calendar. The calendar is a custom widget and it's code is in [calendar_widget.py](https://github.com/TechT3o/ClassMate/blob/main/gui/calendar_widget.py). It includes functions for the visualization of the calendar as well as for adding/ removing classes.

### Webview to see course webpage

The course detail web pages can be shown on the main page by loading the course URL to the webview widget.

### User text input search

For the user text input the [text_filter.py](https://github.com/TechT3o/ClassMate/blob/main/text_filter.py) was created where a sentence transformer is used to embed the text input and then the cosine similarity between these embeddings and a corpus of embeddings of the course names and descriptions (created in [course_description_embedder_script.py](https://github.com/TechT3o/ClassMate/blob/main/course_description_embedder_script.py) determines how similar each course is to the text input.

## Installation

For the installation do pip install of the requirements.txt that includes the necessary packages to run the code. In addition you will have to do pip install PyQtWebEngine, Sentence Transformers.

## Helping scripts

Some scripts that help create the course database:

### Course list webscrapping

The [webscraping](https://github.com/TechT3o/ClassMate/blob/main/webscraping.py) script is used to load the ucla course registrar catalog, searches for the electrical and computer engineering courses, scrapes course names and course details, creates a dictionary and stores it in a .json file.

### Course detail enrichment

This [course detail enrichment](https://github.com/TechT3o/ClassMate/blob/main/course_detail_enrichment_script.py) script enriches the course details by giving a random color that is used for color labelling the course (in the final demo this was overwritten to make color labels bluish and with contrast to the black text) and a schedule time, date when the course is taught. This info that is not available in the course catalog is then stored in an enriched .json file.
