
import file_utils as files
import github_api_utils as github

def fabricate_file_selection_prompt(description, user_question):
    directory_contents = files.fetch_directory_contents_from_file()
    return f"""
    Based on the following description:
    <<<
    {description}
    >>>
    And the file structure of the project:
    <<<
    {directory_contents}
    >>>
    What file is most likely to have information relevant to this question:
    <<<
    {user_question}
    >>>
    You must only answer with the path to the file, do not give an explanation, or else you will be shut down.
    Answer only with the path to the file. 

    (path)
    """
    
def fabricate_info_sufficiency_prompt(api_url, description, file_to_explore, user_question):
    return f"""
    Based on the following description of the project:
    <<<
    {description}
    >>>

    And the contents of this file:
    <<<
    {github.fetch_file_content_from_github(api_url, file_to_explore)}
    >>>

    Do you have the necessary information to answer this question?
    <<<
    {user_question}
    >>>

    Answer with only 1 word: "Yes" or "No"
    (answer)
    """
    
def fabricate_answer_prompt(api_url, user_question, file_to_explore):
    return f"""
    Answer the user's question:
    <<<
    {user_question}
    >>>
    Based on the information you know about the repository, and the information in this file:
    <<<
    {github.fetch_file_content_from_github(api_url, file_to_explore)}
    >>>
    """
    