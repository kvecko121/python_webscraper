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

#PRICE SCRIPT
# price_raw = soup.find("p", class_="MuiTypography-root MuiTypography-body1 css-1b1ajfd")
# price_text = price_raw.text.replace('\u200b', '').replace('\u010d', '').replace('K', '')
# price_clean = re.sub(r'[^\d.,]', '', price_text)
# price_int = int(price_clean)
#print("price:",price_int)

#ROOMS METHOD
def get_rooms(url):
    return url.replace("https://www.sreality.cz/detail/prodej/byt/", "").split("/")[0]

#ROOMS SCRIPT
# url_copy_rooms = url
# rooms_clean = url_copy_rooms.replace("https://www.sreality.cz/detail/prodej/byt/", "").split("/")[0]
# print("rooms:",rooms_clean)

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

#LOCATION SCRIPT
# url_copy_location = url
# parts = url_copy_location.split("/")
# if parts[7].split("-")[1] == "dolni":
#     location = parts[7].split("-")[1] +"_"+ parts[7].split("-")[2]
# if  parts[7].split("-")[1] == "horni":
#     location = parts[7].split("-")[1] +"_"+ parts[7].split("-")[2]
# if  parts[7].split("-")[1] == "praha":
#     location = parts[7].split("-")[1] +"_"+ parts[7].split("-")[2]
# else:
#     location = parts[7].split("-")[1]

# print("location:",location)

#SIZE METHOD
def get_size(soup):
    size_raw = soup.find("h1", class_="MuiTypography-root MuiTypography-body1 css-i4m05l")
    size_text = size_raw.text.replace('\u011b', '')
    size_clean = re.search(r'(\d+)\s*m²', size_text).group(1)
    size = int(size_clean)
    return size

#SIZE SCRIPT
# size_raw = soup.find("h1", class_="MuiTypography-root MuiTypography-body1 css-i4m05l")
# size_text = size_raw.text.replace('\u011b', '')
# size_clean = re.search(r'(\d+)\s*m²', size_text).group(1)
# size = int(size_clean)
# print("size:",size)

#ENERGY-LEVEL METHOD
def get_energy_level(soup):
    energy_raw = soup.find("p", class_="MuiTypography-root MuiTypography-body1 css-sdwmvq")
    if energy_raw is not None:
        energy_text = energy_raw.text
    else:
        energy_text = None
    return energy_text

#ENERGY-LEVEL SCRIPT
# energy_raw = soup.find("p", class_="MuiTypography-root MuiTypography-body1 css-sdwmvq")
# if energy_raw is not None:
#     energy_text = energy_raw.text
# else:
#     energy_text = None
# print("energy level:",energy_text)

#FLOOR METHOD
def get_floor(soup):
    props = soup.find_all("dt", class_="MuiTypography-root MuiTypography-body1 css-hmrxrl")
    for prop in props:
        if prop.text == "Stavba:":
            floor_raw = prop.find_next_sibling("dd")
            floor_text = floor_raw.text
            floor_clean = re.search(r'\d+', floor_text).group()

    return int(floor_clean)      


#FLOOR SCRIPT
# props = soup.find_all("dt", class_="MuiTypography-root MuiTypography-body1 css-hmrxrl")
# for prop in props:
#     if prop.text == "Stavba:":
#         floor_raw = prop.find_next_sibling("dd")
#         floor_text = floor_raw.text
#         floor_clean = re.search(r'\d+', floor_text).group()
#         print("floor:",floor_clean)

#FLOOR-TOTAL SCRIPT
# props = soup.find_all("dt", class_="MuiTypography-root MuiTypography-body1 css-hmrxrl")
# for prop in props:
#     if prop.text == "Stavba:":
#         floor_tot_raw = prop.find_next_sibling("dd")
#         floor_tot_text = floor_tot_raw.text
#         floor_tot_clean = re.search(r'z\s*(\d+)', floor_tot_text).group(1)
#         print("total floors:",floor_tot_clean)

