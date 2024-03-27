import requests
import os
import re

# Your Personal Access Token (PAT) and repository details
ACCESS_TOKEN = 'YOUR_PERSONAL_ACCESS_TOKEN'
REPO_OWNER = 'repository_owner'
REPO_NAME = 'repository_name'
OUTPUT_FILE = 'output_sentences.txt'

def get_repo_contents(path=''):
    """
    Recursively fetches the contents of the repository starting from the specified path.
    """
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    headers = {'Authorization': f'token {ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
    contents = response.json()

    files_content = ""
    for item in contents:
        if item['type'] == 'dir':  # If the item is a directory, recursively fetch its contents
            files_content += get_repo_contents(item['path'])
        elif item['type'] == 'file' and item['name'].endswith('.txt'):  # Process only text files for simplicity
            file_response = requests.get(item['download_url'], headers=headers)
            file_response.raise_for_status()
            file_content = file_response.text
            # Extract sentences ending with specific domains
            sentences = extract_sentences(file_content)
            if sentences:
                files_content += f"\n\nFile: {item['path']}\n\n" + '\n'.join(sentences)
    return files_content

def extract_sentences(text):
    """
    Extracts sentences ending with .com, .ai, .cloud from the provided text.
    """
    # This regex matches sentences ending with .com, .ai, .cloud
    regex_pattern = r'[^.!?]*\.(com|ai|cloud)[^.!?]*[.!?]'
    matches = re.findall(regex_pattern, text, re.IGNORECASE)
    return matches

def main():
    """
    Main function to fetch all repository files' content, filter sentences, and write to an output file.
    """
    try:
        matching_sentences = get_repo_contents()
        with open(OUTPUT_FILE, 'w') as f:
            f.write(matching_sentences)
        print(f"Matching sentences have been written to {OUTPUT_FILE}")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()


srever_name mynameisamerica.com;
