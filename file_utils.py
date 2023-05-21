def fetch_key(program):
    with open(f'{program}_key.txt', 'r') as file:
        return file.read().replace('\n', '')

def fetch_directory_contents_from_file():
    try:
        with open('directory.txt', 'r') as directory_file:
            return directory_file.read()
    except FileNotFoundError:
        return "Directory.txt not found."