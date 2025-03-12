from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import csv
import re

#loading link into code
apart_links_file = open("links3.txt",'r')
links = []
prefix = "https://www.sreality.cz/detail/prodej/byt/"

for i in range(3772):
    link = apart_links_file.readline()
    if link.startswith(prefix):
        links.append(link)
    
    #print("Status: ",i+1)

# print("links: ",len(links))
# url = links[999]
# page = urlopen(url)
# html = page.read().decode("utf-8")
# soup = BeautifulSoup(html, "html.parser")

def normalize(string):
    return string.replace('\u00E9', 'e').replace('\u011b', 'e').replace('\u00ED', 'i').replace('\u0161', 's').replace('\u00FD', 'y').replace('\u0159', 'r').replace('\u017E', 'z').replace('\u00E1', 'a').replace('\u010c', 'C').replace('\u010d', 'c').replace('\u0160', 'S')

# print(url)
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
        if parts[7].split("-")[2].isdigit(): 
            location = parts[7].split("-")[1] +"_"+ parts[7].split("-")[2]
        else:
            location = parts[7].split("-")[1]
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


# #testting unique room dispositions
# rooms_unique = []
# for link in links:
#     # page = urlopen(link)
#     # html = page.read().decode("utf-8")
#     # soup = BeautifulSoup(html, "html.parser")
#     rooms = get_rooms(link)
#     if rooms not in rooms_unique:
#         rooms_unique.append(rooms)

# # print(rooms_unique)

# #testing unique locations 
# location_unique = []
# for link in links:
#     # page = urlopen(link)
#     # html = page.read().decode("utf-8")
#     # soup = BeautifulSoup(html, "html.parser")
#     location = get_location(link)
#     if location not in location_unique:
#         location_unique.append(location)

# #testing unique build types
# build_type_unique = []
# counter = 0
# for link in links:
#     try:
#         page = urlopen(link)
#         html = page.read().decode("utf-8")
#         soup = BeautifulSoup(html, "html.parser")
#         build_type = get_build_type(soup)
#         counter += 1
#         print("counter: ", counter)
#         if build_type not in build_type_unique:
#             build_type_unique.append(build_type)
#             print(build_type_unique)
#     except HTTPError as e:
#         if e.code == 404:
#             print(f"404 Not Found: {link}")
#         else:
#             print(f"HTTP Error {e.code}: {link}")
#         continue
#     except Exception as e:
#         print(f"Error: {e}")
#         continue


# print(location_unique)
# conditions = ["Ve velmi dobrem stavu", "V dobrem stavu", "Ve spatnem stavu", "Ve vystavbe", "Projekt", "Novostavba", "K demolici", "Pred rekonstrukci", "Po rekonstrukci", "V rekonstrukci"]
# features = ["Balkon", "Lodzie","Zahrada", "Terasa", "Parkovaci stani", "Vytah", "Sklep", "Garaz", "Zarizeno", "Nearizeno", "Castecne zarizeno", "Bezbarierovy pristup"]
# for i in features:
#     print("'"+i+"'"+": 0,")




