import re
import argparse
import os

# Load DOIs from a specified file into a dictionary
def load_dois(doi_file):
    doi_dict = {}
    with open(doi_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Split on the comma to separate filename and DOI
            parts = line.split(',')
            if len(parts) < 2:
                continue
            
            filename = parts[0].strip()  # The filename
            doi = parts[1].strip()  # The DOI
            doi_dict[doi] = filename
    return doi_dict

# Read tags from myTags.txt into a dictionary keyed by filename
def load_tags(tag_file):
    tags_dict = {}
    with open(tag_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Split line into filename and tags using ':' as the separator
            parts = line.split(':', 1)  # Only split on the first colon
            if len(parts) < 2:
                continue
            
            filename, tags = parts
            tags_dict[filename.strip()] = tags.strip()
    return tags_dict

# Add keywords to each BibTeX entry based on DOI and corresponding tags
def add_keywords_to_bibtex(bibtex_file, doi_dict, tags_dict, output_file):
    with open(bibtex_file, 'r') as f:
        bibtex_entries = f.read()

    # Pattern to match individual BibTeX entries
    entry_pattern = re.compile(r'@(\w+)\{(.+?),\s*(.*?)\n\}', re.DOTALL)
    updated_bibtex_entries = []

    for match in entry_pattern.finditer(bibtex_entries):
        entry_type, citation_key, content = match.groups()
        
        # Extract the URL field from the content
        url_match = re.search(r'url\s*=\s*{(https?://[^}]+)}', content, re.IGNORECASE)
        doi_in_url = url_match.group(1) if url_match else None

        # Remove all leading whitespace for each subfield line, so there is no indenting
        content_lines = content.splitlines()
        cleaned_content = '\n'.join(line.strip() for line in content_lines if line.strip())

        # Check if any DOI from the doi_dict is a substring of the URL
        found_keywords = False
        for doi, filename in doi_dict.items():
            if doi in doi_in_url:
                if filename in tags_dict:
                    keywords_field = f'keywords = {{{tags_dict[filename]}}},\n'
                    updated_content = f'{cleaned_content},\n{keywords_field}'  # Add keywords after existing fields
                    found_keywords = True
                    break  # Stop checking after finding a match

        if not found_keywords:
            updated_content = cleaned_content + ','  # Maintain comma after last field

        # Rebuild the BibTeX entry with no indentation
        updated_entry = f'@{entry_type}{{{citation_key},\n{updated_content}\n}}'
        updated_bibtex_entries.append(updated_entry + '\n')

    # # Write updated entries to the output file
    # with open(output_file, 'w') as f:
    #     for entry in updated_bibtex_entries:
    #         f.write(entry.strip() + '\n\n')  # Ensure each entry is followed by a newline
    # Write updated entries to the output file, ensuring an empty line between entries
    with open(output_file, 'w') as f:
        # Join the entries with a double newline to ensure separation
        f.write('\n\n'.join(updated_bibtex_entries) + '\n')  # Add an extra newline at the end




parser = argparse.ArgumentParser()
parser.add_argument("inputDirPath", type=str, help="convert pdf in input directory to bibtex file")



args = parser.parse_args()
inputDirPath= args.inputDirPath 

print(inputDirPath)


# Example usage
found_dois_file = os.path.join(inputDirPath, 'foundDOIs.txt')
print(found_dois_file)
missing_dois_file = os.path.join(inputDirPath, 'missingDOIs.txt')
tag_file = os.path.join(inputDirPath, 'myTags.txt')
bibtex_file = os.path.join(inputDirPath, 'bibtexEntries.txt')
output_file = os.path.join(inputDirPath, 'updatedBibtexEntries.txt')

# Load DOIs and tags
doi_dict = load_dois(found_dois_file)
doi_dict.update(load_dois(missing_dois_file))  # Add DOIs from the missingDOIs file
tags_dict = load_tags(tag_file)

# Add keywords to BibTeX entries based on DOIs and tags
add_keywords_to_bibtex(bibtex_file, doi_dict, tags_dict, output_file)
