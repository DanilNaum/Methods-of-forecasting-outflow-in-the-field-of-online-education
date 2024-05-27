from bs4 import BeautifulSoup
import csv

file_name = "message18.04.2024.html"
file = open(file_name, encoding='utf-8')
soup = BeautifulSoup(file,"html.parser")
# name = soup.find('div', class_ ="_2Gk_thS")
name_s = soup.find_all('div', class_ ="_2Gk_thS")
name = [x.text for x in name_s]
numbOfMes_s = soup.find_all('div', class_ ="IJ2Se2I")
numbOfMes = [x.text for x in numbOfMes_s]
chatID_s = soup.find_all('button', class_ ="_2dr0IHH")
chatID = [x['data-testid'] for x in chatID_s]

w_file = open("message.csv", mode="a", encoding='utf-8')
file_writer = csv.writer(w_file, delimiter = ";",lineterminator="\r")
# file_writer.writerow(['ChatId','Name','NumberOfMessage'])
for i in range(len(chatID)):
    file_writer.writerow([chatID[i],name[i],numbOfMes[i]])
