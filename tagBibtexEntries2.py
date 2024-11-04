import re
import argparse
import os
from collections import defaultdict

# Step 1: Load DOIs and corresponding filenames into a dictionary
def load_dois(dois_files):
    doi_dict = {}
    for file in dois_files:
        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                filename, doi = line.split(',', 1)  # Split on the first comma
                doi_dict[doi.strip()] = filename.strip()  # Map DOI to filename
    return doi_dict

# Step 2: Load tags from myTags.txt into a dictionary
def load_tags(tag_file):
    tags_dict = {}
    with open(tag_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            parts = line.split(':', 1)
            if len(parts) < 2:
                continue
            filename, tags = parts
            # print(filename)
            tags_dict[filename.strip()] = tags.strip()
    return tags_dict

# Step 3: Update BibTeX entries
def add_keywords_to_bibtex(bibtex_file, doi_dict, tags_dict, output_file):
    with open(bibtex_file, 'r') as f:
        bibtex_entries = f.read()

    # Pattern to match individual BibTeX entries
    # entry_pattern = re.compile(r'@(\w+)\{(.+?),\s*(.*?)\n\}', re.DOTALL)
    entry_pattern = re.compile(r'@(\w+){([^,]+),([^@]+)}', re.DOTALL)

    bibtex_dict = defaultdict(list)

    with open(bibtex_file, 'r') as file:
                content = file.read()
                # Find all bibtex entries in the file
                matches = entry_pattern.findall(content)
                for match in matches:
                    # Extract the citekey and the entry
                    entry_type, citekey, entry = match
                    # Store the entry in the dictionary
                    # bibtex_dict[citekey].append(f'@{entry_type}{{{citekey},\n{entry}}}')
                    bibtex_dict[citekey].append(f'@{entry_type}{{{citekey},\n{entry.strip()}}}')
    
    # Dictionary to store the final bibtex entries
    final_bibtex_dict = {}

    # New dictionary to store entries by title
    title_dict = defaultdict(list)

    # Iterate over the bibtex entries
    for citekey, entries in bibtex_dict.items():
        # If there are multiple entries with the same citekey
        if len(entries) > 1:
            for i, entry in enumerate(entries):
                title = re.search(r'title\s*=\s*{([^}]+)}', entry, re.IGNORECASE)

                if title:
                    title = title.group(1)
                    # If title already exists in title_dict
                    if title in title_dict:
                        continue
                    else:
                        # Add title in title_dict
                        title_dict[title].append(entry)
                # Add a letter to the citekey
                new_citekey = citekey + chr(97 + i)
                # Replace the old citekey with the new citekey in the entry
                new_entry = entry.replace(citekey, new_citekey, 1)
                # Store the new entry in the final dictionary
                final_bibtex_dict[new_citekey] = new_entry
        else:
            # Store the entry in the final dictionary
            final_bibtex_dict[citekey] = entries[0]

    # Sort the bibtex entries by citekey
    # sorted_entries = sorted(final_bibt ex_dict.items())


    # for key in final_bibtex_dict.keys():
    # #     # print(key)
    #     # print(type(bibtex_dict[key]))
    #     print(final_bibtex_dict[key])
    #     print('hello')

    #     print(len(bibtex_dict[key]))
    #     # print('hello')
    # for citekey, entry in final_bibtex_dict.items():
    #         print(entry)

    print(tags_dict.values())
    # print(doi_dict.keys())
    # print(doi_dict.values())
    
    for doi in doi_dict.keys():
    # #     #  print(doi)
    #     print(f'Looking for {doi}')

        for citekey, entry in final_bibtex_dict.items():
            # print(entry)
            # print(type(entry))

        #     print(f"Looking for doi in {entry}")
            if doi in entry:
                # print(f"DOI {doi} was found in {citekey}")
                # tags_dict[filename] = tags 
                # doi_dict[doi] = filename

                if doi_dict[doi] in tags_dict.keys():
                    keywords = tags_dict[doi_dict[doi]]
                
                    if "keywords=" not in entry and keywords:
                        # Insert the keywords field at the end of the entry
                        # Check if the last line already has a comma at the end
                        if re.search(r'},\s*$', entry.strip()):
                            # If there’s already a comma, just add the keywords field
                            updated_entry = re.sub(r'}\s*$', f',\nkeywords={{{keywords}}}\n}}', entry.strip(), flags=re.DOTALL)
                        else:
                            # If there’s no comma, add one before the keywords field
                            updated_entry = re.sub(r'\s*}$', f',\nkeywords={{{keywords}}}\n}}', entry.strip(), flags=re.DOTALL)
                    else:
                        # If keywords already exists, keep the entry as it is
                        updated_entry = entry.strip()
            
                    final_bibtex_dict[citekey] = updated_entry
                else:
                    continue
                
    # Sort the bibtex entries by citekey
    sorted_entries = sorted(final_bibtex_dict.items())


    # Write the sorted entries to the final text file
    with open(output_file, 'w') as file:
        for citekey, entry in sorted_entries:
            file.write(entry + '\n\n')
    # for match in entry_pattern.finditer(bibtex_entries):
    #     entry_type, citation_key, content = match.groups()
        
    #     # Initialize keywords field
    #     keywords_field = ''

        # Check if any DOI is a substring in the current entry
        # for doi, filename in doi_dict.items():
            # print(doi)
        #     if doi in content:  # Check if DOI is a substring of the entry content
        #         # Get tags for the corresponding filename
        #         if filename in tags_dict.keys():
        #             print('yes the filename is a key in the tags_dict')
        #             keywords_field = f'keywords = {{{tags_dict[filename]}}},\n'
        #         break  # Exit the loop after finding the DOI

        # # Rebuild the BibTeX entry with keywords
        # updated_content = f'{content}\n    {keywords_field}' if keywords_field else content
        # updated_entry = f'@{entry_type}{{{citation_key},\n{updated_content.strip()}\n}}'
        # updated_bibtex_entries.append(updated_entry.strip())

    # Write updated entries to the output file, ensuring an empty line between entries
    # with open(output_file, 'w') as f:
    #     f.write('\n\n'.join(updated_bibtex_entries) + '\n')  # Ensure the file ends with a newline



parser = argparse.ArgumentParser()
parser.add_argument("inputDirPath", type=str, help="convert pdf in input directory to bibtex file")



args = parser.parse_args()
inputDirPath= args.inputDirPath 

# print(inputDirPath)


# Example usage
found_dois_file = os.path.join(inputDirPath, 'foundDOIs.txt')
# print(found_dois_file)
missing_dois_file = os.path.join(inputDirPath, 'missingDOIs.txt')
# print(missing_dois_file)
tag_file = os.path.join(inputDirPath, 'myTags.txt')
bibtex_file = os.path.join(inputDirPath, 'bibtexEntries.txt')
output_file = os.path.join(inputDirPath, 'updatedBibtexEntries.txt')

# Load DOIs and tags
doi_dict = load_dois([found_dois_file])
doi_dict.update(load_dois([missing_dois_file]))  # Add DOIs from the missingDOIs file
# print(doi_dict)
tags_dict = load_tags(tag_file)
# print(tags_dict)
# Add keywords to BibTeX entries based on DOIs and tags
add_keywords_to_bibtex(bibtex_file, doi_dict, tags_dict, output_file)
