from flask import Flask, request
from urllib.request import urlopen
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/lookup')
def lookup():
    response = "Search failed"

    if request.args.get('mtm'):
        mtm = request.args.get('mtm')
        machine_type = mtm[0:4]

        def build_url(machine_type, doc_id):
            search_url = "https://www.ibm.com/common/ssi/ShowDoc.wss?docURL=/common/ssi/rep_sm/"
            search_url += str(doc_id)
            search_url += "/872/ENUS"
            search_url += machine_type
            search_url += "-_h0"
            search_url += str(doc_id)
            search_url += "/index.html"
            return search_url

        def find_mtm(search_url):
            try:
                print("trying " + search_url)
                html = urlopen(search_url)
                soup = BeautifulSoup(html, 'html.parser')
                # soup.contents
                product_life_cycle_title = soup.find("a", string="Product life cycle dates")
                product_life_cycle_table = product_life_cycle_title.find_next("table")
                found_mtm = product_life_cycle_table.find_next('td')
                found_mtm = found_mtm.get_text()
                return found_mtm
            except:
                return ""

        def search(machine_type):
            doc_id = 1
            while doc_id < 10 :
                search_url = build_url(machine_type, doc_id)
                found_mtm = find_mtm(search_url)
                if found_mtm == mtm:
                    print("found MTM at " + search_url)
                    return search_url
                doc_id += 1
            
            print("cannot find sales manual for " + mtm)
            return "Not found"

        response = search(machine_type)

    else:
        response = "Not found"

    return response

@app.route('/')
def index():
    response = "Search failed"

    if request.args.get('mtm'):
        mtm = request.args.get('mtm')
        machine_type = mtm[0:4]

        def build_url(machine_type, doc_id):
            search_url = "https://www.ibm.com/common/ssi/ShowDoc.wss?docURL=/common/ssi/rep_sm/"
            search_url += str(doc_id)
            search_url += "/877/ENUS"
            search_url += machine_type
            search_url += "-_h0"
            search_url += str(doc_id)
            search_url += "/index.html"
            return search_url

        def find_mtm(search_url):
            try:
                print("trying " + search_url)
                html = urlopen(search_url)
                soup = BeautifulSoup(html, 'html.parser')
                # soup.contents
                product_life_cycle_title = soup.find("a", string="Product life cycle dates")
                product_life_cycle_table = product_life_cycle_title.find_next("table")
                found_mtm = product_life_cycle_table.find_next('td')
                found_mtm = found_mtm.get_text()
                return found_mtm
            except:
                return ""

        def search(machine_type):
            doc_id = 1
            while doc_id < 10 :
                search_url = build_url(machine_type, doc_id)
                found_mtm = find_mtm(search_url)
                if found_mtm == mtm:
                    print("found MTM at " + search_url)
                    return search_url
                doc_id += 1
            
            print("cannot find sales manual for " + mtm)
            return "Not found"

        response = search(machine_type)

    else:
        response = "Not found"

    return response

@app.route('/healthz')
# Added healthcheck endpoint
def healthz():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
