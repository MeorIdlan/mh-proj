from flask import Flask, jsonify, request
from scraper import scrape

app = Flask(__name__)

@app.route('/api/subway-locations', methods=['GET'])
def get_subway_locations():
    query = request.args.get('query', default=None, type=str)
    scraper = scrape.Scraper()
    return jsonify({'locations':scraper.getLocations(query=query)})

@app.route('/dev-api/subway-locations', methods=['GET'])
def dev_get_subway_locations():
    query = request.args.get('query', default=None, type=str)
    scraper = scrape.Scraper('dev')
    response = jsonify({'locations': scraper.getLocations(query=query)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True)