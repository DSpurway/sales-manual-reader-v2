from flask import Flask, request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from scrapingant_client import ScrapingAntClient
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

        # Create a ScrapingAntClient instance
        client = ScrapingAntClient(token='8f5726970a07417ba3bf7471c08b0651')
        output = output +"ScrapingAnt run. "

        # Get the HTML page rendered content
        page_content = client.general_request(url).content

        # Parse content with BeautifulSoup
        soup = BeautifulSoup(page_content)

        Product_Life_Cycle_Title = soup.find(string="Product life cycle dates")
        Product_Life_Cycle_Title = Product_Life_Cycle_Title.find_next(string="Product life cycle dates")
        Product_Life_Cycle_Table = soup.find("table")
        output = output +"The Life Cycle Table looks like this: " +Product_Life_Cycle_Table.text
        return output

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
