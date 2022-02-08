import sys
import os
from datetime import date
from datetime import timedelta

PATH_TO_CACHED_FORECASTS = './cache/cachedforecasts.txt'

ARGS_ERROR = '\n' \
             'Niewlasciwa liczba argumentow: weather2.py + {} arg.\n' \
             'Poprawne wywolanie programu:\n' \
             '\tweather2.py <klucz_do_api> [<data>]\n' \
             'Jesli nie podano argumentu opcjonalnego <data> program ' \
             'sprawdza pogode na jutro.'.format(len(sys.argv) - 1)

FORECAST_SAVED = '\nZapisano prognoze dla: '

FORECAST_FOUND = '\nPrognoza dla: '

FORECAST_NOT_FOUND = '\nNie znaleziono prognozy dla: '

SAVED_FORECAST_DATES = '\nPrognozy zapisane dla nastepujacych dni:'

END_OF_PROGRAM = '\nKoniec dzialania programu.'

MSGS = {0: ARGS_ERROR,
        1: FORECAST_FOUND,
        2: FORECAST_SAVED,
        3: FORECAST_NOT_FOUND,
        4: SAVED_FORECAST_DATES,
        5: END_OF_PROGRAM}


class Arguments:
    def __init__(self):
        self.args = sys.argv

    def set_args(self):
        args_len = len(self.args)
        if args_len in range(2, 4):
            if args_len == 2:
                self.args.append(str((date.today()
                                      + timedelta(1)).strftime('%Y-%m-%d')))
            self.args = self.args[1:]
            return True
        else:
            self.prints(0)
            return False

    def prints(self, i):
        msg = MSGS[i]
        if i in range(1, 4):
            msg += self.args[1]
        print(msg)


class FileHandling:
    def __init__(self, path_to_file, object_to_save=None):
        self.path_to_file = path_to_file
        self.object_to_save = object_to_save

    def readfromfile(self):
        if os.path.exists(self.path_to_file):
            with open(self.path_to_file, 'r', encoding='utf-8') as f:
                while True:
                    line = f.readline().strip()
                    if not line:
                        break
                    description = f.readline().strip()
                    yield line, description

    def writetofile(self):
        with open(self.path_to_file, 'w', encoding='utf-8') as f:
            for elem in self.object_to_save:
                for i in range(2):
                    f.write(str(elem[i]) + '\n')
