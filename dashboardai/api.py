def check_string_in_list(string, list_of_strings):
    """
    This function takes a string and a list of strings, checks if any string of the list is contained in the string, case insensitive.
    :param string: string to check
    :param list_of_strings: list of strings to check
    :return: boolean
    """
    # use the string.lower() method to check if any of the strings in the list are contained in the string, case insensitive
    return any(item.lower() in string.lower() for item in list_of_strings)
