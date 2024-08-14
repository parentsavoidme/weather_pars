import requests
from bs4 import BeautifulSoup
import pandas

# url = "https://rp5.ru/"
# headers={
#     "Agent" : "*/*",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
#  }
# request_rp5 = requests.get(url, headers = headers )
# src = request_rp5.text
#
# with open ("index.html", "w", encoding= "utf 8") as file:
#     file.write(src)

with open("index.html", "r", encoding= "utf 8") as file:
    src = file.read()

soup  = BeautifulSoup(src, "lxml")

all_countries = soup.find(class_="countryMap").find_all("a")
#print(all_countries)
url1 = "https://rp5.ru"
url2 = "http://rp5.co.za"
list = []
triple_link=0
for country in all_countries:
    link = country.get("href")
    triple_link+=1
    if triple_link % 3 == 0:
        if link[0] == "/":
            link = url1 + link
            list.append(link)
        else:
            for i in range (len(link) - 1,0,-1):
                if link[i] == "/":
                    link = link[i:]
                    link = url2 + link
                    list.append(link)
                    break


def get_weather(link,array1,array2):
    request_page = requests.get(link)
    small_src = request_page.text
    soup1 = BeautifulSoup(small_src, "lxml")
    find_temperature = soup1.find(class_="countryMap").find_all(class_="t_0")
    find_area = soup1.find(class_="countryMap").find_all(class_="href20")
    for temperature, area in zip(find_temperature, find_area):
        t_t = temperature.text
        a_t = area.text
        array1.append(t_t)
        array2.append(a_t)
      #  print(f"{t_t} : {a_t}")

def get_all_weather(array1, array2):
    i=0
    for link in list:
        i+=1
        get_weather(link,array1,array2)
        print(i)


weather_list = []
area_list = []
get_all_weather(weather_list,area_list)

data = {
    "Weather" : weather_list,
    "Area" : area_list
}

file_name = "result.xlsx"
df = pandas.DataFrame(data)
df.to_excel(file_name,index = 0)







