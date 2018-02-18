#**********************************************************************************
#Sitemap V_0.1
#Python Version: 2.7
#By:Ben Bellerose
#Description: This crawls a given website to display a sitemap for SEO
#**********************************************************************************
import urllib
import datetime

#Gather all links from current site
def gather_links(index_url):
    url_list = []
    checked_list = []
    bad_link = []
    url_list.insert(0,index_url)
    url_count = True

    while url_count == True:
        curpage = urllib.urlopen(url_list[0])
        try:
            html = curpage.read()
            html_list = html.split("<")
            checked_list.insert(0,url_list[0])

            #Find all links on the webpage
            x = 0
            link_bank = []
            while x < len(html_list):
                if  "href" in html_list[x]:
                    if html_list[x][0] == "a":
                        html_hold = html_list[x].split(">")[0]
                        link_hold = html_hold.split('"')
                        b = 0
                        bank_hold = ''
                        while b < len(link_hold) - 1:
                            if "href=" in link_hold[b]:
                                if link_hold[b+1][0] == "/":
                                    link_bank.insert(0,link_hold[b+1])
                                    b = len(link_hold)
                            b = b + 1
                x = x + 1

            #Add links to url bank
            x = 0
            link_bank = list(set(link_bank))
            while x < len(link_bank):
                if len(link_bank[x]) == 1:
                    del link_bank[x]
                else:
                    link_bank[x] = link_bank[x].split('#')[0]
                    url_list.insert(len(url_list),index_url + link_bank[x])
                    x = x + 1

            #Delete current page from url list
            x = 0
            url_list = list(set(url_list))
            while x < len(url_list):
                if ("http" in url_list[x]) or ("https" in url_list[x]):
                    b = 0
                    while b < len(checked_list):
                        if url_list[x] == checked_list[b]:
                            del url_list[x]
                            x = x - 1
                            b = len(checked_list)
                        else:
                            b = b + 1
                    x = x + 1
                else:
                    del url_list[x]
        except:
            bad_link.insert(0,url_list[0])

        if len(url_list) == 0:
            url_count = False
            return list(checked_list), list(bad_link)

#Generate sitemap ".xml" file
def gen_sitemap(Links):
    start_time = datetime.datetime.now()
    sitemap = open("sitemap.xml","w")
    sitemap.write('<?xml version="1.0" encoding="UTF-8"?>')
    sitemap.write('\n')
    sitemap.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">')
    sitemap.write('\n')
    x = 0
    while x < len(Links):
        sitemap.write('\t<url>')
        sitemap.write('\n')
        sitemap.write('\t\t<loc>' + str(Links[x]) + '</loc>')
        sitemap.write('\n')
        sitemap.write('\t\t<lastmod>'+ str(start_time) +'</lastmod>')
        sitemap.write('\n')
        hold = Links[x].split("/")
        if x == 0 and len(hold) == 3:
            sitemap.write('\t\t<priority>1.00</priority>')
        elif len(hold) == 4:
            sitemap.write('\t\t<priority>0.80</priority>')
        else:
            sitemap.write('\t\t<priority>0.65</priority>')
        sitemap.write('\n')
        sitemap.write('\t</url>')
        sitemap.write('\n')
        x = x + 1
    sitemap.write('</urlset>')
    sitemap.close()
    pass

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    index_url = 'YOUR WEBSITE ADRESS'
    print("******Crawling website******")
    crawl_links = gather_links(index_url)
    site_links = sorted(crawl_links[0],key=len)
    bad_links = crawl_links[1]
    print("")
    print("***********Links************")
    x = 0
    while x < len(site_links):
        print(site_links[x])
        x = x + 1
    gen_sitemap(site_links)
    end_time = datetime.datetime.now()
    print("")
    print("Total Links = " + str(len(site_links)))
    print("Bad Links = " + str(len(bad_links)))
    print("Total Time = " + str(end_time - start_time))
