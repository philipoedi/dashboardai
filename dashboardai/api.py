import openai


def check_string_in_list(string, list_of_strings):
    """
    This function takes a string and a list of strings, checks if any string of the list is contained in the string, case insensitive.
    :param string: string to check
    :param list_of_strings: list of strings to check
    :return: boolean
    """
    # use the string.lower() method to check if any of the strings in the list are contained in the string, case insensitive
    return any(item.lower() in string.lower() for item in list_of_strings)


def create_table_definition_prompt(schema):
    """This function creates a prompt for the OpenAI API to generate SQL queries.

    Args:
        df (dataframe): pd.DataFrame object to automtically extract the table columns
        table_name (string): Name of the table within the database

        Returns: string containing the prompt for OpenAI
    """

    prompt = "### sqlite database, with its properties: \n"
    for table_name, columns in schema.items():
        prompt += "# {}({}) \n".format(
            table_name, ",".join([c["name"] for c in columns])
        )
    return prompt


def combine_prompts(fixed_sql_prompt, user_query):
    """Combine the fixed SQL prompt with the user query.

    Args:
        fixed_sql_prompt (string): Fixed SQL prompt
        user_query (string): User query

    Returns:
        string: Combined prompt
    """
    final_user_input = f"### A query to answer: {user_query}\nSELECT"
    return fixed_sql_prompt + final_user_input


def send_to_openai(prompt, stop, max_tokens=500):
    """Send the prompt to OpenAI

    Args:
        prompt (string): Prompt to send to OpenAI

    Returns:
        string: Response from OpenAI
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=stop,
    )
    return response


def handle_response(response):
    """Handles the response from OpenAI.

    Args:
        response (openAi response): Response json from OpenAI

    Returns:
        string: Proposed SQL query
    """
    query = response["choices"][0]["text"]
    if query.startswith(" "):
        query = "Select" + query
    return query


""" A function that takes a dataframe and returns the name of the columns as a single string separated by commas. """


def get_column_names(df):
    return ",".join(df.columns)


def create_dataframe_definition_prompt(df):
    """This function creates a prompt for the OpenAI API to generate SQL queries.

    Args:
        df (dataframe): pd.DataFrame object to automtically extract the table columns
        table_name (string): Name of the table within the database

        Returns: string containing the prompt for OpenAI
    """
    prompt = "### the variable data that is a pandas dataframe, with properties: \n"
    prompt += "# {} \n".format(get_column_names(df))
    return prompt


def combine_prompts_graph(fixed_prompt, user_query):
    final_user_input = f"### Python code creates a plotly graph with with intuitive labelling and answers: {user_query}\n"
    final_user_input += "import plotly.graph_objs as go\n"
    final_user_input += "fig = go.Figure()\n"
    return fixed_prompt + final_user_input


def remove_semicolons_in_brackets(input_str):
    output_str = ""
    inside_brackets = False
    bracket_count = 0
    for char in input_str:
        if char == "(":
            inside_brackets = True
            bracket_count += 1
        elif char == ")":
            inside_brackets = False
            bracket_count -= 1
        elif inside_brackets and char == ";":
            continue
        output_str += char
    if bracket_count != 0:
        raise ValueError("Unbalanced brackets in input string")
    return output_str


def handle_response_graph(response):
    """Handles the response from OpenAI.
    "fig.add_trace(go.Scatter(x=data['debt'], y=data['income'], mode='markers'))\nfig.show()\n\n"
    "fig.add_trace(go.Scatter(x=data['debt'], y=data['income'], mode='markers', name='Debt vs Income'))\nfig.update_layout(title='Debt vs Income', xaxis_title='Debt', yaxis_title='Income')\nfig.show()\n\n"

    Args:
        response (openAi response): Response json from OpenAI

    Returns:
        string: Proposed SQL query
    """
    query = response["choices"][0]["text"]
    query = query.replace("\n", ";").replace("fig.show()", "").strip(";")
    query = remove_semicolons_in_brackets(query)

    return query


def single_semicolon(input_str):
    """
    makes a sequence of ; to a single ; (there can be whitespace between ;)
    """
    return ";".join(filter(lambda x: x.strip() != "", input_str.split(";")))
