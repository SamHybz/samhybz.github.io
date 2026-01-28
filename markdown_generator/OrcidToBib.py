import re
import string
import requests

orcid = '0000-0003-3838-2860'

# Work types to include and how to classify them
JOURNAL_TYPES = {'journal-article'}
CONFERENCE_TYPES = {'conference-paper', 'conference-poster', 'conference-abstract'}


def build_bibtex_from_metadata(work):
    """Build a BibTeX entry from ORCID metadata when citation is missing."""
    title = work['title']['title']['value']
    wtype = work['type']
    journal = work.get('journal-title')
    journal_name = journal['value'] if journal else ''

    # Get publication date
    pub_date = work.get('publication-date') or {}
    year = (pub_date.get('year') or {}).get('value', '1900')
    month_val = (pub_date.get('month') or {}).get('value', '')

    # Get authors from contributors
    authors = []
    for c in (work.get('contributors') or {}).get('contributor', []):
        name = (c.get('credit-name') or {}).get('value', '')
        if name:
            authors.append(name)
    author_str = ' and '.join(authors)

    # Get DOI and URL
    doi = ''
    url = ''
    for eid in (work.get('external-ids') or {}).get('external-id', []) or []:
        if eid['external-id-type'] == 'doi':
            doi = eid['external-id-value']
            url = 'https://doi.org/{}'.format(doi)

    # If no contributors in ORCID, warn but still generate the entry
    if not authors:
        print('  WARNING: no contributors found, entry will lack authors')

    # Build BibTeX key: LastName_Year
    if authors:
        last_name = authors[0].split()[-1]
    else:
        last_name = title.split()[0]
    bib_key = '{}_{}'.format(last_name, year)

    entry_type = 'article' if wtype in JOURNAL_TYPES else 'inproceedings'
    venue_field = 'journal' if wtype in JOURNAL_TYPES else 'booktitle'

    parts = ['@{}{{{}'.format(entry_type, bib_key)]
    if doi:
        parts.append('\tdoi = {{{}}}'.format(doi))
    if url:
        parts.append('\turl = {{{}}}'.format(url))
    parts.append('\tyear = {}'.format(year))
    if month_val:
        months = {'01': 'jan', '02': 'feb', '03': 'mar', '04': 'apr',
                  '05': 'may', '06': 'jun', '07': 'jul', '08': 'aug',
                  '09': 'sep', '10': 'oct', '11': 'nov', '12': 'dec'}
        parts.append('\tmonth = {{{}}}'.format(months.get(month_val, month_val)))
    if author_str:
        parts.append('\tauthor = {{{}}}'.format(author_str))
    parts.append('\ttitle = {{{}}}'.format(title))
    if journal_name:
        parts.append('\t{} = {{{}}}'.format(venue_field, journal_name))
    parts.append('}')

    return ',\t'.join(parts)


def deduplicate_keys(citations):
    """Deduplicate BibTeX entry keys by appending a, b, c, ... when needed."""
    key_pattern = re.compile(r'^(@\w+\{)([^,]+)(,)', re.MULTILINE)

    key_counts = {}
    for citation in citations:
        match = key_pattern.search(citation)
        if match:
            key = match.group(2)
            key_counts[key] = key_counts.get(key, 0) + 1

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
    return deduplicated


def write_bib(filename, citations):
    """Write citations to a .bib file."""
    with open(filename, 'w') as f:
        for citation in citations:
            f.write(citation)
            f.write('\n')
    print('Wrote {} citations to {}'.format(len(citations), filename))


# Retrieve all works from ORCID
print('Fetching works from ORCID...')
response = requests.get(
    'https://pub.orcid.org/v3.0/{}/works'.format(orcid),
    headers={"Accept": "application/orcid+json"},
)
record = response.json()

journal_citations = []
conference_citations = []

for work_group in record['group']:
    summary = work_group['work-summary'][0]
    put_code = summary['put-code']
    wtype = summary['type']
    title = summary['title']['title']['value']

    # Skip types we don't want (e.g. dissertation-thesis)
    if wtype not in JOURNAL_TYPES and wtype not in CONFERENCE_TYPES:
        print('SKIPPED ({}): {}'.format(wtype, title[:60]))
        continue

    # Fetch full work details
    resp = requests.get(
        'https://pub.orcid.org/v3.0/{}/work/{}'.format(orcid, put_code),
        headers={"Accept": "application/orcid+json"},
    )
    work = resp.json()

    if work['citation'] is not None:
        bib_entry = work['citation']['citation-value']
        # Fix entry type: ORCID sometimes returns @article for conference papers
        if wtype in CONFERENCE_TYPES and bib_entry.startswith('@article{'):
            bib_entry = '@inproceedings{' + bib_entry[len('@article{'):]
    else:
        bib_entry = build_bibtex_from_metadata(work)
        print('BUILT from metadata: {}'.format(title[:60]))

    if wtype in JOURNAL_TYPES:
        journal_citations.append(bib_entry)
    else:
        conference_citations.append(bib_entry)

    print('OK ({}): {}'.format(wtype, title[:60]))

# Deduplicate and write
journal_citations = deduplicate_keys(journal_citations)
conference_citations = deduplicate_keys(conference_citations)

write_bib('journals.bib', journal_citations)
write_bib('conferences.bib', conference_citations)
