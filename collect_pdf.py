from BeautifulSoup import BeautifulSoup as bs 
import urllib2 as ul2
import re

import os

lib      = "./lib/"
webpages = ["http://www.aeplan.unicamp.br/"]

def main():
    for wp in webpages:
        html_p = ul2.urlopen(wp)
        soup   = bs(html_p)

        # find all links in the website
        find_pages(wp, soup)

def find_pages(wp, soup):
    # find all the pdfs in the website
    get_pdf(wp, soup)

    # find all the links in the website
    for link in soup.findAll('a', attrs={'href': re.compile(".php$")}):
        link_str = ''.join([wp, link.get('href')])

        # if it is a valid url
        if not re.search('\.\.', link_str):
            try:
                url = ul2.urlopen(link_str)
            except ul2.HTTPError:
                break

            l_html = bs(url)

            find_pages(link_str, l_html)

def get_pdf(wp, soup):
    # start count of current directory
    count = 0

    # get appropriate parent link
    base_wp = ''.join([wp[0:wp.rfind('/')], '/'])

    # create directory
    path = ''.join([lib, '/', wp.replace("/", "*"), '/'])

    # does it already exists?
    if not os.path.exists(path):
        os.makedirs(path)

    # find pdfs!
    for link in soup.findAll('a', attrs={'href': re.compile(".pdf$")}):
        url = ''.join([base_wp, link.get('href')])

        download(path, url, count)
        count += 1

def download(path, link, no):
    try:
        # open link
        rs = ul2.urlopen(link)
    except ul2.HTTPError:
        return
    except ul2.URLError:
        return

    # get filename
    filename = ''.join([path, str(no), '.pdf'])

    with open(filename, 'w+') as tmp:
        tmp.write(rs.read())

if __name__ == "__main__":
    main()