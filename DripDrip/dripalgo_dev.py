import random



days = 21
amount_capital = 10000

sampleList = ["XRP", "BTC", "ADA", "SOL"]
weights = [70, 50, 20, 10]
  
randomList = random.choices(sampleList, weights=weights, k=amount_capital)
  
xrp_count = randomList.count("XRP")
btc_count = randomList.count("BTC")
ada_count = randomList.count("ADA")
sol_count = randomList.count("SOL")

days_amount = xrp_count / days, btc_count / days, ada_count / days, sol_count / days

xrp = days_amount[0]
btc = days_amount[1]
ada = days_amount[2]
sol = days_amount[3]

x = 0
b = 0
a = 0
s = 0

print("Run --", days_amount, "\n")


for i in range(1, days + 1):
    
    x += xrp
    b += btc
    a += ada
    s += sol

    print("Day:",i , round(x,2), round(b,2), round(a,2), round(s,2))


print("\nTotal -----", x, b, a, s)
print("=", x + b + a + s)
