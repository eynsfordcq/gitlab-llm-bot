import json 

def fetch_file_content(file_paths: list) -> str:
    '''
    Fetch all the contents of file paths and return a string containing all the contents.
    '''
    file_content = {}
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                file_content[file_path] = file.read().strip()
        except FileNotFoundError:
            print(f"Warning: {file_path} not found. Skipping.")
        except IOError:
            print(f"Error reading {file_path}. Skipping.")
    
    return json.dumps(file_content)