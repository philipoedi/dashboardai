""" tests in pytest for the api module """


from dashboardai.api import check_string_in_list


def test_check_string_in_list():
    """test the check_string_in_list function"""
    # create a list of strings
    list_of_strings = ["string1", "string2"]
    # check if any of the strings in the list are contained in the string, case insensitive
    assert check_string_in_list("STRING1", list_of_strings) == True
    assert check_string_in_list("STRING3", list_of_strings) == False
    assert check_string_in_list("STRING1", []) == False
    assert check_string_in_list("", list_of_strings) == False
