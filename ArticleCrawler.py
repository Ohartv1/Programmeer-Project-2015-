
import json, time, unicodedata
from pattern.web import URL, DOM, plaintext
from selenium import webdriver
from selenium.webdriver.common.keys import Keys










TARGET = "http://apps.webofknowledge.com"

def crawl(browser, article):

    # temp_list = []
    # for url in cited_by(browser, first.get("link_cited")):
        # make a dom
        # scrape 
        # place in temp_list
        # temp_list = temp_list + crawl(temp_list)

    # list_of_articles = list_of_articles + temp_list

    
    list_of_articles = []
    for each in cited_by(browser, article.get("link_cited")):
        # Download the HTML file of starting point
        url = URL(each)
        html = url.download()

        # Parse the HTML file into a DOM representation
        dom = DOM(html)
        current = scrape_reference(dom)

        list_of_articles.append(current)

        temp_list = list_of_articles + crawl(browser, current)




    return list_of_articles
    

def cited_by(browser, url):
    """
    """
    browser.get(url)
    content = browser.page_source
    page_bottom = browser.find_element_by_id("pageCount.bottom").text


    list_of_urls = []

    while True:
        links = browser.find_elements_by_class_name('smallV110')

        for link in links:  
            href = link.get_attribute("href")
            list_of_urls.append(href)

        stop = browser.find_element_by_class_name("goToPageNumber-input")
        stop = stop.get_attribute("value")

        if stop == page_bottom:
            break

        browser.find_element_by_class_name("paginationNext").click()

    return list_of_urls

def give_start(browser, website, string_for_search):
    browser.get(website)
    elem = browser.find_element_by_id("value(input1)")
    elem.send_keys(string_for_search)
    elem.send_keys(Keys.RETURN)
    link = browser.find_element_by_class_name("smallV110")
    href = link.get_attribute("href")
    return href


def scrape_reference(dom):
    """
    
    """
    
    data_dict = {}

    # title
    for line in dom.by_class("title"):
        for part in line.by_class("hitHilite"):
            article_name = plaintext(line.content.encode("ascii", "ignore"))
            data_dict.update({"title": article_name})

     
        # DOI
        doi = plaintext(dom.by_tag("value")[5].content)
        data_dict.update({"doi": doi})

    # Cited link
    for link in dom.by_attr(title="View all of the articles that cite this one"):
        link = link.attrs.get("href", "")
        data_dict.update({"link_cited": TARGET + link})



    print data_dict
    return data_dict


if __name__ == '__main__':
    # create webbrowser
    browser = webdriver.Firefox()

    START_URL = give_start(browser, TARGET, "Determinants and mechanisms in ego identity development: A review and synthesis")

    # Download the HTML file of starting point
    url = URL(START_URL)
    html = url.download()

    # Parse the HTML file into a DOM representation
    dom = DOM(html)

    # scrape:
    first = scrape_reference(dom)

    # List of all articles
    list_of_articles = []
    list_of_articles = list_of_articles + crawl(browser, first)

    browser.close()

    # parse and write to JSON
    out = json.dumps(list_of_articles)
    f = open("Data.json", "w")
    f.write(out)