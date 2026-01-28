import re
import string
import requests

orcid = '0000-0003-3838-2860'

# Retrieve all works from ORCID
response = requests.get(
    'https://pub.orcid.org/v3.0/{}/works'.format(orcid),
    headers={"Accept": "application/orcid+json"},
)
record = response.json()

put_codes = []
for work in record['group']:
    put_code = work['work-summary'][0]['put-code']
    put_codes.append(put_code)

# Retrieve citation for each work
citations = []
for put_code in put_codes:
    response = requests.get(
        'https://pub.orcid.org/v3.0/{}/work/{}'.format(orcid, put_code),
        headers={"Accept": "application/orcid+json"},
    )
    work = response.json()
    if work['citation'] is not None:
        citations.append(work['citation']['citation-value'])

# Deduplicate BibTeX entry keys by appending a, b, c, ... when needed
key_pattern = re.compile(r'^(@\w+\{)([^,]+)(,)', re.MULTILINE)

# First pass: count occurrences of each key
key_counts = {}
for citation in citations:
    match = key_pattern.search(citation)
    if match:
        key = match.group(2)
        key_counts[key] = key_counts.get(key, 0) + 1

# Second pass: rename duplicates
key_seen = {}
deduplicated = []
for citation in citations:
    match = key_pattern.search(citation)
    if match:
        key = match.group(2)
        if key_counts[key] > 1:
            idx = key_seen.get(key, 0)
            suffix = string.ascii_lowercase[idx]
            new_key = key + suffix
            citation = key_pattern.sub(
                match.group(1) + new_key + match.group(3), citation, count=1
            )
            key_seen[key] = idx + 1
    deduplicated.append(citation)

# Write output
with open('output.bib', 'w') as bibfile:
    for citation in deduplicated:
        bibfile.write(citation)
        bibfile.write('\n')

print('Wrote {} citations to output.bib'.format(len(deduplicated)))
