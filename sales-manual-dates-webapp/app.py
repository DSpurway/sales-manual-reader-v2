from flask import Flask, request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/')
def index():
    content = {}

    if request.args.get('url'):
        url = request.args.get('url')
        content['result'] = "Found URL"
        content['url'] = url

        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')

        Product_Life_Cycle_Title = soup.find("a", string="Product life cycle dates")
        Product_Life_Cycle_Table = Product_Life_Cycle_Title.find_next("table")
        MTM = Product_Life_Cycle_Table.find_next('td')
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
