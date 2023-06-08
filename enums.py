import enum


class SubjectArea(enum.Enum):
    """
    Enums of different subject areas, they make the code more readable and string comparisons faster
    """
    ANY = ''
    ECE = "Electrical and Computer Engineering"
    CS = "Computer Science"
    MATH = "Mathematics"


class College(enum.Enum):
    """
        Enums of different colleges, they make the code more readable and string comparisons faster
        """
    SCHOOL_OF_ENGINEERING = "Henry Samueli School of Engineering and Applied Science"
    ANDERSON_BUSINESS_SCHOOL = "Anderson School of Business"
