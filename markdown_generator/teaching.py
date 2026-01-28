
# coding: utf-8

# # Teaching markdown generator for academicpages
#
# Takes a TSV of teaching experiences with metadata and converts them for use with [academicpages.github.io](academicpages.github.io).
# Run from the `markdown_generator` folder after replacing `teaching.tsv` with one containing your data.

import pandas as pd
import os

# ## Data format
#
# The TSV needs to have the following columns: title, type, url_slug, venue, date, location, description, with a header at the top.
# Many of these fields can be blank, but the columns must be in the TSV.
#
# - Fields that cannot be blank: `title`, `url_slug`, `date`. All else can be blank. `type` defaults to "Course"
# - `date` must be formatted as YYYY-MM-DD.
# - `url_slug` will be the descriptive part of the .md file and the permalink URL for the page about the teaching experience.
#     - The .md file will be `YYYY-MM-DD-[url_slug].md` and the permalink will be `https://[yourdomain]/teaching/YYYY-MM-DD-[url_slug]`
#     - The combination of `url_slug` and `date` must be unique, as it will be the basis for your filenames

# ## Import TSV
#
# Pandas makes this easy with the read_csv function. We are using a TSV, so we specify the separator as a tab, or `\t`.

teaching = pd.read_csv("teaching.tsv", sep="\t", header=0)
teaching

# ## Escape special characters
#
# YAML is very picky about how it takes a valid string, so we are replacing single and double quotes (and ampersands) with their HTML encoded equivilents.

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
    }

def html_escape(text):
    if type(text) is str:
        return "".join(html_escape_table.get(c,c) for c in text)
    else:
        return "False"

# ## Creating the markdown files
#
# This loops through all the rows in the TSV dataframe, then starts to concatenate a big string (```md```)
# that contains the markdown for each teaching experience. It does the YAML metadata first, then does the description.

loc_dict = {}

for row, item in teaching.iterrows():

    # Skip rows with missing required fields
    if pd.isna(item.title) or pd.isna(item.url_slug) or pd.isna(item.date):
        print(f"Skipping row {row + 2}: Missing required fields (title, url_slug, or date)")
        continue

    md_filename = str(item.date) + "-" + item.url_slug + ".md"
    html_filename = str(item.date) + "-" + item.url_slug
    year = item.date[:4]

    md = "---\ntitle: \""   + item.title + '"\n'
    md += "collection: teaching" + "\n"

    if len(str(item.type)) > 3:
        md += 'type: "' + item.type + '"\n'
    else:
        md += 'type: "Course"\n'

    md += "permalink: /teaching/" + html_filename + "\n"

    if len(str(item.venue)) > 3:
        md += 'venue: "' + item.venue + '"\n'

    if len(str(item.date)) > 3:
        md += "date: " + str(item.date) + "\n"

    if len(str(item.location)) > 3:
        md += 'location: "' + str(item.location) + '"\n'

    md += "---\n"

    if len(str(item.description)) > 3:
        md += "\n" + html_escape(item.description) + "\n"

    md_filename = os.path.basename(md_filename)

    with open("../_teaching/" + md_filename, 'w') as f:
        f.write(md)

print("Teaching markdown files generated successfully!")
