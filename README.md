```generated with Git Reader```
# Git Reader

`gitreader.py` serves as the main script in a Python project focused on utilizing the OpenAI API and Github API to interact with a given Github repository. The project seeks to answer user questions regarding the repository by intelligently selecting files and obtaining relevant content.

## Overview
1. The script begins with fetching the OpenAI API key and constructing a Github API URL based on the user-provided Github repository URL.
2. It then retrieves the contents of the Github repository and creates a `directory.txt` file.
3. The script examines if a `README.md` file is present in the repository. If not, it selects another relevant file to understand the purpose of the repository.
4. Users can ask questions related to the repository, and the script generates appropriate prompts to identify which file contains relevant information.
5. The information sufficiency is checked based on the selected file.
6. Finally, if sufficient information is available, the OpenAI API assists in answering the user's question.

## Dependencies
* OpenAI API: This project requires an OpenAI API key to function correctly.
* Github API: A Github API key may be required depending on rate limits.

## How to Use
1. Run `gitreader.py`.
2. Input the Github repository URL when prompted.
3. Ask questions about the repository and receive answers if sufficient information is available.
4. The main loop allows you to continue asking questions one after another.

## Error Handling
For any exceptions encountered during execution, errors are logged in the `error_log.txt` file.