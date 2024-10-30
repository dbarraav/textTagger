import re
import argparse
import os

# Read tags from myTags.txt into a dictionary
def load_tags(tag_file):
    tags_dict = {}
    with open(tag_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
            
            # Split line into filename and tags, using ':' as the separator
            parts = line.split(':', 1)  # Split on the first ':' only
            if len(parts) < 2:
                # Skip lines that don't have both filename and tags
                continue
            
            filename, tags = parts
            tags_dict[filename.strip()] = tags.strip()
    return tags_dict

# Add keywords to each BibTeX entry
# def add_keywords_to_bibtex(bibtex_file, tags_dict, output_file):
#     with open(bibtex_file, 'r') as f:
#         bibtex_entries = f.read()

#     # Pattern to match individual BibTeX entries
#     entry_pattern = re.compile(r'@(\w+)\{(.+?),\s*(.*?)\n\}', re.DOTALL)
#     updated_bibtex_entries = []

#     for match in entry_pattern.finditer(bibtex_entries):
#         entry_type, citation_key, content = match.groups()
        
#         # Extract the filename from the citation key
#         filename = citation_key + '.pdf'

#         # If tags are available for this file, add them to the entry
#         if filename in tags_dict:
#             keywords_field = f'keywords = {{{tags_dict[filename]}}},\n'
#             # Insert keywords field after the citation key line
#             updated_content = f'{content}\n    {keywords_field}'
#         else:
#             # If no tags, leave content unchanged
#             updated_content = content

#         # Rebuild the BibTeX entry with keywords
#         updated_entry = f'@{entry_type}{{{citation_key},\n    {updated_content}\n}}'
#         updated_bibtex_entries.append(updated_entry)

#     # Write updated entries to the output file
#     with open(output_file, 'w') as f:
#         f.write('\n\n'.join(updated_bibtex_entries))
# Add keywords to each BibTeX entry and format correctly
def add_keywords_to_bibtex(bibtex_file, tags_dict, output_file):
    with open(bibtex_file, 'r') as f:
        bibtex_entries = f.read()

    # Pattern to match individual BibTeX entries
    # entry_pattern = re.compile(r'@(\w+)\{(.+?),\s*(.*?)\n\}', re.DOTALL)
    entry_pattern = re.compile(r'@(\w+)\{(.+?),\s*(.*?)\n\}', re.DOTALL)

    updated_bibtex_entries = []

    for match in entry_pattern.finditer(bibtex_entries):
        entry_type, citation_key, content = match.groups()
        
        # Extract the filename from the citation key
        filename = citation_key + '.pdf'

        # Remove all leading whitespace for each subfield line, so there is no indenting
        content_lines = content.splitlines()
        cleaned_content = '\n'.join(line.strip() for line in content_lines if line.strip())

        # Prepare the entry content with keywords if available
        if filename in tags_dict:
            keywords_field = f'    keywords = {{{tags_dict[filename]}}},\n'
            updated_content = f'{cleaned_content},\n{keywords_field}'  # Add keywords after existing fields
        else:
            updated_content = cleaned_content + ','  # Maintain comma after last field

        # Rebuild the BibTeX entry with consistent indentation and spacing
        updated_entry = f'@{entry_type}{{{citation_key},\n{updated_content}\n}}'
        updated_bibtex_entries.append(updated_entry + '\n')

    # Write updated entries to the output file with double newlines between entries
    with open(output_file, 'w') as f:
        f.write('\n\n'.join(updated_bibtex_entries) + '\n\n')


parser = argparse.ArgumentParser()
parser.add_argument("inputDirPath", type=str, help="convert pdf in input directory to bibtex file")


args = parser.parse_args()
inputDirPath= args.inputDirPath 




# Specify file paths
tag_file = os.path.join(inputDirPath, 'myTags.txt')
bibtex_file = os.path.join(inputDirPath, 'bibtexEntries.txt')
output_file = os.path.join(inputDirPath, 'updatedBibtexEntries.txt')

print(tag_file)
# Load tags and add keywords to bibtex entries
tags_dict = load_tags(tag_file)
print(tags_dict)
add_keywords_to_bibtex(bibtex_file, tags_dict, output_file)
