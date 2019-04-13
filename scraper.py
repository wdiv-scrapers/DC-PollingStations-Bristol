import json
import requests
from dc_base_scrapers.common import get_data_from_url
from dc_base_scrapers.arcgis_scraper import ArcGisScraper
from dc_base_scrapers.geojson_scraper import GeoJsonScraper


council_id = 'E06000023'


def scrape_opendata():
    stations_url = "https://opendata.bristol.gov.uk/explore/dataset/polling-stations/download/?format=geojson&timezone=Europe/London"
    districts_url = "https://opendata.bristol.gov.uk/explore/dataset/polling-districts/download/?format=geojson&timezone=Europe/London"

    print(stations_url)
    stations_scraper = GeoJsonScraper(
        stations_url, council_id, 'utf-8', 'stations_opend', key='objectid')
    stations_scraper.scrape()

    print(districts_url)
    districts_scraper = GeoJsonScraper(
        districts_url, council_id, 'utf-8', 'districts_opend', key='objectid')
    districts_scraper.scrape()


def scrape_arcgis():
    stations_url = "https://maps.bristol.gov.uk/arcgis/rest/services/ext/localinfo/MapServer/%s/query?where=OBJECTID+LIKE+%%27%%25%%27&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=4326&returnIdsOnly=false&returnCountOnly=false&orderByFields=OBJECTID&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&f=pjson"
    districts_url = "https://maps.bristol.gov.uk/arcgis/rest/services/ext/localinfo/MapServer/%s/query?where=OBJECTID+LIKE+%%27%%25%%27&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=4326&returnIdsOnly=false&returnCountOnly=false&orderByFields=OBJECTID&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&f=pjson"
    index_url = "https://maps.bristol.gov.uk/arcgis/rest/services/ext/localinfo/MapServer/?f=pjson"

    """
    Bristol's polling station and district data is not published
    with a consistent layer id: it keeps changing
    Read the index to identify the correct layers to request.
    """
    index_str = get_data_from_url(index_url)
    index_data = json.loads(index_str.decode('utf-8'))
    for layer in index_data['layers']:
        if 'polling station' in layer['name'].lower().strip():
            stations_url = stations_url % (layer['id'])
        if 'polling district' in layer['name'].lower().strip():
            districts_url = districts_url % (layer['id'])

    # If we couldn't find appropriate layers, give up
    if '%s' in stations_url:
        raise ValueError('Failed to find Polling Stations layer')
    if '%s' in districts_url:
        raise ValueError('Failed to find Polling Districts layer')

    print(stations_url)
    stations_scraper = ArcGisScraper(stations_url, council_id, 'utf-8', 'stations_arcgis')
    stations_scraper.scrape()

    print(districts_url)
    districts_scraper = ArcGisScraper(districts_url, council_id, 'utf-8', 'districts_arcgis')
    districts_scraper.scrape()


scrape_opendata()
scrape_arcgis()
