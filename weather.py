import requests


def get_weather(city_name, forecast_date):
    url = 'https://www.metaweather.com/'
    eng_city_name = str(city_name)
    eng_city_name = eng_city_name.lower()

    print(forecast_date)
    print(eng_city_name)

    woeid = requests.get(url + 'api/location/search/?query=' + eng_city_name).json()

    forecast_date = forecast_date.lstrip()
    forecast_date = forecast_date.rstrip()
    forecast_date = forecast_date.replace(' ', '/')

    weather = requests.get(url + 'api/location/' + str(woeid[0]['woeid']) + '/' + forecast_date + '/').json()
    # weather = requests.get(url + 'api/location/' + str(woeid[0]['woeid']) + '/').json()

    forecast = weather[0]

    for el in forecast:
        print(el, ': ', forecast[el])

    return_forecast = ''

    for el in forecast:
        return_forecast += str(el) + ':' + str(forecast[el])

    for el in forecast:
        return return_forecast

    # except:
    #     return 'Sorry, we cannot provide weather information for this region or for this date'

# cityName = (input('Input city name: '))
# cityName = cityName.lower()
#
# forecastDate = input('Input forecast date (format: yyyy mm dd): ')
# outputDate = forecastDate
# forecastDate = forecastDate.lstrip()
# forecastDate = forecastDate.rstrip()
# forecastDate = forecastDate.replace(' ', '/')
#
# url = 'https://www.metaweather.com/'
#
# try:
#     woeid = requests.get(url + 'api/location/search/?query=' + cityName).json()
#     print('Weather in', woeid[0]['title'], 'on ', outputDate)
#
#     print()
#
#     weather = requests.get(url + 'api/location/' + str(woeid[0]['woeid']) + '/' + forecastDate + '/').json()
#
#     forecast = weather[0]
#
#     for el in forecast:
#         print(el, ': ', forecast[el])
#
#
# except:
#     print('Sorry, we cannot provide weather information for this region or for this date' )
