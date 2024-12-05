import os
import time 

def create_or_update_md_files(PDFdirectory, MDdirectory):
    for subdir, _, files in os.walk(PDFdirectory):
        # Determine the relative path of the current subdirectory within PDFdirectory
        relative_path = os.path.relpath(subdir, PDFdirectory)
        print(relative_path)
        # Corresponding directory in MDdirectory
        md_subdir = os.path.join(MDdirectory, relative_path)
        os.makedirs(md_subdir, exist_ok=True)  # Ensure the subdirectory exists
        print(f"Going through subdirectory {subdir}")
        # Process each PDF file in the current subdirectory
        for file in files:
            if file.endswith(".pdf"):
                # print(f"Creating/Updating md file {file}")
                pdf_name = file[:-4]  # Remove .pdf extension
                pdf_path = os.path.join(subdir, file)
                
                # Path to corresponding .md file
                md_file_path = os.path.join(md_subdir, f"{pdf_name}.md")
                
                # Create or update the .md file
                create_or_update_md_file(pdf_path, md_file_path)
        print("-----------------FINISHED WITH THIS SUBDIRECTORY-----------------")
        time.sleep(10)

def read_tags_from_file(tags_file, pdf_name):
    if not os.path.exists(tags_file):
        return []
    tags = []
    with open(tags_file, "r") as f:
        for line in f:
            if line.startswith(f"{pdf_name}:"):
                tags_part = line.split(":", 1)[-1].strip()
                tags = [f"#{tag.strip()}" for tag in tags_part.split(",") if tag.strip()]
                break
    return tags

# def extract_existing_tags(md_file_path):
#     tags = []
#     with open(md_file_path, "r") as f:
#         lines = f.readlines()
#         for line in lines:
#             line = line.strip()
#             if line.startswith("#"):
#                 tags.extend(line.split())
#             elif line.startswith("##"):
#                 break  # Stop processing tags once a heading line is encountered
#     return tags

