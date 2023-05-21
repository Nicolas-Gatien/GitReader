import os
import openai
import traceback
import sys
from colorama import Fore, Style, init

import github_api_utils as github
import file_utils as files
import openai_utils as ai
import prompts

# Initialize colorama
init(autoreset=True)

def main():
    try:
        openai.api_key = files.fetch_key("openai")
        api_url = create_github_api_url()
        
        print(Fore.GREEN + "\nWriting Directories to File...\n")

        contents_data = github.fetch_github_repo_contents(api_url)
        github.write_repo_directory_to_file(api_url, contents_data)

        try:
            print(Fore.GREEN + "\nFetching README.md...\n")
            readme_content = github.fetch_file_content_from_github(api_url, 'README.md')
            prompt = f"""
        Based on the following README.md file:
        <<<
        {readme_content}
        >>>

        And the file structure of the project:
        <<<
        {files.fetch_directory_contents_from_file()}
        >>>

        Give a 1 paragraph explanation of what this repository is about.
        """
        except FileNotFoundError:
            print(Fore.RED + "Could not find README.md")
            print(Fore.GREEN + "README.md not found, looking for next best file")
            prompt = prompts.fabricate_file_selection_prompt(" ", "What file most likely has code describing what this repository is about?")
            file_to_explore = ai.generate_gpt_response(prompt)

            print("\033[90m\n I would like to explore: " + file_to_explore + "\033[0m" + "\n")
            prompt = f"""
        Based on the content of the follwing file:
        <<<
        {github.fetch_file_content_from_github(api_url, file_to_explore)}
        >>>

        And the file structure of the project:
        <<<
        {files.fetch_directory_contents_from_file()}
        >>>

        Give a 1 paragraph explanation of what this repository is about.
        """
		
        context = [
            {
                "role": "system",
                "content": "You are an expert programmer with multiple centuries of experience programming. Your job is to be as helpful as possible by explaining details based on the information you are given about the Github Repository.",
            }
        ]

        print(Fore.CYAN + prompt + "\n")

        print(Fore.GREEN + "Describing Repo... \n")

        description = ai.generate_gpt_response_with_context(prompt, context)
        print(description + "\n")

        while True:
            # Ask the user for a question
            user_question = input("\033[34mWhat is your question: ")

            # Question 1
            prompt = prompts.fabricate_file_selection_prompt(description, user_question)
            file_to_explore = ai.generate_gpt_response(prompt)

            print("\033[90m\n I would like to explore: " + file_to_explore + "\033[0m" + "\n")

            if file_to_explore == "None" or file_to_explore == "None.":
            # If no file is relevant, answer the user's question without file info
                context = ai.reset_context_if_needed(context,prompt)
                prompt = prompts.fabricate_answer_prompt(api_url, user_question, None)
                response = ai.generate_gpt_response_with_context(prompt, context)
                print(response + "\n")
                continue

            # Question 2
            prompt = prompts.fabricate_info_sufficiency_prompt(api_url, description, file_to_explore, user_question)
            answer = ai.generate_gpt_response(prompt)
            print("\033[90m\n Based on the information in the file, do you have enough information: " + answer + "\033[0m" + "\n")

            context = ai.reset_context_if_needed(context, prompt)
            
            # If "Yes", move to answer the user's question, otherwise, loop back to question 1 with file_to_explore added to exclude_files
            if "Yes" in answer:
                prompt = prompts.fabricate_answer_prompt(api_url, user_question, file_to_explore)
                response = ai.generate_gpt_response_with_context(prompt, context)
                print(response + "\n")
    
    except Exception as e:
        exc_info = sys.exc_info()
        lines = traceback.format_exception(*exc_info)
        with open('error_log.txt', 'w') as file:
            for line in lines:
                file.write(line)

def create_github_api_url():
    github_url = get_valid_git_url()

    split_url = github_url.split('/')
    username, repo = split_url[-2], split_url[-1]

    api_url = f'https://api.github.com/repos/{username}/{repo}'
    return api_url

def get_valid_git_url():
    while True:
        github_url = input("Please provide a link to the GitHub repository: ")
        try:
            github.validate_url_format(github_url)
            break  # if the URL is valid, we break the loop
        except ValueError:
            print(Fore.RED + "\nLink Not Valid\n" + Style.RESET_ALL)
    return github_url

if __name__ == "__main__":
    main()