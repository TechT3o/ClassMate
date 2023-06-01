from sentence_transformers import SentenceTransformer
from statics import load_dict_from_json, save_dict_to_json

"""
This is a simple application for sentence embeddings: semantic search

We have a corpus with various sentences. Then, for a given query sentence,
we want to find the most similar sentence in this corpus.

This script outputs for various queries the top 5 most similar sentences in the corpus.
"""
from sentence_transformers import SentenceTransformer, util
import torch

embedder = SentenceTransformer('all-MiniLM-L6-v2')

FILE_NAME = 'course_data.json'
course_dict = load_dict_from_json(FILE_NAME)

description_list = [course_dict[course]["Description"] for course in list(course_dict.keys())] 

corpus_embeddings = embedder.encode(description_list, convert_to_tensor=True)

query = 'I would like to have a class on digital filter design and FIR filters'


top_k = min(5, len(description_list))

query_embedding = embedder.encode(query, convert_to_tensor=True)

# We use cosine-similarity and torch.topk to find the highest 5 scores
cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
top_results = torch.topk(cos_scores, k=top_k)

print("\n\n======================\n\n")
print("Query:", query)
print("\nTop 5 most similar sentences in corpus:")

print("")

for score, idx in zip(top_results[0], top_results[1]):
    print(list(course_dict.keys())[idx], "(Score: {:.4f})".format(score),description_list[idx])


for idx,key in enumerate(list(course_dict.keys())):
    course_dict[key]["Corpus Embeddings"] = corpus_embeddings[idx]

print(course_dict)


#save_dict_to_json(course_dict, 'enriched_course_data.json')