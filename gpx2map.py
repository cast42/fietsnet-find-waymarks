#!/usr/bin/python

import sys
import gpxpy
import gpxpy.gpx

gpx_file = open('canibaalh.gpx', 'r')

gpx_elem =  gpxpy.parse(gpx_file)

points = []
for track in gpx_elem.tracks:
    for segment in track.segments:
        for point in segment.points:
            #print 'Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation)
            points.append( (float(point.latitude), float(point.longitude), float(point.elevation)) )

# print points

#encoder = gpolyencode.GPolyEncoder()
#print encoder.encode(points)
print """
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>La Cannibale 2013</title>
    <link href="default.css" rel="stylesheet">
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
    <script src="https://www.google.com/jsapi"></script>
    <script>
    // Load the Visualization API and the columnchart package.
    google.load('visualization', '1', {packages: ['columnchart']});
    var mousemarker = null;
    var Coordinates = null;

function initialize() {
  var sault = new google.maps.LatLng(44.091248, 5.408149);
  var montbrun = new google.maps.LatLng(44.174196,5.436387);
  var abovemontbrun = new google.maps.LatLng(44.195918, 5.415831);
  var bedoin = new google.maps.LatLng(44.123686,5.180719 );
  var monventoux = new google.maps.LatLng(44.174261,5.279714);

  var mapOptions = {
    zoom: 12,
    center: abovemontbrun,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  };


  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  var startMarker = new google.maps.Marker({
      position: bedoin,
      map: map,
      icon: 'http://www.google.com/mapfiles/dd-start.png'
  });

  var stopMarker = new google.maps.Marker({
      position: monventoux,
      map: map,
      icon: 'http://www.google.com/mapfiles/dd-end.png'
  });

  // Create a new chart in the elevation_chart DIV.
  var chart = new google.visualization.ColumnChart(document.getElementById('elevation_chart'));

  var Coordinates = ["""

for p in points:
	sys.stdout.write("new google.maps.LatLng(%f, %f)," %(p[0],p[1]))

print """
  new google.maps.LatLng(44.174258, 5.279746)
  ];
  """
#    var elevations = ["""
# for p in points:
# 	sys.stdout.write('%d,' % p[2])
# print """
#    ];


print """
   var Path = new google.maps.Polyline({
    path: Coordinates,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2
  });

  Path.setMap(map);

  // Extract the data from which to populate the chart.
  // Because the samples are equidistant, the 'Sample'
  // column here does double duty as distance along the
  // X axis.
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Afstand');
  data.addColumn('number', 'Dalen');
  data.addColumn('number', 'Stijgen')
"""


WINDOW = 20
for i in range(WINDOW):
    sys.stdout.write("data.addRow(['', null, %d]);" % points[i][2])
for i in range(WINDOW, len(points)-WINDOW):
    sumprev = 0
    sumnext = 0
    for j in range(WINDOW):
        sumprev += points[i-j][2];
        sumnext += points[i+j][2];
    average_prev = sumprev/WINDOW
    average_next = sumnext/WINDOW
    if average_prev <= average_next:
        sys.stdout.write("data.addRow(['',null,%d]);" % points[i][2])
    else:
        sys.stdout.write("data.addRow(['',%d,null]);" % points[i][2])
for i in range(len(points)-WINDOW, len(points)):
    sys.stdout.write("data.addRow(['', null, %d]);" % points[i][2])

print """
  // Draw the chart using the data within its DIV.
  document.getElementById('elevation_chart').style.display = 'block';
  chart.draw(data, {
    height: 150,
    legend: 'none',
    titleY: 'Hoogte (m)'
  });

  google.visualization.events.addListener(chart, 'onmouseover', function(e) {
      if (mousemarker == null) {
        mousemarker = new google.maps.Marker({
          position: Coordinates[e.row],
          map: map,
          icon: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
        });
      } else {
        mousemarker.setPosition(Coordinates[e.row]);
      }
    });
  }
  // Remove the green rollover marker when the mouse leaves the chart
  function clearMouseMarker() {
    if (mousemarker != null) {
      mousemarker.setMap(null);
      mousemarker = null;
    }
  }

google.maps.event.addDomListener(window, 'load', initialize);

    </script>
  </head>
  <body>
    <div id="map-canvas" style="height:85%;"></div>
    <div id="elevation_chart" style="onmouseout=clearMouseMarker()"></div>
  </body>
</html>
"""
