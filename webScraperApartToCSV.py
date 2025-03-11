from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import re

#loading link into code
apart_links_file = open("links.txt",'r')
links = []
prefix = "https://www.sreality.cz/detail/prodej/byt/"

for i in range(3772):
    link = apart_links_file.readline()
    if link.startswith(prefix):
        links.append(link)
    
    #print("Status: ",i+1)

# print("links: ",len(links))
url = links[1]
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

print(url)

#PRICE SCRIPT
price_raw = soup.find("p", class_="MuiTypography-root MuiTypography-body1 css-1b1ajfd")
price_text = price_raw.text.replace('\u200b', '').replace('\u010d', '').replace('K', '')
price_clean = re.sub(r'[^\d.,]', '', price_text)
price_int = int(price_clean)
print(price_int)

#ROOMS SCRIPT
url_copy_rooms = url
rooms_clean = url_copy_rooms.replace("https://www.sreality.cz/detail/prodej/byt/", "").split("/")[0]
print(rooms_clean)

#LOCATION SCRIPT
url_copy_location = url
parts = url_copy_location.split("/")
if parts[7].split("-")[1] == "dolni":
    location = parts[7].split("-")[1] +"_"+ parts[7].split("-")[2]
if  parts[7].split("-")[1] == "horni":
    location = parts[7].split("-")[1] +"_"+ parts[7].split("-")[2]
if  parts[7].split("-")[1] == "praha":
    location = parts[7].split("-")[1] +"_"+ parts[7].split("-")[2]
else:
    location = parts[7].split("-")[1]

print(location)

#SIZE SCRIPT
size_raw = soup.find("h1", class_="MuiTypography-root MuiTypography-body1 css-i4m05l")
size_text = size_raw.text.replace('\u011b', '')
size_clean = re.search(r'(\d+)\s*m²', size_text).group(1)
size = int(size_clean)
print(size)

#ENERGY-LEVEL SCRIPT
energy_raw = soup.find("p", class_="MuiTypography-root MuiTypography-body1 css-sdwmvq")
energy_text = energy_raw.text
print(energy_text)

#looping through links and extracting data
# data = []
# status_counter = 1
# for link in links:
#     url = link
#     page = urlopen(url)
#     html = page.read().decode("utf-8")
#     soup = BeautifulSoup(html, "html.parser")
    
#     price_raw = soup.find_all("p", class_="MuiTypography-root MuiTypography-body1 css-1b1ajfd")
    