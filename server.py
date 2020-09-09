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

        wind = Wind();
        polygon = wind.getWindLayerCoordinates(longitude, latitude, wind_power, offset)
        geoJson = {
            'type': 'Polygon',
            'coordinates': [polygon]
        }

        tic = time.perf_counter()
        res = h3.polyfill(geoJson, body["resolution"])
        toc = time.perf_counter()
        print(res)
        print(f"Downloaded the tutorial in {(toc - tic)*1000:4f} ms")

        content = {
            'hex': json.dumps(res, default=serialize_sets)
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
