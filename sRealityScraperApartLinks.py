from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://www.sreality.cz/hledani/prodej/byty/praha?vlastnictvi=osobni"
# url = "https://www.sreality.cz/hledani/prodej/byty/praha?strana=2&vlastnictvi=osobni"
base_url = "https://www.sreality.cz"
page = urlopen(url)

html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

#pages 2 to 164
pages = range(2,165)
#all urls are strored here
urls = []
urls.append(url)
#go through the pages
for page in pages:
    next_page_url = "https://www.sreality.cz/hledani/prodej/byty/praha?strana="+str(page)+"&vlastnictvi=osobni"
    urls.append(next_page_url)
    print("page=",page)

#links for apartments
links = []

links_file = open("links.txt","a")

#cycle through all urls 
page_counter = 1
link_counter = 1
for url in urls:
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup2 = BeautifulSoup(html, "html.parser")
    #cycle through all links to apartments 
    for link in soup2.find_all("a", class_="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineAlways css-1s6ohwi"):
        links.append(base_url+link['href'])
        links_file.write(base_url+link['href']+'\n')
        print("page: ",page_counter,", link: ",link_counter)
        link_counter = link_counter + 1
    page_counter = page_counter + 1


print(len(links))
