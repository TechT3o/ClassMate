from enums import SubjectArea
from statics import interpret_days


class ConstraintBasedFilter:

    def __init__(self, constraints):
        self.dict = {}
        self.school_area, self.units_lower, self.units_upper, self.max_hours = constraints

    def filter_course(self, course_details):
        subject_area = course_details['Subject area']
        schedule = course_details['Schedule']

        days = interpret_days(schedule[0])
        if None in days:
            hours = schedule[2] - schedule[1]
        else:
            hours = (schedule[2] - schedule[1]) * 2
        units = int(course_details['Units'][0])

        if ((self.school_area == SubjectArea(subject_area)) or (self.school_area == SubjectArea.ANY)) and\
                (self.units_lower <= units <= self.units_upper) and (hours <= self.max_hours):
            return True
        else:
            return False
