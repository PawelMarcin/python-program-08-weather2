from classes.argsconstsfiles import FileHandling
from classes.argsconstsfiles import PATH_TO_CACHED_FORECASTS
import requests


class WeatherForecast:
    def __init__(self, api_key):
        self.api_key = api_key
        self.saved_forecasts = []
        self.saved_forecasts_dates = []
        self.api_forecast = {}
        self.searched_forecast = ''
        self.is_forecast_from_api = False

    def __iter__(self):
        for elem in self.saved_forecasts:
            self.saved_forecasts_dates.append(elem[0])
        return iter(self.saved_forecasts_dates)

    def __next__(self):
        pass

    def __getitem__(self, item):
        for elem in self.items():
            if elem[0] == item:
                self.searched_forecast = elem[1]
                return elem[1]
        else:
            self.get_forecast_from_api()
            for elem in self.search_in_forecast_from_api():
                if elem[0] == item:
                    self.is_forecast_from_api = True
                    self.searched_forecast = elem[1]
                    return elem[1]

    def __setitem__(self, key, value):
        self.saved_forecasts.append((key, value))
        self.saved_forecasts.sort()

    def items(self):
        fh = FileHandling(PATH_TO_CACHED_FORECASTS)
        for elem in fh.readfromfile():
            yield elem[0], elem[1]
            self.saved_forecasts.append((elem[0], elem[1]))

    def get_forecast_from_api(self):
        url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/daily"
        qstr = {"lat": "52.06931644938404", "lon": "19.48030183891317",
                "units": "metric", "lang": "pl"}
        headers = {
            'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
            'x-rapidapi-key': self.api_key
        }
        response = requests.request("GET", url, headers=headers, params=qstr)
        self.api_forecast = response.json()

    def search_in_forecast_from_api(self):
        for day_forecast in self.api_forecast['data']:
            day = day_forecast['valid_date']
            desc = ('Będzie padać: ' + day_forecast['weather']['description']
                    + '.') if day_forecast['weather']['code'] \
                              in range(200, 700) else ('Nie będzie padać')
            yield day, desc

    def write_saved_forecasts_to_file(self):
        fh = FileHandling(PATH_TO_CACHED_FORECASTS, self.saved_forecasts)
        fh.writetofile()

    def print_forecast(self, msg):
        print('\t', msg)
