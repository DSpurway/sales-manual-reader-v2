from flask import Flask, request
from quickcsv.file import *
import json

app = Flask(__name__)

@app.route('/')
def index():
    content = {}

    if request.args.get('MTM'):
        url = request.args.get('MTM')
        content['result'] = "Found MTM"
        content['MTM'] = MTM

        csvfile=read_csv("ibm_product_lifecycle_list.csv", encoding='latin1')
        df=create_df(csvfile)
        row = df[df["MTM"] == MTM]
        Available = row["GA"].item()
        Announce = "The input file I am using does not have announcement dates, but it will have been shortly before the GA date, which was " + Available
        WDFM = row["EOM"].item()
        EOS = row["EOS"].item()

        content['mtm'] = MTM.get_text()
        content['announce'] = Announce.get_text()
        content['available'] = Available.get_text()
        content['wdfm'] = WDFM.get_text()
        content['eos'] = EOS.get_text()

        content['result'] = "Success"

    else:
        content ['result'] = "MTM Missing"
        
    return content

@app.route('/healthz')
# Added healthcheck endpoint
def healthz():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
