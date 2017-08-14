from gat.scraper import url_parser


def scrape(url):
    if url != None and url.strip() != "":
        return url_parser.write_articles([url.strip()])
    return None
