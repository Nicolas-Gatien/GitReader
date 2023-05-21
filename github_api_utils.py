import re
import requests
import base64
import openai_utils as ai

import file_utils as files

def validate_url_format(url):
    pattern = re.compile('https://github.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+')
    if not pattern.match(url):
        raise ValueError(f"Invalid GitHub URL: {url}")

# Add your token here
token = files.fetch_key("github")

headers = {'Authorization': f'token {token}'}
    
def fetch_file_content_from_github(api_url, path, retry=False):
    path = path.lstrip("/\\") if path else path
    file_url = f'{api_url}/contents/{path}'
    print(file_url)
    response = requests.get(file_url, headers=headers)
    file_data = response.json()
    if response.status_code != 200:
        if not retry:
            print(f"\033[31mFile {path} was not found\033[0m")
            prompt = f"""
            Format the following file path: {path}
            So that the following method:
            ---
            def fetch_file_content_from_github(api_url, path):
                path = path.lstrip("/\\") if path else path
                file_url = f'{api_url}/contents/{path}'
                response = requests.get(file_url, headers=headers)
                file_data = response.json()
                if response.status_code != 200:
                    raise FileNotFoundError('File not found')
                return base64.b64decode(file_data['content']).decode('utf-8', 'backslashreplace')
            ---
            Will be able to successfully pull the contents.
            Only respond with the formated path.
            """
            new_path = ai.generate_gpt_response(prompt)
            print(f"\033[90mReformated, going to search for {new_path}\033[0m")
            return fetch_file_content_from_github(api_url, new_path, retry=True)
        else:
            print(f"\033[31mFile does not exist\033[0m")
            raise FileNotFoundError('File not found')
    return base64.b64decode(file_data['content']).decode('utf-8', 'backslashreplace')

    
def fetch_github_repo_contents(api_url):
    contents_url = f'{api_url}/contents'
    return requests.get(contents_url, headers=headers).json()


def write_repo_directory_to_file(api_url, contents_data):
    with open('generated/directory.txt', 'w') as directory_file:
        write_directory_contents_to_file(api_url, contents_data, '', directory_file)

def write_directory_contents_to_file(api_url, contents, path, directory_file):
    print(f"Writing {path} to file")
    if 'message' in contents:
        directory_file.write(contents['message'] + '\n')
        return
    for item in contents:
        new_path = '/'.join([path, item['name']])
        directory_file.write(new_path + '/\n' if item['type'] == 'dir' else new_path + '\n')
        if item['type'] == 'dir':
            dir_url = f'{api_url}/contents/{new_path}'
            dir_contents = requests.get(dir_url, headers=headers).json()
            write_directory_contents_to_file(api_url, dir_contents, new_path, directory_file)
