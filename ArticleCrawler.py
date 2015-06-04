
import json
from pattern.web import URL, DOM, plaintext

TARGET_URL = "http://apps.webofknowledge.com"
TARGET_query = "/full_record.do?product=UA&search_mode=GeneralSearch&qid=8&SID=P1xkMFYxAIRfFuaGs4Z&page=1&doc=1"
test_query = "/CitingArticles.do?product=WOS&REFID=22967726&SID=P1xkMFYxAIRfFuaGs4Z&search_mode=CitingArticles&parentProduct=UA&parentQid=8&parentDoc=1&excludeEventConfig=ExcludeIfFromFullRecPage"

def crawl(article):

    # article = list_of_article[-1]

    # temp_list = []
    # for url in cited_by(article[link_cited]):
        # make a dom
        # scrape 
        # place in temp_list
        # temp_list = temp_list + crawl(temp_list)

    # list_of_articles = list_of_articles + temp_list

    return list_of_articles

def cited_by(query):
    """
    """
    url = URL(TARGET_URL + query)
    print url
    html = url.download()


    # Parse the HTML file into a DOM representation
    dom = DOM(html)
    print dom
    
    list_of_querys = []
    for link in dom.by_class("smalV110"):
        #print link
        link = link.attrs.get("href", "")
        list_of_querys.append(link)

    return list_of_querys


def scrape_reference(dom):
    """
    
    """
    
    data_dict = {}

    # title
    article = dom
    title_parts = []
    for line in article.by_class("title"):
        for part in line.by_class("hitHilite"):
            article_name = plaintext(line.content.encode("ascii", "ignore"))

    data_dict.update({"title": article_name})

     
    # DOI
    doi = plaintext(article.by_tag("value")[5].content)
    data_dict.update({"doi": doi})

    # Cited link
    for link in article.by_attr(title="View all of the articles that cite this one"):
        link = link.attrs.get("href", "")
        data_dict.update({"link_cited": link})

    return data_dict


if __name__ == '__main__':
    # Download the HTML file of starting point

    url = URL(TARGET_URL + TARGET_query)
    html = url.download()

    # Parse the HTML file into a DOM representation
    dom = DOM(html)
    #print dom

    # scrape:
    first = scrape_reference(dom)

    # List of all articles
    list_of_articles = []
    list_of_articles = list_of_articles + crawl(first)

    # List of querys to crawl
    querys = cited_by(test_query)
    #print querys

    # parse and write to JSON
    out = json.dumps(first)
    f = open("Data.json", "w")
    f.write(out)