from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests




startUrl = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("C:/Users/robot/Downloads/chromedriver_win32/chromedriver.exe")
browser.get(startUrl)
time.sleep(10)

planetData = []
newPlanetData =[]
headers = ["NAME", "LIGHT_YEARS_FROM_EARTH", "PLANET_MASS", "STELLAR_MAGNITUDE", "DISCOVERY_DATE", "HYPER_LINK",
           "PLANET_TYPE", "PLANET_RADIUS", "MASS", "ORBITAL_RADIUS", "ORBITAL_PERIOD", "ECCENTRICITY"]
def scrape():


    for i in range(0,10):
        soup = BeautifulSoup(browser.page_source,"html.parser")
        for ultag in soup.find_all("ul",attrs={"class","exoplanet"}):
            liTags = ultag.find_all("li")
            tempList = []
            for index,litag in enumerate(liTags):
                if index == 0:
                    tempList.append(litag.find_all("a")[0].contents[0])
                else:
                    try:
                        tempList.append(litag.contents[0])
                    except:
                        tempList.append("")
            hyperLink = liTags[0]
            tempList.append("https://exoplanets.nasa.gov/"+hyperLink.find_all("a",href=True)[0]["href"])
            planetData.append(tempList)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
def more_scrape(hyperLink):
    try:
        page = requests.get(hyperLink)
        soup = BeautifulSoup(page.content,"html.parser")
        tempList = []
        for trtag in soup.find_all("tr",attrs={"class","fact_row"}):
            tdTags = trtag.find_all("td")
            for tdtag in tdTags:
                try:
                    tempList.append(tdtag.find_all("div",attrs={"class","value"})[0].contents[0])
                except:
                    tempList.append("")
        newPlanetData.append(tempList)
    except:
        time.sleep(1)
        more_scrape(hyperLink)
scrape()

for index,data in enumerate(planetData):
    more_scrape(data[5])

finalData = []
for index,data in enumerate(planetData):
    newElement = newPlanetData[index]
    newElement=[elem.replace("\n"," ")for elem in newElement]
    newElement = newElement[:7]
    finalData.append(data+newElement)


with open("Scrapper1.csv","w") as f:
    csvWriter = csv.writer(f)
    csvWriter.writerow(headers)
    csvWriter.writerows(finalData)

