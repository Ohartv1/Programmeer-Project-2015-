
import json, time, unicodedata, socket
from pattern.web import URL, DOM, plaintext
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

TARGET = "http://apps.webofknowledge.com"
SEARCH_FOR = "The Nature-Nurture Debates: 25 Years of Challenges in Understanding the Psychology of Gender"
temp = "Determinants and mechanisms in ego identity development: A review and synthesis"

generation = 0

def crawl(browser, article, generation):
    generation = generation + 1

    master_article = article

    list_of_articles = []
    list_of_citations = []

    if article.get("link_cited") != None:

        iteration = 0

        for each in cited_by(browser, article.get("link_cited")):
            # print "generation:", generation, "iteration:", iteration
            iteration = iteration + 1

            if each == None:
                print "break, no citations"
                break
            try:          
                # Download the HTML file of starting point
                url = URL(each)
                html = url.download()

                # Parse the HTML file into a DOM representation
                dom = DOM(html)
                current = scrape_reference(dom)
                

                list_of_citations.append(current.get("title"))

                if current.get("link_cited") != None:
                    if len(list_of_articles) == 0:
                        print list_of_articles
                        list_of_articles = crawl(browser, current, generation)
                    else:
                        list_of_articles = list_of_articles + crawl(browser, current, generation)
                        print len(list_of_articles)

            except pattern.web.URLTimeout:
                print "break at pattern.web.URLTimeout"
                break
        master_article.update({"cited_by": list_of_citations, "generation": generation})
        list_of_articles.append(master_article)
    
    return list_of_articles
    

def cited_by(browser, url):
    """
    """
    list_of_urls = []

    try:
        browser.get(url)
        page_bottom = browser.find_element_by_id("pageCount.bottom").text
    except socket.timeout as e:
        try:
            print "timeout error"
            print "url at the time of error:", url
            time.sleep(60)
            browser.get(url)
            socket.setdefaulttimeout(60)
            page_bottom = browser.find_element_by_id("pageCount.bottom").text
        except:
            print "exception unkown"
            return list_of_urls



    while True:

        links = browser.find_elements_by_class_name('smallV110')

        iterations = len(links) / 2
        while iterations > 0:
            links.pop()
            iterations = iterations - 1


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
        article_name = plaintext(line.content.encode("ascii", "ignore"))
        data_dict.update({"title": article_name})

    # authors
    author_list = []
    for author in dom.by_attr(title="Find more records by this author"):
        author = plaintext(author.content.encode("ascii", "ignore"))
        author_list.append(author)
    data_dict.update({"authors": author_list})


    # DOI
    doi = plaintext(dom.by_tag("value")[5].content)
    data_dict.update({"doi": doi})

    # Cited link
    for link in dom.by_attr(title="View all of the articles that cite this one"):
        link = link.attrs.get("href", "")
        data_dict.update({"link_cited": TARGET + link})


    return data_dict


if __name__ == '__main__':
    # create webbrowser
    browser = webdriver.Firefox()

    START_URL = give_start(browser, TARGET, SEARCH_FOR)

    # Download the HTML file of starting point
    url = URL(START_URL)
    html = url.download()

    # Parse the HTML file into a DOM representation
    dom = DOM(html)

    # scrape:
    first = scrape_reference(dom)

    # List of all article
    list_of_articles = crawl(browser, first, generation)

    browser.close()

    # # parse and write to JSON
    with open("Data.json", "a") as outfile:
        json.dump(list_of_articles, outfile, indent=2)