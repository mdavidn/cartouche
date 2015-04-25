from lxml import etree, html
from multiprocessing.dummy import Pool
import requests
import re

# Match words in English text. Attempt to preserve punctuation in abbreviations
# and concatenations, such as "Ph.D." and "don't" respectively.
WORDS = re.compile(r"\w+(?:\.\w+\.?)*(?:'\w+)*")
api_url = "http://kol.coldfront.net/thekolwiki/api.php"


def itermwpages():
    """Yield all pages on a MediaWiki site."""
    query = {"format": "xml",
             "action": "query",
             "list": "allpages",
             "aplimit": 100}
    while True:
        resp = requests.get(api_url, params=query)
        root = etree.fromstring(resp.content)
        for p in root.iterfind("query/allpages/p"):
            yield p.get("title")
        cont = root.find("query-continue/allpages")
        if cont is not None:
            query["apcontinue"] = cont.get("apcontinue")
        else:
            break


def mwpage(title):
    """Return title and HTML of a MediaWiki page."""
    query = {"format": "xml",
             "action": "parse",
             "prop": "text",
             "page": title}
    resp = requests.get(api_url, params=query)
    root = etree.fromstring(resp.content)
    el = root.find("parse/text")
    return "" if el is None else el.text


def htmltext(markup):
    """Return all text in HTML."""
    return html.document_fromstring(markup).text_content()


def iterwords(text):
    return (m.group(0).lower() for m in WORDS.finditer(text))


def crawl_page(title):
    words = set()
    words.update(iterwords(title))
    words.update(iterwords(htmltext(mwpage(title))))
    return words


def crawl_site():
    all_words = set()
    for words in Pool(6).imap_unordered(crawl_page, itermwpages()):
        all_words.update(words)
    return all_words


if __name__ == "__main__":
    for w in sorted(crawl_site()):
        print(w)
