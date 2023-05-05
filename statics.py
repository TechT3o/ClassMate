import json


def save_dict_to_json(data, filename):
    """
    Save dictionary in json file
    :param data: dictionary to save
    :param filename: filename to save it as
    :return: None
    """
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
