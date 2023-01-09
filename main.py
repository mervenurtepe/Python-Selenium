from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pathlib import Path
from selenium.webdriver.common.by import By
import json

source = "https://www.8notes.com/piano/classical/sheet_music/"
print("                     Program baslatiliyor ..... \n")
print ("8notes sitesine baglaniliyor...")
defurl='https://www.8notes.com/'

def homefunction(source):
    wait_imp = 10
    CO = webdriver.ChromeOptions()
    CO.add_experimental_option('useAutomationExtension', False)
    CO.add_argument('--ignore-certificate-errors')
    CO.add_argument('--start-maximized')
    wd = webdriver.Chrome(r'C:/Users/MERVE TEPE/Desktop/selenium/chromedriver.exe',options=CO)
    wd.get(source)
    wd.implicitly_wait(wait_imp)
    artist=[]
    title=[]
    difficulty=[]
    link=[]
    tag_tbody=wd.find_element(By.TAG_NAME, 'tbody')
    response=tag_tbody.find_elements(By.TAG_NAME, 'tr')

    for match in response:
        singer=match.find_element("xpath", './td[2]').text
        artist.append(singer)
        title.append(match.find_element("xpath", './td[3]').text)
        temp = match.find_element("xpath", './td[4]')
        diff_level=temp.find_element(By.TAG_NAME,"img").get_attribute('title')
        difficulty.append(diff_level)
        onclick_addr = match.get_attribute('onclick')
        onclick_addr = onclick_addr[19:]
        onclick_addr = onclick_addr[:-1]
        onclick_addr=defurl + onclick_addr
        link.append(onclick_addr)
        linkjson = json.dumps(link)
        diffjson = json.dumps(difficulty)
        artistjson = json.dumps(artist)
        titlejson = json.dumps(title)
        with open("Ozgul_Baglanti.json", "w") as outfile:
            outfile.write(linkjson)
        with open("Zorluk.json", "w") as outfile:
            outfile.write(diffjson)
        with open("Artist.json", "w") as outfile:
            outfile.write(artistjson)
        with open("Title.json", "w") as outfile:
            outfile.write(titlejson)
        detailfunction(onclick_addr)
    print('Ana sayfa scrape yapıldı')

def detailfunction(source):
    wait_imp = 10
    CO = webdriver.ChromeOptions()
    CO.add_experimental_option('useAutomationExtension', False)
    CO.add_argument('--ignore-certificate-errors')
    CO.add_argument('--start-maximized')
    wd = webdriver.Chrome(r'C:/Users/MERVE TEPE/Desktop/selenium/chromedriver.exe',options=CO)
    wd.get(source)
    wd.implicitly_wait(wait_imp)
    imagelink = []
    midilink = []
    about = []
    wholeabout = ""
    whole_images_links=[]
    imagegeneral=wd.find_elements("xpath",'// main / div / div[ @class ="img-container"]')
    for a in imagegeneral:
        imagelinkinfo = a.find_element(By.TAG_NAME, "img").get_attribute('src')
        whole_images_links.append(imagelinkinfo)
    imagelink.append(whole_images_links)
    imagejson = json.dumps(imagelink)
    with open("İmg_Linkler.json", "w") as outfile:
        outfile.write(imagejson)
    midi = wd.find_element("xpath", '//li/a[@class="midi_list"]').get_attribute('href')
    midilink.append(midi)
    midijson = json.dumps(midilink)
    with open("Midi_Linkler.json", "w") as outfile:
        outfile.write(midijson)
    aboutinfo=wd.find_elements("xpath", '//div[@id="infobox"]/table')
    for label1 in aboutinfo:
        label2 = label1.find_elements(By.TAG_NAME, 'td')
        for label3 in label2:
            wholeabout = wholeabout + label3.text
    about.append(wholeabout)
    aboutjson = json.dumps(about)
    with open("About.json", "w") as outfile:
        outfile.write(aboutjson)
    print("Özgün bağlantılardan scrape yapıldı")
    

homefunction(source)

files=['About.json','Artist.json','İmg_Linkler.json','Midi_Linkler.json','Ozgul_Baglanti.json','title.json','Zorluk.json']

def merge_JsonFiles(filename):
    result = list()
    for f1 in filename:
        with open(f1, 'r') as infile:
            result.extend(json.load(infile))

    with open('final.json', 'w') as output_file:
        json.dump(result, output_file)

merge_JsonFiles(files)

print("Program Bitti")