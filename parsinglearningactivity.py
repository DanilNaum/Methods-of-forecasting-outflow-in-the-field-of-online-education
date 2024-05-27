from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv


def table_Scrape(soup,learningGroupe):
    # table = soup.select_one()
    table = soup.find('table', class_='table _header-grey-light _header-thin _header-vertical-align-middle')
    # headers = [th.text for th in table.findAll("tr")[1]]
    body = table.find('tbody')
    with open("Lg"+learningGroupe+".csv", "a", encoding='utf-8') as f:
        wr = csv.writer(f,delimiter = ";",lineterminator="\r")
        # wr.writerow(headers)
        for data_row in body.findAll("tr"):
            # th = data_row.find('th')
            
            alltd = data_row.findAll("td")
            print([td.text for td in alltd])
            try:
                score = data_row.find('div',class_ = '-VCGnCA').text
            except:
                score = ''
            wr.writerow( [data_row.find('div',class_ = 'flex-row-center gap-3').div.a.text,data_row.find('div',class_ = 'flex-row-center gap-3').div.a.get('href')] 
                        # + [td.text for td in alltd[1:6]] +
                        +[ score]+
                         [ alltd[7].text] )  

token = '*'
url = "https://soholms.com/login/token/" + token
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(url)
python_button = driver.find_element(By.CLASS_NAME, "_1H-TBIp")
python_button.click()

url = "https://master.soholms.com/lms/learning/courses/4462/groups/150853"
learningGroupe = url.split('/')[-1]
driver.get(url)
python_button = driver.find_element(By.CSS_SELECTOR, ".table-pagination_nav button:nth-child(2)")
with open("Lg"+learningGroupe+".csv", "w", encoding='utf-8') as f:
        wr = csv.writer(f,delimiter = ";",lineterminator="\r")
        wr.writerow(["Имя","ССылка","Прогресс сколько из скольки","Средний балл/Суммарный балл"])
    
while python_button.is_enabled():
    python_button = driver.find_element(By.CSS_SELECTOR, ".table-pagination_nav button:nth-child(2)")
    time.sleep(0.7)
    soup = BeautifulSoup(driver.page_source)
    # print(soup)
    table_Scrape(soup,learningGroupe)
    # names = [[x.a.get('href'),x.a.text,y.text] 
    #          for x in soup.findAll('div',class_ = 'flex-row-center gap-3') for y in soup.findAll('div',class_ = '-VCGnCA')]
    # print(names)
    python_button.click()
    
driver.quit()

    