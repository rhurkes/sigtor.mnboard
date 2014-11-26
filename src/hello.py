from flask import Flask, render_template
import requests
import json
from lxml import html

app = Flask(__name__)

@app.route('/mnboard/')
def mnboard():
    model = {}
    
    # TODO Update to async
    endpoint = 'http://kamala.cod.edu/mn/latest.fxus63.KMPX.html'
    page = requests.get(endpoint)
    tree = html.fromstring(page.text)
    afd = html.tostring(tree.xpath('//body/pre/font')[0], pretty_print = True)
    afd = afd.replace('&amp;nbsp', '')
    model['afd'] = afd

    # TODO update to async
    endpoint = 'http://forecast.weather.gov/MapClick.php?lat=44.8819&lon=-93.2217&FcstType=json'
    response = requests.get(endpoint)
    model['nwsData'] = json.loads(response.text)

    model['iemPrefix'] = 'http://www.meteor.iastate.edu/~ckarsten/bufkit/images/plotter.php?site=kmsp'
    return render_template('hello.html', model = model)

if __name__ == '__main__':
    app.run(debug = True)