def extract_existing_tags(md_file_path):
    tags = []
    with open(md_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            stripped_line = line.strip()
            # Skip processing once we encounter the first heading
            if stripped_line.startswith("##"):
                break
            # Collect tags from lines starting with '#'
            if stripped_line.startswith("#") and not stripped_line.startswith("##"):
                tags.extend(stripped_line.split())
    return tags


def create_or_update_md_file(pdf_path, md_file_path):
    # Read tags from the myTags.txt in the same directory as the PDF file
    tags_file = os.path.join(os.path.dirname(pdf_path), "myTags.txt")
    tags = read_tags_from_file(tags_file, os.path.basename(pdf_path))
    # print(tags)
    # Existing tags in the .md file (if it exists)
    existing_tags = []
    if os.path.exists(md_file_path):
        existing_tags = extract_existing_tags(md_file_path)
    
    # Combine and deduplicate tags
    updated_tags = sorted(set(existing_tags + tags))
    
    # Write the .md file with the updated tags
    if os.path.exists(md_file_path):
        print(f"Updating md file {os.path.splitext(os.path.basename(pdf_path))[0]}")
        update_md_file(md_file_path, pdf_path, updated_tags)
    else:
        print(f"Creating md file {os.path.splitext(os.path.basename(pdf_path))[0]}")
        create_md_file(md_file_path, pdf_path, updated_tags)
    # write_md_file(md_file_path, pdf_path, updated_tags)

def create_md_file(md_file_path, pdf_path, tags):
    annotTargetPath = os.path.join(*os.path.normpath(pdf_path).split(os.sep)[-3:])
    annotation_target = f"annotation-target: {annotTargetPath}"

    tags_line = " ".join(tags)
    createdContent = [
        "---",
        annotation_target,
        "---",
        tags_line,
        "",
        # f"## {os.path.basename(pdf_path)}", #os.path.splitext(os.path.basename(file_path))[0]
        f"## {os.path.splitext(os.path.basename(pdf_path))[0]}", 
        "",
        "```dataview",
        'TABLE WITHOUT ID question as "Questions"',
        "where file.path = this.file.path",
        "```",
        "",
        "```dataview",
        'TABLE WITHOUT ID reference as "References to Check"',
        "where file.path = this.file.path",
        "```",
    ]

    if not os.path.exists(md_file_path):
        new_lines = createdContent
        with open(md_file_path, 'w'): pass

    #Write content to new file
    with open(md_file_path, 'w') as f:
        f.writelines("\n".join(createdContent))

def update_md_file(md_file_path, pdf_path, tags):
    annotTargetPath = os.path.join(*os.path.normpath(pdf_path).split(os.sep)[-3:])
    annotation_target = f"annotation-target: {annotTargetPath}"
    tags_line = " ".join(tags)
    existingContent = [
        "---",
        annotation_target,
        "---",
        tags_line,
        "",
        # f"## {os.path.basename(pdf_path)}", #os.path.splitext(os.path.basename(file_path))[0]
        f"## {os.path.splitext(os.path.basename(pdf_path))[0]}", 
        "",
    ]

    with open(md_file_path, 'r') as f:
        lines = f.readlines()

    # Find the index where the first '##' heading appears
    heading_index = next((i for i, line in enumerate(lines) if line.startswith(f"## ")), None)
    newContent = existingContent
    
    # print(lines[:heading_index])
    # print("\n".join(newContent))
    # print('hello')
    # for line in lines[heading_index+1:]:
    #     print(line)
    #Write content to new file
    with open(md_file_path, 'w') as f:
        # f.writelines("\n".join(newContent)+lines[heading_index+1:])
        f.write("\n".join(newContent) + "".join(lines[heading_index + 1:]))

    # if heading_index == len(lines):
    # with open(md_file_path, 'w') as f:
    #     f.writelines(lines[heading_index+1:])
        
#---------------------------------------------------------------------------
# def write_md_file(md_file_path, pdf_path, tags):
#     annotTargetPath = os.path.join(*os.path.normpath(pdf_path).split(os.sep)[-3:])
#     annotation_target = f"annotation-target: {annotTargetPath}"
#     tags_line = " ".join(tags)
#     existingContent = [
#         "---",
#         annotation_target,
#         "---",
#         tags_line,
#         "",
#         # f"## {os.path.basename(pdf_path)}", #os.path.splitext(os.path.basename(file_path))[0]
#         f"## {os.path.splitext(os.path.basename(pdf_path))[0]}", 
#         "",
#     ]
#     createdContent = [
#         "---",
#         annotation_target,
#         "---",
#         tags_line,
#         "",
#         # f"## {os.path.basename(pdf_path)}", #os.path.splitext(os.path.basename(file_path))[0]
#         f"## {os.path.splitext(os.path.basename(pdf_path))[0]}", 
#         "",
#         "```dataview",
#         'TABLE WITHOUT ID question as "Questions"',
#         "where file.path = this.file.path",
#         "```",
#         "",
#         "```dataview",
#         'TABLE WITHOUT ID reference as "References to Check"',
#         "where file.path = this.file.path",
#         "```",
#     ]
#     new_lines = existingContent
#     # if os.path.exists()
#     if not os.path.exists(md_file_path):
#         new_lines = createdContent
#         with open(md_file_path, 'w'): pass

#     with open(md_file_path, 'r') as f:
#         lines = f.readlines()
    
#     # Find the index where the first '##' heading appears
#     heading_index = next((i for i, line in enumerate(lines) if line.startswith("## ")), None)
    
#     # If a heading was found, replace lines up to and including it with new lines
#     if heading_index is not None:
#         # Replace the lines before and including the first heading with the new lines
#         updated_lines = new_lines + lines[heading_index + 1:]  # Skip the heading line itself
#     else:
#         # If no heading is found, just append the new lines at the end
#         updated_lines = new_lines + lines
#     # Write the updated content back to the file
#     with open(md_file_path, 'w') as f:
#         f.writelines("\n".join(updated_lines))
#     # with open(md_file_path, "w") as f:
#     #     f.write("\n".join(content))
#---------------------------------------------------------------------------
# def write_md_file(md_file_path, pdf_path, tags):
#     # Normalize and adjust the PDF path for the annotation target
#     annotTargetPath = os.path.join(*os.path.normpath(pdf_path).split(os.sep)[-3:])
#     annotation_target = f"annotation-target: {annotTargetPath}"
#     tags_line = " ".join(tags)
#     pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]  # Name of the PDF file without extension
    
#     # Content template for new or updated files
#     created_content = [
#         "---",
#         annotation_target,
#         "---",
#         tags_line,
#         "",
#         f"## {pdf_name}",
#         "",
#         "```dataview",
#         'TABLE WITHOUT ID question as "Questions"',
#         "where file.path = this.file.path",
#         "```",
#         "",
#         "```dataview",
#         'TABLE WITHOUT ID reference as "References to Check"',
#         "where file.path = this.file.path",
#         "```",
#     ]
    
#     if not os.path.exists(md_file_path):
#         # If the file doesn't exist, create it with the template
#         with open(md_file_path, "w") as f:
#             f.write("\n".join(created_content))
#         return

#     # Read the existing file
#     with open(md_file_path, "r") as f:
#         lines = f.readlines()
    
#     # Find the index of the first heading that starts with "##"
#     heading_index = next((i for i, line in enumerate(lines) if line.startswith("## ")), None)
    
#     if heading_index is not None:
#         # Replace everything up to and including the heading
#         updated_lines = created_content + lines[heading_index + 1:]
#     else:
#         # If no heading is found, just prepend the created content
#         updated_lines = created_content + lines

#     # Write back the updated content, ensuring no duplicate blank lines
#     with open(md_file_path, "w") as f:
#         f.write("\n".join(line.strip() for line in updated_lines if line.strip()))
# --------------------------------------------------------------------------------
# def write_md_file(md_file_path, pdf_path, tags):
#     # Normalize and adjust the PDF path for the annotation target
#     annotTargetPath = os.path.join(*os.path.normpath(pdf_path).split(os.sep)[-3:])
#     annotation_target = f"annotation-target: {annotTargetPath}"
#     tags_line = " ".join(tags)
#     pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]  # Name of the PDF file without extension

#     # Header structure for the `.md` file
#     new_header_content = [
#         "---",
#         annotation_target,
#         "---",
#         tags_line,
#         "",
#         f"## {pdf_name}",
#         "",
#     ]

#     if not os.path.exists(md_file_path):
#         # If the file doesn't exist, create it with the full structure
#         full_content = new_header_content + [
#             "```dataview",
#             'TABLE WITHOUT ID question as "Questions"',
#             "where file.path = this.file.path",
#             "```",
#             "",
#             "```dataview",
#             'TABLE WITHOUT ID reference as "References to Check"',
#             "where file.path = this.file.path",
#             "```",
#         ]
#         with open(md_file_path, "w") as f:
#             f.write("\n".join(full_content) + "\n")
#         return

#     # If the file exists, read its content
#     with open(md_file_path, "r") as f:
#         lines = f.readlines()

#     # Find the index of the first subheading
#     heading_index = next((i for i, line in enumerate(lines) if line.startswith("## ")), None)

#     # Extract pre-heading and post-heading sections
#     if heading_index is not None:
#         pre_heading_lines = lines[:heading_index]
#         post_heading_lines = lines[heading_index:]  # Preserve all content after the first subheading
#     else:
#         pre_heading_lines = lines
#         post_heading_lines = []

#     # Check if the header needs updating
#     existing_annotation = next((line.strip() for line in pre_heading_lines if line.startswith("annotation-target:")), "")
#     existing_tags = next((line.strip() for line in pre_heading_lines if line.startswith("#")), "")

#     if existing_annotation == annotation_target and existing_tags == tags_line:
#         # No updates needed; header is already correct
#         return

#     # Update the pre-heading lines with the new header content
#     updated_pre_heading_lines = new_header_content

#     # Combine the updated header with the unmodified rest of the file
#     updated_lines = updated_pre_heading_lines + post_heading_lines

#     # Write back the updated content
#     with open(md_file_path, "w") as f:
#         f.write("\n".join(updated_lines) + "\n")



# Example usage
PDFdirectory = "/Users/diegobarra/Library/CloudStorage/OneDrive-WashingtonUniversityinSt.Louis/Research_PathakLab/scientificarticles"
MDdirectory = "/Users/diegobarra/Documents/ObsidianVault/PhD/scientificArticles"
create_or_update_md_files(PDFdirectory, MDdirectory)
