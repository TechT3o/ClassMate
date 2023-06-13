"""
Script that enriches the course_data.json database by adding random hours as the class schedule and
 assigns a random rgb color in each class
"""

from statics import load_dict_from_json, save_dict_to_json
import random as rng
from typing import Tuple


def generate_random_schedule() -> Tuple[str, int, int]:
    """
    Generates a random time schedule for the class
    :return: None
    """

    # possible lecture days
    days = ["MW", "TT", "WF", "Mo", "Tu", "We", "Th", "Fr"]

    # selects random, hours, duration and days
    hours = list(range(1, 8))
    duration = rng.randint(1, 3)
    start_hour = rng.choice(hours)
    day = rng.choice(days)
    finish_hour = start_hour + duration

    return (day, start_hour, finish_hour)

FILE_NAME = 'course_data.json'
course_dict = load_dict_from_json(FILE_NAME)

for course in list(course_dict.keys()):
    schedule = generate_random_schedule()
    rgb_color = (rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255))
    course_dict[course]['Schedule'] = schedule
    course_dict[course]['Color'] = rgb_color

save_dict_to_json(course_dict, 'enriched_course_data.json')