#CONDITION SCRIPT
# props = soup.find_all("dt", class_="MuiTypography-root MuiTypography-body1 css-hmrxrl")
# for prop in props:
#     if prop.text == "Stavba:":
#         condition_raw = prop.find_next_sibling("dd")
#         condition_text = condition_raw.text
#         condition_parts = [part.strip() for part in condition_text.split(',')]
#         if len(condition_parts) > 1:
#             condition_clean = condition_parts[1].replace('\u00E9', 'e').replace('\u011b', 'e').replace('\u00ED', 'i').replace('\u0161', 's').replace('\u00FD', 'y')
#             print("condition:", condition_clean)

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


#CONDITION SCRIPT 2
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
                print("condition:", condition)

#BUILD-TYPE SCRIPT
props = soup.find_all("dt", class_="MuiTypography-root MuiTypography-body1 css-hmrxrl")
for prop in props:
    if prop.text == "Stavba:":
        build_type_raw = prop.find_next_sibling("dd")
        build_type_text = build_type_raw.text
        build_type_parts = [part.strip() for part in build_type_text.split(',')]
        if len(build_type_parts) > 1:
            build_type_clean = build_type_parts[0].replace('\u00E1', 'a').replace('\u011b', 'e').replace('\u00ED', 'i').replace('\u0161', 's').replace('\u00FD', 'y')
            print("build_type:", build_type_clean)

#FEATURES SCRIPT
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
print("features:",features_result)  

#PROXIMITY SCRIPT (css-36xgvt)
props = soup.find_all("dt", class_="css-36xgvt")
#BUS 
for prop in props:
    if normalize(prop.text.strip()) == "Bus MHD:":
        bus_raw = prop.find_next_sibling("dd")
        bus_text = normalize(bus_raw.text).replace('\xa0', ' ')
        bus_clean = re.search(r'\(([\d\s]+) m\)', bus_text).group(1).replace(" ", "")
        bus = int(bus_clean)
        print("bus:", bus)

#Tram 
for prop in props:
    if normalize(prop.text.strip()) == "Tram:":
        tram_raw = prop.find_next_sibling("dd")
        tram_text = normalize(tram_raw.text).replace('\xa0', ' ')
        tram_clean = re.search(r'\(([\d\s]+) m\)', tram_text).group(1).replace(" ", "")
        tram = int(tram_clean)
        print("tram:", tram)

#Metro 
for prop in props:
    if normalize(prop.text.strip()) == "Metro:":
        metro_raw = prop.find_next_sibling("dd")
        metro_text = normalize(metro_raw.text).replace('\xa0', ' ')
        metro_clean = re.search(r'\(([\d\s]+) m\)', metro_text).group(1).replace(" ", "")
        metro = int(metro_clean)
        print("metro:", metro)

#Train 
for prop in props:
    if normalize(prop.text.strip()) == "Vlak:":
        train_raw = prop.find_next_sibling("dd")
        train_text = normalize(train_raw.text).replace('\xa0', ' ')
        train_clean = re.search(r'\(([\d\s]+) m\)', train_text).group(1).replace(" ", "")
        train = int(train_clean)
        print("train:", train)

#school 
for prop in props:
    if normalize(prop.text.strip()) == "Skola:":
        school_raw = prop.find_next_sibling("dd")
        school_text = normalize(school_raw.text).replace('\xa0', ' ')
        school_clean = re.search(r'\(([\d\s]+) m\)', school_text).group(1).replace(" ", "")
        school = int(school_clean)
        print("school:", school)

#kindergarden 
for prop in props:
    if normalize(prop.text.strip()) == "Skolka:":
        kindergarden_raw = prop.find_next_sibling("dd")
        kindergarden_text = normalize(kindergarden_raw.text).replace('\xa0', ' ')
        kindergarden_clean = re.search(r'\(([\d\s]+) m\)', kindergarden_text).group(1).replace(" ", "")
        kindergarden = int(kindergarden_clean)
        print("kindergarden:", kindergarden)
#small_store 
for prop in props:
    if normalize(prop.text.strip()) == "Vecerka:":
        small_store_raw = prop.find_next_sibling("dd")
        small_store_text = normalize(small_store_raw.text).replace('\xa0', ' ')
        small_store_clean = re.search(r'\(([\d\s]+) m\)', small_store_text).group(1).replace(" ", "")
        small_store = int(small_store_clean)
        print("small_store:", small_store)
