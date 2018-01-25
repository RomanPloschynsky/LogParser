class Filter():

    def __init__(self, data_to_filter, ftype = 'AND', **filters):
        self.data = data_to_filter
        self.filters = filters
        self.ftype = ftype
        self.filter_result = []
        self.isAND = True

        if len(filters) > 0:
            self.dumb_filter()
            self.dumb_compare()

    def _minor_filter(self, field, value):
        filtered_list = []
        if type(value) in [list, set, tuple]:
            for v in value:
                counter = 0
                for item in data:
                    if item[field] == v:
                        counter += 1
                        filtered_list.append(item)
                if counter > 0:
                    print(f"I just found {counter} matches for {field}='{v}'")
                else:
                    self.isAND = False
                    print(f"No matches for {field}='{v}'")
        else:
            counter = 0
            for item in data:
                if item[field] == value:
                    counter += 1
                    filtered_list.append(item)
            if counter > 0:
                print(f"I just found {counter} matches for {field}='{value}'")
            else:
                self.isAND = False
                print(f"No matches for {field}='{value}'")
        return filtered_list

    def dumb_filter(self):

        # Check filters
        if len(self.filters) == 0:
            print("Looks like you didn't set any filter. I couldn't help you without filters.")
            quit()
        possible_keys = set(self.data[0].keys())
        incorrect_keys = set(self.filters.keys()) - possible_keys
        if len(incorrect_keys) > 0:
            for field in incorrect_keys:
                del self.filters[field]
            print(f"I noticed that you set the wrong fields: {incorrect_keys}. "
                  f"Try to use these: {possible_keys}.")

        for key, value in self.filters.items():
            self.filter_result.append(self._minor_filter(key, value))

    def dumb_compare(self, ftype=None):

        if ftype is not None:
            self.ftype = ftype

        if self.ftype == 'AND' and self.isAND == False:
            self.data = None
            print("The filters intersection gives nothing.")
        elif self.ftype == 'AND':
            self.data = list(self.filter_result[0])
            t_data = list(self.data)
            for item in t_data:
                for minor_filtering_result in self.filter_result:
                    if item not in minor_filtering_result:
                        self.data.remove(item)
            t_data = None
            if len(self.data) > 0:
                print("The data was successfully filtered.")
            else:
                print("The filters intersection gives nothing.")
        elif self.ftype == 'OR':
            self.data = []
            for minor_filtering_result in self.filter_result:
                for item in minor_filtering_result:
                    if item not in self.data:
                        self.data.append(item)
            print("The data was successfully filtered.")
        elif self.ftype == 'EXC':
            for minor_filtering_result in self.filter_result:
                for item in minor_filtering_result:
                    if item in self.data:
                        self.data.remove(item)
            if len(self.data) > 0:
                print("The data was successfully filtered.")
            else:
                print("The filters intersection gives nothing.")
        else:
            print(f"You probably set incorrect filter type '{self.ftype}.'\n"
                  "Try to set 'AND' or 'OR' or 'EXC'.")
            self.data = []
        self.filter_result = None







data = [{'a':'1', 'b':'1'},{'a':'2', 'b':'2'},{'a':'3', 'b':'3'}]

c = Filter(data_to_filter=data, ftype='EXC', a='1', b='2')

print("data: ", c.data)