data = []
default_row = {'price': 0,
               '1+1': 0,
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
               'chodov': 0,
                'hlubocepy': 0,
                'smichov': 0,
                'vysocany': 0,
                'zizkov': 0,
                'vinohrady': 0,
                'modrany': 0,
                'nove': 0,
                'liben': 0,
                'vrsovice': 0,
                'cakovice': 0,
                'krc': 0,
                'nusle': 0,
                'praha': 0,
                'radlice': 0,
                'satalice': 0,
                'haje': 0,
                'horni': 0,
                'branik': 0,
                'holesovice': 0,
                'dolni': 0,
                'stodulky': 0,
                'mala': 0,
                'praha_1': 0,
                'kosire': 0,
                'troja': 0,
                'brevnov': 0,
                'praha_8': 0,
                'kyje': 0,
                'vysehrad': 0,
                'karlin': 0,
                'kbely': 0,
                'pitkovice': 0,
                'sobin': 0,
                'cerny': 0,
                'treboradice': 0,
                'cimice': 0,
                'strizkov': 0,
                'praha_9': 0,
                'letnany': 0,
                'kobylisy': 0,
                'dejvice': 0,
                'praha_14': 0,
                'bubenec': 0,
                'radotin': 0,
                'ujezd': 0,
                'suchdol': 0,
                'hostavice': 0,
                'praha_5': 0,
                'podoli': 0,
                'zlicin': 0,
                'veleslavin': 0,
                'michle': 0,
                'hostivar': 0,
                'strasnice': 0,
                'petrovice': 0,
                'praha_4': 0,
                'zbraslav': 0,
                'stare': 0,
                'bohnice': 0,
                'kolovraty': 0,
                'kamyk': 0,
                'trebonice': 0,
                'zabehlice': 0,
                'ruzyne': 0,
                'jinonice': 0,
                'malesice': 0,
                'motol': 0,
                'prosek': 0,
                'vokovice': 0,
                'repy': 0,
                'hloubetin': 0,
                'lochkov': 0,
                'lipence': 0,
                'liboc': 0,
                'josefov': 0,
                'hrdlorezy': 0,
                'slivenec': 0,
                'sterboholy': 0,
                'praha_7': 0,
                'hodkovicky': 0,
                'cholupice': 0,
                'miskovice': 0,
                'uhrineves': 0,
                'stresovice': 0,
                'dubec': 0,
                'lhotka': 0,
                'velka': 0,
                'pisnice': 0,
                'klanovice': 0,
                'dablice': 0,
                'vinor': 0,
                'holyne': 0,
                'praha_10': 0,
                'libus': 0,
                'hajek': 0,
                'praha_2': 0,
                'reporyje': 0,
                'seberov': 0,
                'bechovice': 0,
                'kolodeje': 0,
                'hradcany': 0,
                'praha_6': 0,
                'tocna': 0,
                'kralovice': 0,
                'kunratice': 0,
                'praha_11': 0,
                'dolni_brezany': 0,
                'size': 0,
                'energy_level': None,
                'floor': 0,
                'Ve velmi dobrem stavu': 0,
                'V dobrem stavu': 0,
                'Ve spatnem stavu': 0,
                'Ve vystavbe': 0,
                'Projekt': 0,
                'Novostavba': 0,
                'K demolici': 0,
                'Pred rekonstrukci': 0,
                'Po rekonstrukci': 0,
                'V rekonstrukci': 0,
                'Smisena': 0,
                'Panelova': 0,
                'Cihlova': 0,
                'Skeletova': 0,
                'Modularni': 0,
                'Kamenna': 0,
                'Drevostavba': 0,
                'Balkon': 0,
                'Lodzie': 0,
                'Zahrada': 0,
                'Terasa': 0,
                'Parkovaci stani': 0,
                'Vytah': 0,
                'Sklep': 0,
                'Garaz': 0,
                'Zarizeno': 0,
                'Nearizeno': 0,
                'Castecne zarizeno': 0,
                'Bezbarierovy pristup': 0,
                'bus': 0,
                'tram': 0,
                'metro': 0,
                'train': 0,
                'school': 0,
                'kindergarden': 0,
                'small_store': 0,
                'big_store': 0,
                'pub': 0,
                'restaurant': 0,
                'post_office': 0,
                'atm': 0,
                'nature_place': 0,
                'pharmacy': 0,
                'sports': 0
            }
# data row test

data.append(default_row) #data[0][feature]
url = links[0]
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

price = get_price(soup)
data[0]['price'] = price

rooms = get_rooms(url)
data[0][rooms] = 1

location = get_location(url)
data[0][location] = 1

size = get_size(soup)
data[0]['size'] = size

energy_level = get_energy_level(soup)
data[0]['energy_level'] = energy_level

floor = get_floor(soup)
data[0]['floor'] = floor

condition = get_condition(soup)
data[0][condition] = 1

build_type = get_build_type(soup)
data[0][build_type] = 1

features = get_features(soup)
for feature in features:
    data[0][feature] = 1

bus = get_proximity(soup, "Bus MHD:")
data[0]['bus'] = bus
tram = get_proximity(soup, "Tram:")
data[0]['tram'] = tram
metro = get_proximity(soup, "Metro:")
data[0]['metro'] = metro
train = get_proximity(soup, "Vlak:")
data[0]['train'] = train
school = get_proximity(soup, "Skola:")
data[0]['school'] = school
kindergarden = get_proximity(soup, "Skolka:")
data[0]['kindergarden'] = kindergarden
small_store = get_proximity(soup, "Vecerka:")
data[0]['small_store'] = small_store
big_store = get_proximity(soup, "Obchod:")
data[0]['big_store'] = big_store
pub = get_proximity(soup, "Hospoda:")
data[0]['pub'] = pub
restaurant = get_proximity(soup, "Restaurace:")
data[0]['restaurant'] = restaurant
post_office = get_proximity(soup, "Posta:")
data[0]['post_office'] = post_office
atm = get_proximity(soup, "Bankomat:")
data[0]['atm'] = atm
nature_place = get_proximity(soup, "Prirodni zajimavost:")
data[0]['nature_place'] = nature_place
pharmacy = get_proximity(soup, "Lekarna:")
data[0]['pharmacy'] = pharmacy
sports = get_proximity(soup, "Sportoviste:")
data[0]['sports'] = sports
# print(price, rooms, location, size, energy_level, floor, condition, build_type, features, bus, tram, metro, train, school, kindergarden, small_store, big_store, pub, restaurant, post_office, atm, nature_place, pharmacy, sports)
print(data[0])