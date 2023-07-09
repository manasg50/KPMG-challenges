import requests
import json

metadata_url = 'http://169.254.169.254/latest/'


def traverse_tree(url: str, data_path: list) -> dict:
    """
    param url:
    param data_path: List of the end-points
    return metadata: meta-deta dictionary populated by the function.
    This function will traverse to the root of the end-point and get the data.
    Once the data is obtained it will construct the dictionary which captures the path as well the metadata obtained for that path.
    """
    # Initializing an empty dictionary.
    metadata = {}
    for path in data_path:
        # The new url path is constructed by appending the path to older url.
        new_url = url + path
        # Calling the url
        req = requests.get(new_url)
        # Getting the response out of the request.
        resp = req.text
        # If the obtained path ends with / then that means the end-point can go deeper level and data can be
        # extracted.
        if path.endswith("/"):
            list_of_values = resp.splitlines()
            # Use recursion to go one more level deeper and construct the metadata.
            metadata[path[:-1]] = traverse_tree(new_url, list_of_values)
        else:
            # If the response contains a json output then that will be converted to python data structure and used.
            # Else the response will be used as it is.
            try:
                metadata[path] = json.loads(resp)
            except ValueError:
                metadata[path] = resp
    return metadata


def fetch_key_value(metadata: dict, search_key: str) -> object:
    """
    param metadata: Meta-data captured by traverse_tree function to extract search_key out of it.
    param search_key: Key needs to be searched. Please provide the complete hierarchy.
    return: The value of the search_key will be returned if found else Error string will be returned.
    This function will search the key provided by the user and return the value for it.
    """
    value = metadata
    key_arr = search_key.split("/")
    for index, item in enumerate(key_arr):
        try:
            value = value[item]
        except KeyError:
            value = f"Error! key: {item} not found in {index + 1} hierarchy in the nested object: {metadata}", index + 1
            break
        except TypeError:
            if not isinstance(value, dict):
                value = f"Error! The level {index + 1} is exhausted for {metadata} for key: {item}"
    return value


def get_metadata():
    """
    return The dictionary obtained from traverse_tree function.
    This function will call traverse_tree with initial URL to get the meta-data captured as python dictionary.
    """
    # Initial URL to fetch the meta-data will be 'http://169.254.169.254/latest/meta-data'
    initial = ["meta-data/"]
    # Function call to construct the meta-data.
    result = traverse_tree(metadata_url, initial)
    return result


def get_metadata_json(search_key: str = None) -> object:
    """
    param key: The key needs to be searched.
    return: The json formatted meta-data.
    This function will get_metadata function and convert the python dictionary to a json output.
    If the search_key is provided then the value for key is fetched else whole meta-data is returned.
    """
    metadata = get_metadata()
    if search_key:
        metadata = fetch_key_value(metadata, search_key)
    metadata_json = json.dumps(metadata, indent=4, sort_keys=True)
    return metadata_json


if __name__ == '__main__':
    key = "meta-data/block-device-mapping"
    key1 = "meta-data/network/interfaces/macs"
    key2 = "meta-data/system"
    print(get_metadata_json())
    print(get_metadata_json(key))
    print(get_metadata_json(key1))
    print(get_metadata_json(key2))