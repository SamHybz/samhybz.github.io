#!/usr/bin/env python
# coding: utf-8

# # Publications markdown generator for academicpages
#
# Takes a set of bibtex of publications and converts them for use with [academicpages.github.io](academicpages.github.io). This is an interactive Jupyter notebook ([see more info here](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html)).
#
# The core python code is also in `pubsFromBibs.py`.
# Run either from the `markdown_generator` folder after replacing updating the publist dictionary with:
# * bib file names
# * specific venue keys based on your bib file preferences
# * any specific pre-text for specific files
# * Collection Name (future feature)
#
# TODO: Make this work with other databases of citations,
# TODO: Merge this with the existing TSV parsing solution


from pybtex.database.input import bibtex
import pybtex.database.input.bibtex
from time import strptime
import string
import html
import os
import re

# LaTeX accent commands to Unicode mapping
LATEX_ACCENTS = {
    "`": {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù",
          "A": "À", "E": "È", "I": "Ì", "O": "Ò", "U": "Ù"},
    "'": {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú",
          "A": "Á", "E": "É", "I": "Í", "O": "Ó", "U": "Ú"},
    "^": {"a": "â", "e": "ê", "i": "î", "o": "ô", "u": "û",
          "A": "Â", "E": "Ê", "I": "Î", "O": "Ô", "U": "Û"},
    '"': {"a": "ä", "e": "ë", "i": "ï", "o": "ö", "u": "ü",
          "A": "Ä", "E": "Ë", "I": "Ï", "O": "Ö", "U": "Ü"},
    "~": {"a": "ã", "n": "ñ", "o": "õ", "A": "Ã", "N": "Ñ", "O": "Õ"},
    "c": {"c": "ç", "C": "Ç"},
}


def latex_to_unicode(text):
    """Convert LaTeX accent commands to Unicode characters."""
    # Handle {\cmd{char}} patterns, e.g. {\'{e}} or {\c{c}}
    def replace_accent(m):
        cmd = m.group(1)
        char = m.group(2)
        return LATEX_ACCENTS.get(cmd, {}).get(char, char)

    text = re.sub(r"\{\\([`'^\"~c])\{([a-zA-Z])\}\}", replace_accent, text)
    # Handle \cmd{char} without outer braces
    text = re.sub(r"\\([`'^\"~c])\{([a-zA-Z])\}", replace_accent, text)
    # Handle remaining braces and backslashes
    text = text.replace("{", "").replace("}", "").replace("\\", "")
    return text


# todo: incorporate different collection types rather than a catch all publications, requires other changes to template
publist = {
    "proceeding": {
        "file": "output.bib",
        "venuekey": "booktitle",
        "venue-pretext": "In the proceedings of ",
        "collection": {"name": "publications", "permalink": "/publication/"},
    },
    "journal": {
        "file": "output.bib",
        "venuekey": "journal",
        "venue-pretext": "",
        "collection": {"name": "publications", "permalink": "/publication/"},
    },
}

html_escape_table = {"&": "&amp;", '"': "&quot;", "'": "&apos;"}


def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c, c) for c in text)


for pubsource in publist:
    parser = bibtex.Parser()
    bibdata = parser.parse_file(publist[pubsource]["file"])

    # loop through the individual references in a given bibtex file
    for bib_id in bibdata.entries:
        # reset default date
        pub_year = "1900"
        pub_month = "01"
        pub_day = "01"

        b = bibdata.entries[bib_id].fields

        try:
            pub_year = f"{b['year']}"

            # todo: this hack for month and day needs some cleanup
            if "month" in b.keys():
                if len(b["month"]) < 3:
                    pub_month = "0" + b["month"]
                    pub_month = pub_month[-2:]
                elif b["month"] not in range(12):
                    tmnth = strptime(b["month"][:3], "%b").tm_mon
                    pub_month = "{:02d}".format(tmnth)
                else:
                    pub_month = str(b["month"])
            if "day" in b.keys():
                pub_day = str(b["day"])

            pub_date = pub_year + "-" + pub_month + "-" + pub_day

            # strip out {} as needed (some bibtex entries that maintain formatting)
            clean_title = (
                latex_to_unicode(b["title"])
                .replace(" ", "-")
            )

            url_slug = re.sub("\\[.*\\]|[^a-zA-Z0-9_-]", "", clean_title)
            url_slug = url_slug.replace("--", "-")

            md_filename = (str(pub_date) + "-" + url_slug + ".md").replace("--", "-")
            html_filename = (str(pub_date) + "-" + url_slug).replace("--", "-")

            # Build Citation from text
            citation = ""

            # citation authors - todo - add highlighting for primary author?
            for author in bibdata.entries[bib_id].persons["author"]:
                citation = (
                    citation
                    + " "
                    + latex_to_unicode(author.first_names[0])
                    + " "
                    + latex_to_unicode(author.last_names[0])
                    + ", "
                )

            # citation title
            citation = (
                citation
                + '"'
                + html_escape(
                    latex_to_unicode(b["title"])
                )
                + '."'
            )

            # add venue logic depending on citation type
            venue = publist[pubsource]["venue-pretext"] + latex_to_unicode(
                b[publist[pubsource]["venuekey"]]
            )

            citation = citation + " " + html_escape(venue)
            citation = citation + ", " + pub_year + "."

            ## YAML variables
            md = (
                '---\ntitle: "'
                + html_escape(
                    latex_to_unicode(b["title"])
                )
                + '"\n'
            )

            md += """collection: """ + publist[pubsource]["collection"]["name"]

            md += (
                """\npermalink: """
                + publist[pubsource]["collection"]["permalink"]
                + html_filename
            )

            note = False
            if "note" in b.keys():
                if len(str(b["note"])) > 5:
                    md += "\nexcerpt: '" + html_escape(b["note"]) + "'"
                    note = True

            md += "\ndate: " + str(pub_date)

            md += "\nvenue: '" + html_escape(venue) + "'"

            url = False
            if "url" in b.keys():
                if len(str(b["url"])) > 5:
                    md += "\npaperurl: '" + b["url"] + "'"
                    url = True

            md += "\ncitation: '" + html_escape(citation) + "'"

            md += "\n---"

            ## Markdown description for individual page
            if note:
                md += "\n" + html_escape(b["note"]) + "\n"

            if url:
                md += "\n[Access paper here](" + b["url"] + '){:target="_blank"}\n'
            else:
                md += (
                    "\nUse [Google Scholar](https://scholar.google.com/scholar?q="
                    + html.escape(clean_title.replace("-", "+"))
                    + '){:target="_blank"} for full citation'
                )

            md_filename = os.path.basename(md_filename)

            with open("../_publications/" + md_filename, "w", encoding="utf-8") as f:
                f.write(md)
            print(
                f'SUCESSFULLY PARSED {bib_id}: "',
                b["title"][:60],
                "..." * (len(b["title"]) > 60),
                '"',
            )
        # field may not exist for a reference
        except KeyError as e:
            print(
                f'WARNING Missing Expected Field {e} from entry {bib_id}: "',
                b["title"][:30],
                "..." * (len(b["title"]) > 30),
                '"',
            )
            continue
