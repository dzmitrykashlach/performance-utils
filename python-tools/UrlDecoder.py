import sys
import urllib.parse
import regex

OUTPUT_DIRECTORY: str = r'output/'
SEARCH_TERMS: str = r'search-terms-swa-prod-06.2021.txt'

configuration_path: str = sys.argv[1] if len(sys.argv) > 1 else r'search-terms-swa-prod-06.2021-src.csv.'
decoded_search_terms = []
with open(configuration_path) as params:
    search_queries = params.read().splitlines()
    for q in search_queries:
        decoded_search_term = regex.findall(r"queryString=(.+)", urllib.parse.unquote(q))
        if decoded_search_term not in decoded_search_terms:
            decoded_search_terms.append(decoded_search_term)
with open(OUTPUT_DIRECTORY + SEARCH_TERMS, 'w+', encoding="utf-8") as f:
    for term in decoded_search_terms:
        f.write(" ".join(term)+"\n")
print('READY')

