from flask import Flask, request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/')
def find():
    if request.args.get('mtm'):
        MTM = request.args.get('mtm')
        Machine_Type = MTM[0:4]
        Result_URL = "Unknown"
        Doc_ID = 1
        
        def Build_url(Machine_Type, Doc_ID):
            Search_url = "https://www.ibm.com/common/ssi/ShowDoc.wss?docURL=/common/ssi/rep_sm/"
            Search_url += str(Doc_ID)
            Search_url += "/877/ENUS"
            Search_url += Machine_Type
            Search_url += "-_h0"
            Search_url += str(Doc_ID)
            Search_url += "/index.html"
            return Search_url
        
        def Find_MTM(Search_url):
            html = urlopen(Search_url)
            soup = BeautifulSoup(html, 'html')
            # soup.contents
            Product_Life_Cycle_Title = soup.find("a", string="Product life cycle dates")
            Product_Life_Cycle_Table = Product_Life_Cycle_Title.find_next("table")
            Found_MTM = Product_Life_Cycle_Table.find_next('td')
            Found_MTM = Found_MTM.get_text()
            return Found_MTM
        
        def Check_URL(Machine_Type, Result_URL):
            Doc_ID = 1
            while Doc_ID < 10 :
                Search_URL = Build_url(Machine_Type, Doc_ID)
                Found_MTM = Find_MTM(Search_URL)
                if Found_MTM == MTM:    
                    print("found mtm at " + Search_URL)
                    Result_URL = Search_URL
                    return Result_URL
                Result_URL = Search_URL
                return Result_URL
                Doc_ID += 1

        return Check_URL(Machine_Type, Result_URL)

@app.route('/healthz')
# Added healthcheck endpoint
def healthz():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
