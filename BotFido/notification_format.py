

def data_format(data, dataName):
    """ Text format for the read data func. """

    txt1 = ""
    txt2 = ""
    txt_combined = ""

    for d in data:

        txt1 = str(d)
        txt2 = str(data[d])

        txt_combined += '\n🔸'+txt1 + " : " + txt2 + "\n"

    txt_main = f"📑{dataName} \n\n{txt_combined}" 

    return txt_main




def logs_format(logs, logname):
    """ Text format for the calculation func. """

    txt1 = f"📜 {logname}: \n\n"
    txt2 = ""
    
    for log in logs:
        txt2 += "\n" + log

    return str(txt1 + txt2)