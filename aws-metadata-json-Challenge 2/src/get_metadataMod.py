import requests
import json

metadata_url = 'http://169.254.169.254/latest/'

"""
This function will traverse to the root of the end-point and get the data.
Once the data is obtained it will construct the dictionary which captures the path as well the metadata obtained for that path.
Usually the output of 'http://169.254.169.254/latest/meta-data' is following:
ami-id
ami-launch-index
ami-manifest-path
block-device-mapping/
events/
...
So this function will construct the URL, call the url and fetch the metadata for direct end-points.
'http://169.254.169.254/latest/meta-data/ami-id'
But for the URL which contain deeper layer of end-point, this function will identify it and traverse deeper into tree and construct the data structure.
'http://169.254.169.254/latest/meta-data/block-device-mappping/'
ami
root
"""
def traverse_tree(url, data_path):
    # Initializing an empty dictionary.
    metadata = {}
    # The path obtained by previous calls. For the first time the value will be ['meta-data'].
    # We will loop all the paths obtained by calling the url.
    for path in data_path:
        # The new url path is constructed by appending the path to older url.
        # For example we got 'http://169.254.169.254/latest/meta-data' in first call. When the recursive call is made to this function then the URL will be 'http://169.254.169.254/latest/meta-data and the path will be ami-id. Now the new_url would be 'http://169.254.169.254/latest/meta-data/ami-id
        new_url = url + path
        # Calling the url
        req = requests.get(new_url)
        # Getting the response out of the request.
        resp = req.text
        # If the obtained path ends with / then that means the end-point can go more deeper level and data can be extracted.
        # For example block-device-mapping/ we know we need to go one more level deeper as it may contain more data.
        if path.endswith("/"):
            # To create an array out of obtained values. 'http://169.254.169.254/latest/meta-data/block-device-mappping/' will give ['ami','root'].
            list_of_values = resp.splitlines()
            # Use recursion to go one more level deeper and construct the metadata.
            # For example in 'http://169.254.169.254/latest/meta-data/block-device-mappping/' will give:
            """
            "block-device-mapping": {
                "ami": "/dev/sda1",
                "root": "/dev/sda1"
            }, 
            """
            metadata[path[:-1]] = traverse_tree(new_url, list_of_values)
        else:
            # If the response contains a json output then that will be converted to python data structure and used.
            # Else the response will be used as it is.
            try:
                metadata[path] = json.loads(resp)
            except ValueError:
                metadata[path] = resp
    return metadata


"""
This function will call traverse_tree with initial URL to get the meta-data captured as python dictionary.
"""
def get_metadata()
    # Initial URL to fetch the meta-data will be 'http://169.254.169.254/latest/meta-data'
    initial = ["meta-data/"]
    # Function call to construct the meta-data.
    result = traverse_tree(metadata_url, initial)
    return result


"""
This function will get_metadata function and convert the python dictionary to a json output.
"""
def get_metadata_json():
    metadata = get_metadata()
    metadata_json = json.dumps(metadata, indent=4, sort_keys=True)
    return metadata_json

if __name__ == '__main__':
    print(get_metadata_json())
