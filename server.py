import falcon
import json
import h3
import time
from falcon_cors import CORS
from hexagons_calc import Wind

def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj


class Hexagons():
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        credentials = json.loads(req.stream.read())
        body = json.loads(credentials["body"])
        longitude = body["longitude"];
        latitude = body["latitude"];
        wind_power = body["windPower"];
        offset = body["offset"];
        resolution = body["resolution"];
        color = body["color"];

        wind = Wind();
        polygon = wind.getWindLayerCoordinates(longitude, latitude, wind_power, offset)
        geoJson = {
            'type': 'Polygon',
            'coordinates': [polygon]
        }

        hexagons = h3.polyfill(geoJson, resolution)
        
        h3_index = h3.geo_to_h3(latitude, longitude, resolution);
        trees = [];
        for hex in hexagons:
            direction = h3.h3_distance(h3_index, hex);
            opacity = 255 - direction * (80 / wind_power);
            if (opacity > 0):
                trees.append({ 'opacity': direction, 'hex': hex, 'color': color });

        content = {
            'hex': json.dumps(trees, default=serialize_sets)
        }

        resp.body = json.dumps(content)


cors = CORS(
    allow_all_origins=True,
    allow_all_headers=True,
    allow_all_methods=True,
)

api = falcon.API(middleware=[cors.middleware])

hexagons = Hexagons()

api.add_route('/hexagons', hexagons)
