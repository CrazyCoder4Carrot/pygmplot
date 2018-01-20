import json
from shutil import copyfile


class PyGmPlot(object):
    def __init__(self, lat, lng, key, zoom=10):
        '''Initilize the google map      
        Args:
            lat: The latitude of the center coordination
            lng: The longitude of the center coordination
            key: The google map key get from Google map
            zoom: The zoom level of the google map (default: {10})
        '''
        self.vars = {}
        self.zoom = zoom
        self.vars['key'] = key
        self.vars['init'] = {'zoom': zoom, 'center': {'lat': lat, 'lng': lng}}
        self.vars['markers'] = []
        self.vars['lines'] = []
        self.vars['polygons'] = []
        self.vars['circles'] = []
        self.filename = 'plotdata.js'
        self.template = 'template.html'

    def add_marker(self, lat, lng, **kwargs):
        '''Add f marker to the google map
        Args:
            lat: The latitude of the marker.
            lng: The longtitude of the marker.
            **kwargs: This parameter allows you to customize your maker.
            such as label='label'
            more information refer to
            https://developers.google.com/maps/documentation/javascript/markers
        '''
        marker = {}
        marker['position'] = {'lat': lat, 'lng': lng}
        marker.update(kwargs)
        self.vars['markers'].append(marker)

    def add_line(self, coords, **kwargs):
        '''Add a line on the google map        
        Args:
            coords:{list} list of (lat ,lng) tuples
            **kwargs: This parameter allows you to customize your line.
            such as strokeColor = '#FF0000'
            more information refer to
            https://developers.google.com/maps/documentation/javascript/examples/polyline-simple
        '''
        line = {}
        line['path'] = [{'lat': lat, 'lng': lng} for lat, lng in coords]
        line.update(kwargs)
        self.vars['lines'].append(line)

    def add_circle(self, lat, lng, radius, **kwargs):
        '''Draw a circle on google map
        Args:
            lat: The lat of the center
            lng: The lng of the center
            radius: The radius in KM
            **kwargs: This parameter allows you to customize your circle.
            such as fillColor='#FF0000'
            more information refer to
            https://developers.google.com/maps/documentation/javascript/examples/circle-simple
        '''
        circle = {}
        radius *= 1000
        circle['center'] = {'lat': lat, 'lng': lng}
        circle['radius'] = radius
        circle.update(kwargs)
        self.vars['circles'].append(circle)

    def add_polygon(self, boundary, holes, **kwargs):
        '''[summary]
        
        [description]
        
        Args:
            boundary: outer boundary list of (lat, lng) tuples.
            holes: list of holes in the polygonm, each hole is a list of
                    (lat, lng) tuples.
            **kwargs: This parameter allows you to customize your polygon.
            such as fillOpacity=0.35
            more information refer to
            https://developers.google.com/maps/documentation/javascript/examples/polygon-hole
        '''
        polygon = {}
        path = []
        path.append([{'lat': lat, 'lng': lng} for lat, lng in boundary])
        for hole in holes:
            path.append([{'lat': lat, 'lng': lng} for lat, lng in hole])
        polygon['paths'] = path
        polygon.update(kwargs)
        self.vars['polygons'].append(polygon)

    def draw(self, filename):
        '''Create the file in target path
        Args:
            filename: The output file and path.
        '''
        copyfile(self.template, filename)
        with open(self.filename, 'w') as outfile:
            for key in self.vars:
                outfile.write(" ".join(
                    [key, '=', json.dumps(self.vars[key]), ';\n']))


def main():
    key = "YOUR_GOOLE_MAP_KEY"
    plot = PyGmPlot(26.771339, -72.346313, key, 5)
    plot.add_marker(25.466, -90.118)
    plot.add_circle(29.444291, -98.531578, 500, strokeColor='black')
    plot.add_line([(30.444291, -90.531578), (35.467, -80.118),(32.321, -70.757),
                 ], strokeColor='#black')
    outerCoords = [ (25.774,-80.190), (18.466, -66.118), (32.321, -64.757)]
    hole1 = [(28.745, -70.579), (29.570, -67.514), (27.339, -66.668)]
    hole2 = [(25.745, -76.579), (26.570, -70.514), (20.339, -66.668)]
    plot.add_polygon(outerCoords, [hole1, hole2], fillColor='#FFC107')
    plot.draw('test.html')


if __name__ == '__main__':
    main()
