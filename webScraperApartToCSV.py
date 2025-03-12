from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv
import re

#loading link into code
apart_links_file = open("links2.txt",'r')
links = []
prefix = "https://www.sreality.cz/detail/prodej/byt/"

for i in range(3772):
    link = apart_links_file.readline()
    if link.startswith(prefix):
        links.append(link)
    
    #print("Status: ",i+1)

# print("links: ",len(links))
url = links[999]
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

def normalize(string):
    return string.replace('\u00E9', 'e').replace('\u011b', 'e').replace('\u00ED', 'i').replace('\u0161', 's').replace('\u00FD', 'y').replace('\u0159', 'r').replace('\u017E', 'z').replace('\u00E1', 'a').replace('\u010c', 'C').replace('\u010d', 'c').replace('\u0160', 'S')

print(url)
#PRICE METHOD
def get_price(soup):
    price_raw = soup.find("p", class_="MuiTypography-root MuiTypography-body1 css-1b1ajfd")
    price_text = price_raw.text.replace('\u200b', '').replace('\u010d', '').replace('K', '')
    price_clean = re.sub(r'[^\d.,]', '', price_text)
    price_int = int(price_clean)
    #print("price:",price_int)
    return price_int


#ROOMS METHOD
def get_rooms(url):
    return url.replace("https://www.sreality.cz/detail/prodej/byt/", "").split("/")[0]



#LOCATION METHOD
def get_location(url):
    parts = url.split("/")
    if parts[7].split("-")[1] == "dolni":
        location = parts[7].split("-")[1] +"_"+ parts[7].split("-")[2]
    if  parts[7].split("-")[1] == "horni":
        location = parts[7].split("-")[1] +"_"+ parts[7].split("-")[2]
    if  parts[7].split("-")[1] == "praha":
        location = parts[7].split("-")[1] +"_"+ parts[7].split("-")[2]
    else:
        location = parts[7].split("-")[1]

    return location


#SIZE METHOD
def get_size(soup):
    size_raw = soup.find("h1", class_="MuiTypography-root MuiTypography-body1 css-i4m05l")
    size_text = size_raw.text.replace('\u011b', '')
    size_clean = re.search(r'(\d+)\s*m²', size_text).group(1)
    size = int(size_clean)
    return size

#ENERGY-LEVEL METHOD
def get_energy_level(soup):
    energy_raw = soup.find("p", class_="MuiTypography-root MuiTypography-body1 css-sdwmvq")
    if energy_raw is not None:
        energy_text = energy_raw.text
    else:
        energy_text = None
    return energy_text


#FLOOR METHOD
def get_floor(soup):
    props = soup.find_all("dt", class_="MuiTypography-root MuiTypography-body1 css-hmrxrl")
    for prop in props:
        if prop.text == "Stavba:":
            floor_raw = prop.find_next_sibling("dd")
            floor_text = floor_raw.text
            floor_clean = re.search(r'\d+', floor_text).group()

    return int(floor_clean)      




#CONDITION METHOD
def get_condition(soup):
    conditions = ["Ve velmi dobrem stavu", "V dobrem stavu", "Ve spatnem stavu", "Ve vystavbe", "Projekt", "Novostavba", "K demolici", "Pred rekonstrukci", "Po rekonstrukci", "V rekonstrukci"]
    props = soup.find_all("dt", class_="MuiTypography-root MuiTypography-body1 css-hmrxrl")
    for prop in props:
        if prop.text == "Stavba:":
            condition_raw = prop.find_next_sibling("dd")
            condition_text = normalize(condition_raw.text)
            # print("condition text:", condition_text)
            columns = condition_text.split(",")
            for column in columns:
                column_clean = column.strip()
                if column_clean in conditions:
                    condition = column_clean
    return condition



#BUILD-TYPE METHOD
def get_build_type(soup):
    props = soup.find_all("dt", class_="MuiTypography-root MuiTypography-body1 css-hmrxrl")
    for prop in props:
        if prop.text == "Stavba:":
            build_type_raw = prop.find_next_sibling("dd")
            build_type_text = build_type_raw.text
            build_type_parts = [part.strip() for part in build_type_text.split(',')]
            if len(build_type_parts) > 1:
                build_type_clean = normalize(build_type_parts[0])
    return build_type_clean



#FEATURES METHOD
def get_features(soup):
    features = ["Balkon", "Lodzie","Zahrada", "Terasa", "Parkovaci stani", "Vytah", "Sklep", "Garaz", "Zarizeno", "Nearizeno", "Castecne zarizeno", "Bezbarierovy pristup"]
    features_result = []
    props = soup.find_all("div", class_="MuiBox-root css-1b7capf")
    for prop in props:
        feature_text = normalize(prop.text)
        # print("feature:", feature_text)
        for feature in features:
            if feature in feature_text:
                features_result.append(feature)
                break
    return features_result  


#PROXIMITY METHOD
def get_proximity(soup, place):
    props = soup.find_all("dt", class_="css-36xgvt")
    place_dist = None
    for prop in props:
        if normalize(prop.text.strip()) == place:
            place_raw = prop.find_next_sibling("dd")
            place_text = normalize(place_raw.text).replace('\xa0', ' ')
            place_clean = re.search(r'\(([\d\s]+) m\)', place_text).group(1).replace(" ", "")
            place_dist = int(place_clean)
            # print("place:", place)
    return place_dist


#testting unique room dispositions
rooms_unique = []
for link in links:
    # page = urlopen(link)
    # html = page.read().decode("utf-8")
    # soup = BeautifulSoup(html, "html.parser")
    rooms = get_rooms(link)
    if rooms not in rooms_unique:
        rooms_unique.append(rooms)

print(rooms_unique)








data = []
default_row = {price: 0,
               1+1: 0,
               '1+kk': 0,
               '2+1': 0,
               '2+kk': 0,
               '3+1': 0,
               '3+kk': 0,
               '4+1': 0,
               '4+kk': 0,
               '5+1': 0,
               '5+kk': 0,
               '6-a-vice': 0,
               'atypicky': 0,
               }
# data row test 
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
price = get_price(soup)
rooms = get_rooms(url)
location = get_location(url)
size = get_size(soup)
energy_level = get_energy_level(soup)
floor = get_floor(soup)
condition = get_condition(soup)
build_type = get_build_type(soup)
features = get_features(soup)
bus = get_proximity(soup, "Bus MHD:")
tram = get_proximity(soup, "Tram:")
metro = get_proximity(soup, "Metro:")
train = get_proximity(soup, "Vlak:")
school = get_proximity(soup, "Skola:")
kindergarden = get_proximity(soup, "Skolka:")
small_store = get_proximity(soup, "Vecerka:")
big_store = get_proximity(soup, "Obchod:")
pub = get_proximity(soup, "Hospoda:")
restaurant = get_proximity(soup, "Restaurace:")
post_office = get_proximity(soup, "Posta:")
atm = get_proximity(soup, "Bankomat:")
nature_place = get_proximity(soup, "Prirodni zajimavost:")
pharmacy = get_proximity(soup, "Lekarna:")
sports = get_proximity(soup, "Sportoviste:")
# print(price, rooms, location, size, energy_level, floor, condition, build_type, features, bus, tram, metro, train, school, kindergarden, small_store, big_store, pub, restaurant, post_office, atm, nature_place, pharmacy, sports)
