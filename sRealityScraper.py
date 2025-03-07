from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "https://www.sreality.cz/hledani/prodej/byty/praha?vlastnictvi=osobni"
# url = "https://www.sreality.cz/hledani/prodej/byty/praha?strana=2&vlastnictvi=osobni"
base_url = "https://www.sreality.cz"
page = urlopen(url)

html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# links = []

# for link in soup.findAll("a", class_="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineAlways css-1s6ohwi"):
#     links.append(base_url+link['href'])

#pages 2 to 164
pages = range(2,165)
urls = []
urls.append(url)
#go through the pages
for page in pages:
    next_page_url = "https://www.sreality.cz/hledani/prodej/byty/praha?strana="+str(page)+"&vlastnictvi=osobni"
    urls.append(next_page_url)

#all urls are strored here
print(urls)
