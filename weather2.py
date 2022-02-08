from classes.weatherforecast import WeatherForecast
from classes.argsconstsfiles import Arguments

arguments = Arguments()
if arguments.set_args():
    wf = WeatherForecast(arguments.args[0])
    if wf[arguments.args[1]]:
        arguments.prints(1)
        wf.print_forecast(wf.searched_forecast)
        if wf.is_forecast_from_api:
            wf[arguments.args[1]] = wf.searched_forecast
            wf.write_saved_forecasts_to_file()
            arguments.prints(2)
    else:
        arguments.prints(3)
        arguments.prints(4)
        for elem in wf:
            wf.print_forecast(elem)

        # generator tupli - tylko po to zeby pokazac, ze dziala (nie jest
        # tu potrzebny, wykorzystywany jest wewnatrz klasy WeatherForecast)
        wf.print_forecast('-' * 60)
        for elem in wf.items():
            wf.print_forecast(elem)

arguments.prints(5)
