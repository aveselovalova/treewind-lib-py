import math;

class Wind:
    MIN_POINTS_IN_POLYGON = 3;
    COORDINATES_OFFSET = 0.0001;
    LATITUDE_WIND_INCREMENT = 0.0002;

    def _fibonacci(self, nums):
        preNumb = 0;
        res = 1;
        while (nums > 1):
            tmp = preNumb;
            preNumb = res;
            res += tmp;
            nums -= 1;
        return res;

    def _generateFibonacciLongitudes(self, longitude, windPower):
        fibNum = 3;
        longitudes = [];
        arrIndex = 0;
        cuttedWindPower = windPower - 1 if windPower > 6 else windPower;
        windPoints = self.MIN_POINTS_IN_POLYGON + cuttedWindPower;
        while (fibNum < windPoints):
            longitudes.append(
                self._fibonacci(fibNum) * self.COORDINATES_OFFSET + (longitude if arrIndex == 0 else longitudes[arrIndex - 1])
            );
            fibNum += 1;
            arrIndex += 1;

        return longitudes;
        
    def _generateFunction(self, windLongitudes, latitude, longitude, increment):
        l = [[latitude, longitude]];
        r = [];
        isLastPoint = len(windLongitudes) - 1;
        for i in range(isLastPoint + 1):
            currentLat = l[i][0];
            currentLon = windLongitudes[i];
            l.append([currentLat if i == isLastPoint else currentLat + increment, currentLon]);
            item = latitude - self.LATITUDE_WIND_INCREMENT * (i + 1);
            if (i == isLastPoint):
                item = r[len(r) - 1][0];
            r.append([item, currentLon]);
        return l + list(reversed(r));

    def _rotate(self, treeLon, treeLat, x, y, radians):
        cos = math.cos(radians);
        sin = math.sin(radians);
        return [cos * (y - treeLat) - sin * (x - treeLon) + treeLat, cos * (x - treeLon) + sin * (y - treeLat) + treeLon];

    def getWindLayerCoordinates(self, longitude, latitude, windPower, offsetAngle):
        longitudes = self._generateFibonacciLongitudes(longitude, 6)
        generated = self._generateFunction(longitudes, latitude, longitude, self.LATITUDE_WIND_INCREMENT);
        rotated = []
        for point in generated:
            rotated.append(self._rotate(longitude, latitude, point[1], point[0], offsetAngle))
        rotated.append([latitude, longitude])
        return rotated;
