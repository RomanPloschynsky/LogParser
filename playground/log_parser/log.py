from playground.log_parser.Filters import Filters

class Log():
    __private_data = []

    def __init__(self, file, separator='\t'):
        self.file = file
        self.separator = separator

        self.get_file_data()

    def get_file_data(self):
        try:
            with open(self.file, 'r') as file:
                keys = next(file).split(self.separator)
                for line in file:
                    for line in file:
                        values = line.split(self.separator)
                        self.__private_data.append(dict(zip(keys, values)))
        except FileNotFoundError:
            print(f"Couldn't find {self.file}")
            quit()
        except TypeError:
            print("Separator must be str or None")
            quit()
        except ValueError:
            print("Separator must be str or None")
            quit()

    def filter(self, ftype='AND', **filters):
        self.__private_data = Filters.filter(data=self.__private_data, ftype=ftype, **filters)

    def compose(self, *columns):

        uncomposed_data = list(self.__private_data); self.__private_data = []
        composed_data = {}

        setted_columns = set(columns)
        possible_columns = set(uncomposed_data[0].keys())
        incorrect_columns = setted_columns - possible_columns

        # check if there are columns in table
        if len(incorrect_columns) > 0:
            print("I noticed that you set the wrong columns to display:")
            for column in incorrect_columns:
                print(f'\t{column}')
                setted_columns.remove(column)
            print(f"I found some columns you could use: {possible_columns}")

        if len(setted_columns) == 0:
            print("Looks like we have no columns to show you now")
            quit()
        else:
            print(f"I'll show you next columns: {setted_columns}")
            pass


        # create table with setted columns
        for line in uncomposed_data:
            for column in setted_columns:
                composed_data[column] = line[column]
            self.__private_data.append(composed_data)
            self.__private_data = [dict(composed_data) for composed_data in set([tuple(data.items()) for data in self.__private_data])]

    def get_data(self):
        return self.__private_data





