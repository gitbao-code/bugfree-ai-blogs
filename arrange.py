import os
import re
from datetime import datetime

# Path to your blogs folder
blogs_dir = "./"
readme_file = "README.md"

# Regular expressions to extract the title and datePublished from YAML front matter
title_pattern = re.compile(r'title:\s*"(.*?)"')
date_pattern = re.compile(r"datePublished:\s*(.*?)\n")

# Collect blog metadata
blogs = []

for blog in os.listdir(blogs_dir):
    if blog.endswith(".md"):
        blog_path = os.path.join(blogs_dir, blog)
        with open(blog_path, "r") as file:
            content = file.read()
            title_match = title_pattern.search(content)
            date_match = date_pattern.search(content)

            if title_match and date_match:
                title = title_match.group(1)
                date_str = date_match.group(1).strip()

                # Remove the timezone abbreviation (everything in parentheses)
                date_str_cleaned = re.sub(r"\s*\(.*\)$", "", date_str)

                # Convert datePublished to a datetime object
                try:
                    print(date_str_cleaned)
                    date_published = datetime.strptime(
                        date_str_cleaned, "%a %b %d %Y %H:%M:%S %Z%z"
                    )
                except ValueError:
                    print(f"Invalid date format in {blog}: {date_str}")
                    continue

                # Convert title to a filename-friendly format
                new_filename = (
                    re.sub(r"[^\w\s-]", "", title).replace(" ", "-").lower() + ".md"
                )
                new_file_path = os.path.join(blogs_dir, new_filename)

                # Rename the file if necessary
                if blog_path != new_file_path:
                    os.rename(blog_path, new_file_path)

                # Append metadata
                blogs.append(
                    {"title": title, "date": date_published, "filename": new_filename}
                )

# Sort blogs by datePublished (ascending order: oldest to latest)
blogs.sort(key=lambda x: x["date"])

# Generate Table of Contents
toc = "# Table of Contents\n\n"
for idx, blog in enumerate(blogs, 1):
    toc += f"{idx}. [{blog['title']}]({blog['filename']})\n"

# Append the TOC to the README.md
with open(readme_file, "a") as readme:  # Use "a" to append
    readme.write("\n" + toc)  # Add a newline before the TOC for better formatting

print("File renaming, sorting, and Table of Contents appended successfully!")
