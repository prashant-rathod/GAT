from newspaper import Article
import codecs


# def gather_urls(news_sites):

def url_reader(url):
    article = Article(url)
    article.download()
    article.parse()
    title = article.title
    authors = article.authors
    date = article.publish_date
    text = article.text
    # can also include things like article images, and attached videos
    # article.nlp()
    # keywords = article.keywords
    # summary = article.summary
    print("The article: {} is downloaded and parsed".format(title))
    return title, authors, date, text  # keywords , summary


def text_writer(title="No Title Given", authors="No Authors Given", date="No Date Given", text="No Text Given"):
    def newline():
        f.write("\n")

    print("Writing Text File")
    f = codecs.open("out/nlp/scrapedArticles/" + reformat_title(title) + ".txt", "w", encoding="utf8")
    f.write(title + "\n")
    newline()
    for author in authors:
        f.write(author + "\n")
    newline()
    f.write(reformat_date(date) + "\n")
    newline()
    for sentence in separate_text(text):
        f.write(sentence + "\n")
    newline()
    f.close()
    print("Text Written \n")


def separate_text(text):
    punctuation = ".?!"
    sentences = []
    sentence = ""
    for ch in text:
        sentence += ch
        if ch in punctuation:
            sentences.append(sentence)
            sentence = ""
    sentences = preserve_order_duplicate_remove(sentences)
    return sentences


def preserve_order_duplicate_remove(sentences):
    seen = set()
    seen_add = seen.add
    return [x for x in sentences if not (x in seen or seen_add(x))]


def reformat_date(datetime):
    if datetime == None:
        return "No Date Given"
    months = {"01": "January",
              "02": "February",
              "03": "March",
              "04": "April",
              "05": "May",
              "06": "June",
              "07": "July",
              "08": "August",
              "09": "September",
              "10": "October",
              "11": "November",
              "12": "December"}
    date = ""
    t = datetime.strftime('%m/%d/%Y')
    parts = t.split("/")
    date += parts[1] + " "
    date += months.get(parts[0]) + " "
    date += parts[2]
    return date


def reformat_title(title):
    new_title = ""
    for ch in title:
        if ch == " ":
            new_title += "_"
        else:
            new_title += ch
    return new_title


def write_articles(urls):
    articles = []
    for url in urls:
        title, authors, date, text = url_reader(url)
        articles = [title, authors, date, text]
        text_writer(title, authors, date, text)
    return articles


if __name__ == "__main__":
    urls = ['http://www.reuters.com/article/us-mideast-crisis-iraq-mosul-idUSKBN13W1H1',
            'http://217.218.67.231/Detail/2015/07/27/422086/iran-iraq-power-plant-basra-mapna-gas-',
            'http://theiranproject.com/blog/2016/02/18/industry-minister-attends-irans-second-exclusive-fair-in-baghdad/',
            'http://theiranproject.com/blog/2014/10/26/iran-to-export-water-electricity-to-iraq/',
            'http://www.janes.com/article/65950/law-legalising-iraq-s-hashd-al-shaabi-assures-militias-funding-and-facilitates-political-engagement-but-hinders-country-s-reconciliation-project']
    print(write_articles(urls))
