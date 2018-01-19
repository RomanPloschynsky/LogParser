from time import sleep
from itertools import groupby

FILE_ADRESS = "C:\\Users\\roman.sysiuk\\Desktop\\Logs\\Audit_USHDC0155_2018-01-17.log"
APP_NAME = "\\\\USHDC0160\\QLIK\\USER_DOCUMENTS\\staffit.qvw"


class Log():

    _data = []

    def __init__(self, file, *args, ftype='AND', **kwargs):
        self._file = file
        self._args = args
        self._ftype = ftype
        self._kwargs = kwargs

        self._get_file_data()

        if len(self._args) > 0:
            self.compose()

        if len(self._kwargs) > 0:
            self.filter()

    def _get_file_data(self):
        with open(self._file, 'r') as file:
            for line in file:
                _values = line.split('\t')
                _server_started = _values[0]
                _timestamp = _values[1]
                _document = _values[2]
                _type = _values[3]
                _user = _values[4]
                _message = _values[5]
                _id = _values[6]
                _session = _values[7]
                self._data.append({'server_started':_server_started,
                                   'timestamp':_timestamp,
                                   'document':_document,
                                   'type':_type,
                                   'user':_user,
                                   'message':_message,
                                   'id':_id,
                                   'session':_session})

    def compose(self, *args):
        if len(args) > 0:
            self._args = args

        composed_data_minor = {}
        composed_data = []
        keys = []

        # check if there are columns in table
        for arg in self._args:
            if arg in self._data[0]:
                keys.append(arg)

        # create table with columns from args
        for line in self._data:
            for key in keys:
                composed_data_minor[key] = line[key]
            composed_data.append(composed_data_minor)
        self._data = list(composed_data)
        composed_data_minor = None
        composed_data = None
        keys = None

    # auxiliary function creates list from inputed list, which has mutches with inputed filters
    @staticmethod
    def _dumb_filtering(data_to_filter, key, value):
        filtering_result = []
        c = 0
        # check if there are more then one value for the filter's key
        if type(value) == list or type(value) == set or type(value) == tuple:
            print(value)
            for v in value:
                for row in data_to_filter:
                    if row[key] == v:
                        filtering_result.append(row)
                        c += 1
                print(f"I just found {c} matches for {key} = '{v}'")
        else:
            print(value)
            for row in data_to_filter:
                if row[key] == value:
                    filtering_result.append(row)
                    c += 1
            print(f"I just found {c} matches for {key} = '{value}'")
        return filtering_result

    @staticmethod
    def _filtering_or(data_to_filter, filters):
        filtering_result = []
        for key, value in filters.items():
            filtering_result += Log._dumb_filtering(data_to_filter, key, value)
        print("Filtering was finished successfully")
        return [el for el, _ in groupby(filtering_result)]

    @staticmethod
    def _filtering_and(data_to_filter, filters):
        if len(filters) > 1:
            key, value = filters.popitem()
        else:
            for key, value in filters.items():
                key = key
                value = value
        filtering_result = Log._dumb_filtering(data_to_filter, key, value)
        temp_table = list(filtering_result)
        for key, value in filters.items():
            minor_filter_table = Log._dumb_filtering(data_to_filter, key, value)
            for item in temp_table:
                if item not in minor_filter_table and item in filtering_result:
                    filtering_result.remove(item)
        print("Filtering was finished successfully")
        return filtering_result

    @staticmethod
    def _filtering_exc(data_to_filter, filters):
        filtering_result = data_to_filter
        for key, value in filters.items():
            minor_filter_table = Log._dumb_filtering(data_to_filter, key, value)
            for item in minor_filter_table:
                if item in filtering_result:
                    filtering_result.remove(item)
        print("Filtering was finished successfully")
        return filtering_result

    def filter(self, ftype='AND', **kwargs):
        # check if there are any filters
        if len(kwargs) > 0:
            self._kwargs = kwargs
            print(type(self._kwargs), self._kwargs)

        if len(self._kwargs) == 0:
            print("No filters was setted.\n"
                  "Try one more time with parameters:\n"
                  "\tkey='value', key={'value','value'}, ...")

        # check if the filter type was setted correctly
        if ftype not in ['AND','OR','EXC']:
            print(f"You probably set incorrect filter type '{ftype}'\n"
                  "Try to set 'AND' or 'OR' or 'EXC'.\n"
                  "Or don't set any type and we will choose it randomly.\n"
                  "Just joking.) We have allready set 'AND' type by default")

        # check if filters are in table columns
        filters = {}
        keys = []
        for key in self._data[0]:
            keys.append(key)
        print("I'm checking the filters:")
        for k, v in self._kwargs.items():
            if k not in keys:
                print(f"\tThere is no column '{key}' in table")
            else:
                print(f"\tFilter '{key}' is OK")
                filters[k] = v
        if len(filters) > 0:
            self._kwargs = dict(filters)
        else:
            print("All your filters are incorrect\n"
                  f"Try to use one of these: {keys}\n")
            quit()
        filters = None
        keys = None


        if self._ftype == 'AND':
            Log._filtering_and(self._data, self._args)
        elif self._ftype == 'OR':
            Log._filtering_and(self._data, self._args)
        elif self._ftype == 'EXC':
            Log._filtering_and(self._data, self._args)
        else:
            print(f"Incorrect filter type {self._ftype}."
                  f"Try to use 'AND', 'OR', 'EXC'."
                  f"Also there is something wrong eith prigram. 'couse you shouldn't get this error")








l = Log(FILE_ADRESS, 'id','message',
            message='Close',
#            user='US\\shchitnis',
#            id='Document\\SH_Landing',
#            idq='Document\\SH_Landingt',
#            document=('\\\\USHDC0160\\QLIK\\USER_DOCUMENTS\\StafFit.qvw','\\\\ushdc0160\\qlik\\UserDocuments\\My_Clients\\My Clients.qvw','','1')
        )
#l.compose('id')
#l.filter(message='Open')
print(l._data)


