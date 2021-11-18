from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import sys

MTM = sys.argv[1]
# MTM = "9117-MMD"
Machine_Type = MTM[0:4]
Doc_ID = 1

def Build_url(Machine_Type, Doc_ID):
    global Search_url
    Search_url = "https://www.ibm.com/common/ssi/ShowDoc.wss?docURL=/common/ssi/rep_sm/"
    Search_url += str(Doc_ID)
    Search_url += "/877/ENUS"
    Search_url += Machine_Type
    Search_url += "-_h0"
    Search_url += str(Doc_ID)
    Search_url += "/index.html"

Build_url(Machine_Type, Doc_ID)

def Find_MTM(Search_url):
    global Found_MTM
    html = urlopen(Search_url)
    soup = BeautifulSoup(html, 'html')
    # soup.contents
    Product_Life_Cycle_Title = soup.find("a", string="Product life cycle dates")
    Product_Life_Cycle_Table = Product_Life_Cycle_Title.find_next("table")
    Found_MTM = Product_Life_Cycle_Table.find_next('td')
    Found_MTM = Found_MTM.get_text()

Find_MTM(Search_url)

while Doc_ID < 10 and Found_MTM != MTM:
    Doc_ID += 1
    Build_url(Machine_Type, Doc_ID)
    Find_MTM(Search_url)
    
print (Search_url)
