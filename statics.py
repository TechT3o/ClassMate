import json
import pickle
from typing import List, Tuple
from torch import Tensor


def save_dict_to_json(data: dict, filename: str):
    """
    Save dictionary in json file
    :param data: dictionary to save
    :param filename: filename to save (must end with .json)
    :return: None
    """
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


def load_dict_from_json(filename: str) -> dict:
    """
    Loads dictionary from .json file
    :param filename: filename to load dict from
    :return: dictionary saved in .json
    """
    with open(filename) as json_file:
        data = json.load(json_file)
        return data


def load_pickle_embeddings() -> Tuple[List[str], Tensor]:
    """
    Loads pickled course description embeddings from the embeddings.pkl file
    :return:
    """
    with open('embeddings.pkl', "rb") as fIn:
        stored_data = pickle.load(fIn)
        stored_sentences = stored_data['sentences']
        stored_embeddings = stored_data['embeddings']
        return stored_sentences, stored_embeddings


def interpret_days(days):

    if days == "MW":
        return 0, 2

    if days == "TT":
        return 1, 3

    if days == "WF":
        return 2, 4

    if days == "Mo":
        return 0, None

    if days == "Tu":
        return 1, None

    if days == "We":
        return 2, None

    if days == "Th":
        return 3, None

    if days == "Fr":
        return 4, None
