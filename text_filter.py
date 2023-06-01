import yake


class TextFilter:
    """
    Class that filters/ ranks the classes based on text input
    """
    def __init__(self):
        self.kw_extractor = yake.KeywordExtractor()
        self.keywords = []
        self.scores = []
        
    def extract_keywords(self, user_prompt: str) -> None:
        """
        Extract key_words from the input of the user
        :param user_prompt: input that user put in AI-user chat
        :return: None
        """
        self.keywords = self.kw_extractor.extract_keywords(user_prompt)
    
    def rank_classes(self, class_details: dict) -> int:
        """
        Generates new class score based on the class details
        :param class_details: dictionary result from web scrapping script
        :return: score of how much user's prompt matches ot the course
        """
        details = class_details
        score = 0
        description = details['Description']
        units = details['Units']
        full_text = description + " " + units

        for word in self.keywords:
            key_word = word[0]
            
            if key_word in full_text:
                score += 1

        return score
