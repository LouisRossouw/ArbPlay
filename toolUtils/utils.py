import math
import json
import datetime
import calendar



def round_down_float(value):
    """ Rounds down a 2 decimal value to the lowest number. """
    return math.floor(float(value) * 100)/100.0



def write_to_json(json_path, data):
    """ Create and write to json file """

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=6)




def read_json(json_path):
    """ Reads json file """

    with open(json_path) as f:
        json_file = json.loads(f.read())

    return (json_file)




def get_percentage_difference(new_value, original_value):
    """ finds the percentage difference between new number and original """

    output_value = ((float(new_value) - float(original_value)) / float(original_value)) * 100

    return(output_value)




def percent_increase(percent, input_value):
    """ adds a percent to a value and returns it"""
    
    output_value = float(((input_value / 100) * float(percent)) + float(input_value))

    return(float(output_value))




def get_dates():
    """ Returns a lot of date stuff! """

    # Date functions
    date_now_full = (str(datetime.datetime.now()))
    date_now = (str(datetime.datetime.now()).split(' ')[0])
    date_time = (str(datetime.datetime.now()).split(' ')[1])
    day_num = datetime.datetime.today().day
    day_name = calendar.day_name[datetime.date.today().weekday()]
    date_year = datetime.datetime.today().year
    day_month_num = datetime.datetime.today().month
    day_month_name = calendar.month_name[day_month_num]

    dict = {}
    dict['date_NOW'] = [date_now, date_time, 
                        day_num, day_name, date_year, 
                        day_month_num, day_month_name, date_now_full]
    
    return(date_now, date_time, day_num, day_name, 
           date_year, day_month_num, day_month_name, dict, date_now_full)




if __name__ == "__main__":


    CHECK_get_percentage_difference = False
    CHECK_percent_increase = False
    GET_DATES = True
    # 1.2%

    if CHECK_get_percentage_difference == True:
        # buy on Kucoin / sell on Valr ("sell_valr", "ask_kucoin")
        print(get_percentage_difference(1981.5, 1957.88))

    if CHECK_percent_increase == True:
        print(percent_increase(1.7, 50000))

    if GET_DATES == True:
        print(get_dates()[1].split(":")[0])