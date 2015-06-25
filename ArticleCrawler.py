    # Onno Hartveldt
    # 10972935

    # visualisation:
    # "Wie zijn de nakomelingen van een wetenschappelijke publicatie?"

import json, time, unicodedata, socket
from pattern.web import URL, DOM, plaintext
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

TARGET = "http://apps.webofknowledge.com"
SEARCH_FOR = "The Nature-Nurture Debates: 25 Years of Challenges in Understanding the Psychology of Gender"

generation = 0
archief = []


def give_start(browser, website, string_for_search):
    """
    The start of the scraping algoritm. This function give the first
    input in the website. 

    Input: the browser object, the website url, and a search element. 
    Output: a url to a sub page with article information

    """

    browser.get(website)

    # search for 
    elem = browser.find_element_by_id("value(input1)")
    elem.send_keys(string_for_search)
    elem.send_keys(Keys.RETURN)
    
    # get link of the respons
    link = browser.find_element_by_class_name("smallV110")
    href = link.get_attribute("href")
    
    return href


def scrape_reference(dom):
    """
    Collect information of given article.

    Input: a dom element for one article
    OUtput: a dictionary with information of a article, like the
    title, authors, doi, data of publication, and an link to all cited by.
    
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


    # # DOI
    # doi = plaintext(dom.by_tag("value")[5].content)
    # data_dict.update({"doi": doi})

    # # Date
    # datum = plaintext(dom.by_tag("value")[6].content)
    # data_dict.update({"date": datum})

    # Cited link
    for link in dom.by_attr(title="View all of the articles that cite this one"):
        link = link.attrs.get("href", "")
        data_dict.update({"link_cited": TARGET + link})

    return data_dict


def cited_by(browser, url):
    """
    Walks through all pages of articles and makes a list of the url's

    Input: the browser element and a url to a javaScript generated list of
    all cited by articles.
    Output: een list of url's to all individual cited by articles.
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

        # get rid of doubles
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


def crawl(browser, article, generation):
    """
    A recursive funcion with a base when it gets no url of cited by articles.

    Input: the browser, one article as dictionary, the generation counter
    Output: a list of article dictionaries
    """

    generation = generation + 1

    master_article = article

    list_of_articles = []
    list_of_citations = []

    if not master_article.get("title") in archief:
        iteration = 0

        for each in cited_by(browser, article.get("link_cited")):

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

                archief.append(current.get("title"))

            except pattern.web.URLTimeout:
                print "break at pattern.web.URLTimeout"
                break

        master_article.update({"cited_by": list_of_citations, "generation": generation})
        list_of_articles.append(master_article)
    
    return list_of_articles
    

def data_to_connections(data):
    """ 
    Changes the output of the crawler to the right json file needed
    for the visualisation.

    input: a list of dictionary with articles
    output: a dictionary with a list of nodes and a list of links
    """

    list_nodes = []
    list_titles = []
    for dic in data:
        list_titles.append(dic.get("title"))
        dict_nut = {}
        dict_nut.update({"name": dic.get("title"), \
            "num_cit": len(dic.get("cited_by")), \
            "generation": dic.get("generation"), \
            "date": dic.get("date")})
        list_nodes.append(dict_nut)

    for dic in data:
        for cit in dic.get("cited_by"):
            if not cit in list_titles:
                dict_nut = {}
                dict_nut.update({"name": cit, \
                    "num_cit": 0, \
                    "generation": dic.get("generation") + 1})
                list_nodes.append(dict_nut)
                list_titles.append(cit)

    list_connections = []
    for each in data:
        for every in each.get("cited_by"):
            new_dict = {}
            temp = each.get("title")
            new_dict.update({"source": list_titles.index(temp), \
                "target": list_titles.index(every)})
            list_connections.append(new_dict)

    final_connections = []
    for iets in list_connections:
        if not iets in final_connections:
            final_connections.append(iets)

    return_dict = {}
    return_dict.update({"nodes": list_nodes})
    return_dict.update({"links": list_connections})

    return return_dict



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
    if first.get("link_cited") != None:
        list_of_articles = crawl(browser, first, generation)

    browser.close()

    # transform list of articles to right format for visualisation
    output = data_to_connections(list_of_articles)

    # # parse and write to JSON
    with open("graph.json", "a") as outfile:
        json.dump(output, outfile, indent=2)