from urllib.request import urlopen
import re
#url = "http://olympus.realpython.org/profiles/aphrodite"
# url = "http://olympus.realpython.org/profiles/poseidon"
# page = urlopen(url)
# #print(page)

# html_bytes = page.read()
# html = html_bytes.decode("utf-8")
# #print(html)

# title_index = html.find("<title>")
# #print(title_index)

# start_index = title_index + len("<title>")
# #print(start_index)

# end_index = html.find("</title>")
# #print(end_index)

# title = html[start_index:end_index]
# #print(title)

# print(re.findall("kvec*k*o*", "kvecko", re.IGNORECASE))

# match_results = re.search("ab*c", "ABC", re.IGNORECASE)
# print(match_results.group())

# string = "Everything is <replaced> if it's in <tags>."
# string = re.sub("<.*>", "ELEPHANTS", string)
# print(string)

# pattern = "<title.*?>.*?</title.*?>"
# match_results = re.search(pattern, html, re.IGNORECASE)
# title = match_results.group()
# title = re.sub("<.*?>", "", title) # Remove HTML tags
# print(title)

#ex1 
url = "http://olympus.realpython.org/profiles/dionysus"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

for string in ["Name: ","Favorite Color: "]:
    string_start_idx = html.find(string)
    text_start_idx = string_start_idx + len(string)
    
    next_html_tag_offset = html[text_start_idx:].find("<")
    text_end_idx = text_start_idx + next_html_tag_offset

    raw_text = html[text_start_idx:text_end_idx]
    clean_text = raw_text.strip(" \r\n\t")
    print(clean_text)