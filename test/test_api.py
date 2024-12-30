""" tests in pytest for the api module """


from dashboardai.api import (
    check_string_in_list,
    create_table_definition_prompt,
    handle_response_graph,
    remove_semicolons_in_brackets,
    single_semicolon,
)


def test_check_string_in_list():
    """test the check_string_in_list function"""
    # create a list of strings
    list_of_strings = ["string1", "string2"]
    # check if any of the strings in the list are contained in the string, case insensitive
    assert check_string_in_list("STRING1", list_of_strings) == True
    assert check_string_in_list("STRING3", list_of_strings) == False
    assert check_string_in_list("STRING1", []) == False
    assert check_string_in_list("", list_of_strings) == False


def test_create_table_definition_prompt():
    """test the create_table_definition_prompt function"""
    # create a schema
    schema = {
        "table1": [
            {"name": "col1", "type": "INTEGER"},
            {"name": "col2", "type": "TEXT"},
        ],
        "table2": [
            {"name": "col1", "type": "INTEGER"},
            {"name": "col2", "type": "TEXT"},
        ],
    }
    # create the prompt
    prompt = create_table_definition_prompt(schema)
    # check if the prompt is correct
    assert (
        prompt
        == "### sqlite database, with its properties: \n# table1(col1,col2) \n# table2(col1,col2) \n"
    )


""" test in pytest for handle_response_graph function """


def test_handle_response_graph():
    """test the handle_response_graph function"""
    # create a response
    response = {
        "choices": [
            {
                "text": "fig.add_trace(go.Scatter(x=data['debt'], y=data['income'], mode='markers'))\nfig.show()\n\n"
            }
        ]
    }
    response_handled = handle_response_graph(response)
    assert (
        response_handled
        == "fig.add_trace(go.Scatter(x=data['debt'], y=data['income'], mode='markers'))"
    )


def remove_semicolons_in_brackets():
    """test the remove_semicolons_in_brackets function"""
    # create a string
    input_str = "(;, ,, ;);(;;;;)"
    # remove semicolons in brackets
    output_str = remove_semicolons_in_brackets(input_str)
    # check if the output is correct
    assert output_str == "(, ,, );()"


def test_single_semicolon():
    """test the single_semicolon function"""
    # create a string
    input_str = ";;;;"
    # remove semicolons in brackets
    output_str = single_semicolon(input_str)
    # check if the output is correct
    assert output_str == ""
    input_str = ";;  ;  ;"
    output_str = single_semicolon(input_str)
    assert output_str == ""
    input_str = "c;;b; ; a"
    output_str = single_semicolon(input_str)
    assert output_str == "c;b;a"
