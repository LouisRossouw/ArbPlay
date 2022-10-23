import os
import json




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




if __name__ == "__main__":


    CHECK_get_percentage_difference = False
    CHECK_percent_increase = True
    # 1.2%

    if CHECK_get_percentage_difference == True:
        # buy on Kucoin / sell on Valr ("sell_valr", "ask_kucoin")
        print(get_percentage_difference(1981.5, 1957.88))

    if CHECK_percent_increase == True:
        print(percent_increase(1.7, 50000))