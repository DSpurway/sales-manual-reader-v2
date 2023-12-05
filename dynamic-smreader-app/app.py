from flask import Flask, request
from urllib.request import urlopen
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/')
def index():
    content = {}

    if request.args.get('url'):
        url = request.args.get('url')
        output = "Input url of: " +url +" recieved. "
        content['result'] = "Found URL"
        content['url'] = url

        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(options=options)
        driver.get('http://selenium.dev')

        driver.maximize_window() #maximize the window
        driver.get(url)          #open the URL
        driver.implicitly_wait(220) #maximum time to load the link

        try:
            element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.ID, "h2-smabstr"))
            )

            result = driver.page_source
        finally:
            driver.quit()

        soup = BeautifulSoup(result, 'html.parser')

        Product_Life_Cycle_Title = soup.find(string="Product life cycle dates")
        Product_Life_Cycle_Title = Product_Life_Cycle_Title.find_next(string="Product life cycle dates")
        Product_Life_Cycle_Table = soup.find("table")
        output = output +"The Life Cycle Table looks like this: " +Product_Life_Cycle_Table.text

        MTM = Product_Life_Cycle_Table.find('td')
        Announce = MTM.find_next('td')
        Available = Announce.find_next('td')
        WDFM = Available.find_next('td')
        EOS = WDFM.find_next('td')

        content['mtm'] = MTM.get_text()
        content['announce'] = Announce.get_text()
        content['available'] = Available.get_text()
        content['wdfm'] = WDFM.get_text()
        content['eos'] = EOS.get_text()

        content['result'] = "Success"

    else:
        content ['result'] = "URL Missing"

    return json.dumps(content)

@app.route('/healthz')
# Added healthcheck endpoint
def healthz():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
