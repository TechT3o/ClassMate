"""
Script that creates embeddings from course descriptions and saves them in pickle file.
"""
from statics import load_dict_from_json
from sentence_transformers import SentenceTransformer
import pickle


# Load dict and get course descriptions
FILE_NAME = 'course_data.json'
course_dict = load_dict_from_json(FILE_NAME)
description_list = [course + '.' + course_dict[course]["Description"] for course in list(course_dict.keys())]

# Create embedder
embedder = SentenceTransformer('all-MiniLM-L6-v2')
corpus_embeddings = embedder.encode(description_list, convert_to_tensor=True)


# Store sentences & embeddings on disc
with open('embeddings.pkl', "wb") as fOut:
    pickle.dump({'sentences': description_list, 'embeddings': corpus_embeddings}, fOut, protocol=pickle.HIGHEST_PROTOCOL)