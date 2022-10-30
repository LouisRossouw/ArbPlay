

def buy_format(drip_data, coin, amount_coins_buy, amount):
    """ Text format for the calculation func. """

    day_count = drip_data["day_count"]
    days_total = drip_data["days_total"]

    txt1 = f"💎 DripDrip : {str(day_count)}/{str(days_total)}\n\n"
    txt2 = f"🚀Purchased Coin: {str(amount_coins_buy)}/{str(coin)} | @ R {str(amount)}"

    return str(txt1 + txt2)




def calculation_format(data, total, amount_capital, days):
    """ Text format for the calculation func. """

    txt = f"🔸 Setting New Calcuation plan. 🔸\n\nR{str(amount_capital)} @ {str(days)} days:\n\n"
    count = -1

    for coin in data:
        count += 1
        txt += f"{coin}: R{data[coin]} = R{total[count]} \n"

    return str(txt)








if __name__ == "__main__":

    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import BotFido.BotNotifications as BOTNOT

    drip_data = {}
    drip_data["day_count"] = 3
    drip_data["days_total"] = 20

    coin = "XRP"
    amount_coins_buy = 64
    amount = 800

    txt = buy_format(drip_data, coin, amount_coins_buy, amount)
    BOTNOT.BotNotification().send_ADMIN_notification(text=txt)