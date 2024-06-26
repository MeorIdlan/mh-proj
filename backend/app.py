from flask import Flask, jsonify, request
from flask_cors import CORS
from scraper import scrape
from location.locationObj import Location
from complexQuery.nlp_parse import parse_query

app = Flask(__name__)
CORS(app)

@app.route('/api/subway-locations', methods=['GET'])
def get_subway_locations():
    query = request.args.get('query', default=None, type=str)
    scraper = scrape.Scraper()
    return jsonify({'locations':scraper.getLocations(query=query)})

@app.route('/dev-api/subway-locations', methods=['GET'])
def dev_get_subway_locations():
    query = request.args.get('query', default=None, type=str)
    scraper = scrape.Scraper('dev')
    return jsonify({'locations': scraper.getLocations(query=query)})

@app.route('/api/complex-query', methods=['POST'])
def complex_query():
    data = request.json
    query = data['query'].lower()
    locations = [Location.fromDict(loc) for loc in data['locations']]
    
    filteredLocations = parse_query(query=query, locations=locations)
    
    return jsonify({'locations': filteredLocations})

if __name__ == '__main__':
    app.run(debug=True)