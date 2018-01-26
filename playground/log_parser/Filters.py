#from playground.log_parser import Log


class Filters():

    def minor_filter(data, field, value):
        filtered_list = []
        if type(value) in [list, set, tuple]:
            for v in value:
                counter = 0
                for item in self.data:
                    if item[field] == v:
                        counter += 1
                        filtered_list.append(item)
                if counter > 0:
                    print(f"I just found {counter} matches for {field}='{v}'")
                else:
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
                print(f"No matches for {field}='{value}'")
        return filtered_list

    def filter(data, ftype, **filters):
        filter_result = []
        # Check filter type
        if ftype not in ['AND','OR','EXC']:
            print(f"You probably set incorrect filter type '{ftype}.'\n"
                  "Try to set 'AND' or 'OR' or 'EXC'.")
            quit()

        # Check filters
        if len(filters) == 0:
            print("Looks like you didn't set any filter. I couldn't help you without filters.")
            quit()
        possible_keys = set(data[0].keys())
        incorrect_keys = set(filters.keys()) - possible_keys
        if len(incorrect_keys) > 0:
            for field in incorrect_keys:
                del filters[field]
            print(f"I noticed that you set the wrong fields: {incorrect_keys}. "
                  f"Try to use these: {possible_keys}.")

        # get data for comparing, which includes all minor filtering results
        for key, value in filters.items():
            filter_result = []
            filter_result.append(Filters.minor_filter(data, key, value))

        if ftype == 'AND':
            # check if all filters have mathces
            if [] in filter_result:
                data = None
                print("The filters intersection gives nothing.")

            data = list(filter_result[0])
            t_data = list(data)
            for item in t_data:
                for minor_filtering_result in filter_result:
                    if item not in minor_filtering_result:
                        data.remove(item)
            t_data = None
            if len(data) > 0:
                print("The data was successfully filtered.")
            else:
                print("The filters intersection gives nothing.")
        elif ftype == 'OR':
            data = []
            for minor_filtering_result in filter_result:
                for item in minor_filtering_result:
                    if item not in data:
                        data.append(item)
            print("The data was successfully filtered.")
        elif ftype == 'EXC':
            for minor_filtering_result in filter_result:
                for item in minor_filtering_result:
                    if item in data:
                        data.remove(item)
            if len(data) > 0:
                print("The data was successfully filtered.")
            else:
                print("The filters intersection gives nothing.")
        return data



#FILE_ADRESS = "C:\\Users\\roman.sysiuk\\Desktop\\Logs\\Audit_USHDC0155_2018-01-17.log"
#log = Log(FILE_ADRESS).data
#print(log)

#f = Filters.filter(log, 'AND', Type='Document')


