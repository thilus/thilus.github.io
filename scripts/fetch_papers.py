import json
from scholarly import scholarly

# Google Scholar user ID
user_id = "xe3MHscAAAAJ"

def fetch_publications(user_id):
    search_query = scholarly.search_author_id(user_id)
    author = scholarly.fill(search_query)
    publications = author.get('publications', [])
    paper_list = []
    for pub in publications:
        # Fill publication details
        pub_filled = scholarly.fill(pub)
        bib = pub_filled.get('bib', {})
        title = bib.get('title', 'No Title')
        authors = bib.get('author', 'Unknown Authors')
        journal = bib.get('journal', 'Unknown Journal')
        # Try both keys for year
        year = bib.get('pub_year', bib.get('year', '0'))
        paper_list.append({
            'title': title,
            'authors': authors,
            'journal': journal,
            'year': year
        })
        print(title)
    # Sort papers: convert year to int if possible, defaulting to 0 if conversion fails
    def year_key(p):
        try:
            return int(p['year'])
        except ValueError:
            return 0
    paper_list = sorted(paper_list, key=year_key, reverse=True)
    return paper_list

if __name__ == "__main__":
    papers = fetch_publications(user_id)
    # Group papers by year
    groups = {}
    for paper in papers:
        groups.setdefault(paper['year'], []).append(paper)
    years = sorted(groups.keys(), key=lambda y: int(y) if y.isdigit() else 0, reverse=True)
    
    # Output as markdown with groups and publication counters
    with open("../publications.md", "w", encoding="utf-8") as f:
        f.write("# Publications\n\n")
        for year in years:
            group = groups[year]
            count = len(group)
            f.write(f"## [{year}] ({count} publication{'s' if count > 1 else ''})\n\n")
            for idx, paper in enumerate(group, start=1):
                f.write(f"{idx}. [{paper['year']}] {paper['title']}\n")
                f.write(f"   - Journal: {paper['journal']}\n")
                f.write(f"   - Authors: {paper['authors']}\n\n")
    print("Publications list has been generated in publications.md")
