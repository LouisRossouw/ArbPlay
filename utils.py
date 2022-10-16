def get_percentage_difference(new_value, original_value):
    """ finds the percentage difference between new number and original """
    output_value = ((float(new_value) - float(original_value)) / float(original_value)) * 100
    return(output_value)




def percent_increase(percent, input_value):
    """ adds a percent to a value and returns it"""
    output_value = float(((input_value / 100) * float(percent)) + float(input_value))
    return(float(output_value))




if __name__ == "__main__":


    CHECK_get_percentage_difference = True
    CHECK_percent_increase = True


    if CHECK_get_percentage_difference == True:
        # buy on Kucoin / sell on Valr ("sell_valr", "ask_kucoin")
        print(get_percentage_difference(2550, 2500))

    if CHECK_percent_increase == True:
        print(percent_increase(0.1, 10000))