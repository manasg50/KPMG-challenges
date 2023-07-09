def fetch_key_value(nested_object: dict, search_key: str) -> object:
    """
    param nested_object: The nested_object where the value need to be fetched for the search_key.
    param search_key: The search_key which needs to be searched in nested_object. Please provide the complete hierarchy
    split using "/".
    return: The value fetched for the search_key from the nested_object.
    This function will search the key provided by the user and return the value for it.
    """
    value = nested_object
    key_arr = search_key.split("/")
    for index, item in enumerate(key_arr):
        try:
            value = value[item]
        except KeyError:
            value = f"Error! key: {item} not found in {index + 1} hierarchy in the nested object: {nested_object}"
            break
        except TypeError:
            if not isinstance(value, dict):
                value = f"Error! The level {index + 1} is exhausted for {nested_object} for key: {item}"
    return value


if __name__ == "__main__":
    print(fetch_key_value({"a": {"b": {"c": "d"}}}, "a/b/c"))
    print(fetch_key_value({"x": {"y": {"z": "a"}}}, "x/y/z"))
    print(fetch_key_value({"a": {"b": {"c": "d"}}}, "a/x/c"))
    print(fetch_key_value({"a": {"b": {"c": "d"}}}, "a/b/x"))
    print(fetch_key_value({"a": {"b": {"c": "d"}}}, "a/b/c/d"))
    print(fetch_key_value({"a": {"b": {"x": 1, "c": "d"}}}, "a/b/c"))
    print(fetch_key_value({"a": {"b": {"x": 1, "c": "d"}}}, "a/b"))
    print(fetch_key_value({"a": {"b": {"x": 1, "c": "d"}}}, "a/b/x"))