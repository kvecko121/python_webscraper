from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "http://olympus.realpython.org/profiles/dionysus"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
# print(soup.get_text())
image1, image2 = soup.find_all("img")
# print(image2["src"])
# f = open("sreality_home_source.txt", "w")
# f.write(soup.string)
# print(soup.string)
print(image1.name)
print(image1['src'])
print(soup.title.string)
print(soup.find_all("img", src="/static/dionysus.jpg"))

#exercise
base_url = "http://olympus.realpython.org"
extra = "/profiles"
page = urlopen(base_url + extra)
html = page.read().decode("utf-8")
soup2 = BeautifulSoup(html, "html.parser")
#print(str(soup2))
for link in soup2.find_all("a"):
    link_url = base_url + link['href']
    print(link_url)

# link1, link2, link3 = soup2.find_all("a")
# print(link1['href'] ,"\n",link2['href'],"\n",link3['href'])

