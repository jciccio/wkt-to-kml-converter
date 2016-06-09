# wkt-to-kml-converter

This script is intended to convert WKT files into KML files.

WKT can have multiple mutipolygons, this tool process line by line and split the results into different kml output files.

For executing, you need to pass a folder where the wkt files you want to process are located.

Output:
- A folder with splitted wkt
- A folder with splitted kml
- A folder with non duplicated kml
