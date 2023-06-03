from statics import load_pickle_embeddings
from sentence_transformers import SentenceTransformer, util


class TextFilter:
    """
    Class that filters/ ranks the classes based on text input
    """
    def __init__(self):
        self.keywords = []
        self.scores = []
        self.sentences, self.embeddings = load_pickle_embeddings()
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def generate_scores(self, query: str) -> None:
        """
        Generates scores from given prompt based on cosine similarity to course description embeddings
        :param query: user input query
        :return: None
        """
        # Creates vector of query
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        self.scores = util.cos_sim(query_embedding, self.embeddings)[0]