#big_store 
for prop in props:
    if normalize(prop.text.strip()) == "Obchod:":
        big_store_raw = prop.find_next_sibling("dd")
        big_store_text = normalize(big_store_raw.text).replace('\xa0', ' ')
        big_store_clean = re.search(r'\(([\d\s]+) m\)', big_store_text).group(1).replace(" ", "")
        big_store = int(big_store_clean)
        print("big_store:", big_store)

#pub 
for prop in props:
    if normalize(prop.text.strip()) == "Hospoda:":
        pub_raw = prop.find_next_sibling("dd")
        pub_text = normalize(pub_raw.text).replace('\xa0', ' ')
        pub_clean = re.search(r'\(([\d\s]+) m\)', pub_text).group(1).replace(" ", "")
        pub = int(pub_clean)
        print("pub:", pub)

#restaurant 
for prop in props:
    if normalize(prop.text.strip()) == "Restaurace:":
        restaurant_raw = prop.find_next_sibling("dd")
        restaurant_text = normalize(restaurant_raw.text).replace('\xa0', ' ')
        restaurant_clean = re.search(r'\(([\d\s]+) m\)', restaurant_text).group(1).replace(" ", "")
        restaurant = int(restaurant_clean)
        print("restaurant:", restaurant)

#post_office 
for prop in props:
    if normalize(prop.text.strip()) == "Posta:":
        post_office_raw = prop.find_next_sibling("dd")
        post_office_text = normalize(post_office_raw.text).replace('\xa0', ' ')
        post_office_clean = re.search(r'\(([\d\s]+) m\)', post_office_text).group(1).replace(" ", "")
        post_office = int(post_office_clean)
        print("post_office:", post_office)

#atm 
for prop in props:
    if normalize(prop.text.strip()) == "Bankomat:":
        atm_raw = prop.find_next_sibling("dd")
        atm_text = normalize(atm_raw.text).replace('\xa0', ' ')
        atm_clean = re.search(r'\(([\d\s]+) m\)', atm_text).group(1).replace(" ", "")
        atm = int(atm_clean)
        print("atm:", atm)

#culture_monument 
for prop in props:
    if normalize(prop.text.strip()) == "Kulturni pamatka:":
        culture_monument_raw = prop.find_next_sibling("dd")
        culture_monument_text = normalize(culture_monument_raw.text).replace('\xa0', ' ')
        culture_monument_clean = re.search(r'\(([\d\s]+) m\)', culture_monument_text).group(1).replace(" ", "")
        culture_monument = int(culture_monument_clean)
        print("culture_monument:", culture_monument)
#nature_place 
for prop in props:
    if normalize(prop.text.strip()) == "Prirodni zajimavost:":
        nature_place_raw = prop.find_next_sibling("dd")
        nature_place_text = normalize(nature_place_raw.text).replace('\xa0', ' ')
        nature_place_clean = re.search(r'\(([\d\s]+) m\)', nature_place_text).group(1).replace(" ", "")
        nature_place = int(nature_place_clean)
        print("nature_place:", nature_place)

#pharmacy 
for prop in props:
    if normalize(prop.text.strip()) == "Lekarna:":
        pharmacy_raw = prop.find_next_sibling("dd")
        pharmacy_text = normalize(pharmacy_raw.text).replace('\xa0', ' ')
        pharmacy_clean = re.search(r'\(([\d\s]+) m\)', pharmacy_text).group(1).replace(" ", "")
        pharmacy = int(pharmacy_clean)
        print("pharmacy:", pharmacy)

#sports 
for prop in props:
    if normalize(prop.text.strip()) == "Sportoviste:":
        sports_raw = prop.find_next_sibling("dd")
        sports_text = normalize(sports_raw.text).replace('\xa0', ' ')
        sports_clean = re.search(r'\(([\d\s]+) m\)', sports_text).group(1).replace(" ", "")
        sports = int(sports_clean)
        print("sports:", sports)




#looping through links and extracting data
data = []
status_counter = 1
for link in links:
    url = link
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    price = get_price(soup)
    rooms = get_rooms(url)
    location = get_location(url)
