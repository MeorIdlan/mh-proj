from flask import Flask, jsonify, request
import scrape

app = Flask(__name__)

@app.route('/api/subway-locations', methods=['GET'])
def get_subway_locations():
    query = request.args.get('query', default=None, type=str)
    scraper = scrape.Scraper()
    return jsonify({'locations':scraper.getLocations(query=query)})

if __name__ == '__main__':
    app.run(debug=True)