import robin_stocks as rs
import time


def signin(username, password):
    rs.robinhood.login(username=username, password=password, expiresIn=86400, by_sms=True)


def currentstockprice(ticker):
    # returns stock price as float.
    currentprice = rs.robinhood.stocks.get_latest_price(ticker, includeExtendedHours=True)
    currentprice = float(currentprice[0])
    return currentprice


def percentchange(ticker, initialprice):
    # ----------------------------------------------------------------------------
    currentprice = rs.robinhood.stocks.get_latest_price(ticker, includeExtendedHours=True)
    currentprice = float(currentprice[0])
    # below. calculates the percentage difference between current and 2 second old price.
    percentagedifference = float(((currentprice - initialprice) / initialprice) * 100)
    # numbers retured match actual % so a 1.5 will represent 1.5%. 2.5 = 2.5% ect.
    # ----------------------------------------------------------------------------
    return percentagedifference


def percentchangecontinuous(ticker, numberofcycles, updatespeed):
    x = 0
    while numberofcycles > x:
        initialprice = rs.robinhood.stocks.get_latest_price(ticker, includeExtendedHours=True)
        initialprice = float(initialprice[0])
        time.sleep(updatespeed)
        currentprice = rs.robinhood.stocks.get_latest_price(ticker, includeExtendedHours=True)
        currentprice = float(currentprice[0])
        # below. calculates the percentage difference between current and 2 second old price.
        percentagedifference = float(((currentprice - initialprice) / initialprice) * 100)
        # numbers retured match actual % so a 1.5 will represent 1.5%. 2.5 = 2.5% ect.
        x += 1
        return percentagedifference


def stoplimitsell(ticker, quantity, limitprice, stopprice, tif, extended):
    stoplimit = rs.robinhood.order_buy_stop_limit(ticker, quantity, limitprice, stopprice, tif, extended)
    stoplimitid = stoplimit['id']
    return stoplimitid


def stoplimitbuy(ticker, quantity, limitprice, stopprice, tif, extended):
    stoplimit = rs.robinhood.order_sell_stop_limit(ticker, quantity, limitprice, stopprice, tif, extended)
    stoplimitid = stoplimit['id']
    return stoplimitid


def trailingbuy(ticker, quantity, trailamount, trailtype, tif):
    stoplimit = rs.robinhood.orders.order_buy_trailing_stop(ticker, quantity, trailamount, trailtype, tif)
    stoplimitid = stoplimit['id']
    return stoplimitid


def trailingsell(ticker, quantity, trailamount, trailtype, tif):
    stoplimit = rs.robinhood.orders.order_sell_trailing_stop(ticker, quantity, trailamount, trailtype, tif)
    stoplimitid = stoplimit['id']
    return stoplimitid


def cancel(orderid):
    print(rs.robinhood.orders.cancel_stock_order(orderid))


def limitpricecalc(currentprice, percentage):
    # a price matching the percentage of the current price passed to it.
    percentage = float((percentage * .01) + 1)
    limitprice = currentprice * percentage
    return limitprice


def stoppricecalc(currentprice, percentage):
    percentage = float((percentage * .01) + 1)
    stopprice = currentprice * percentage
    return stopprice


def orderfilledcheck(orderid):
    # checks to see if the order is filled.
    # returns either queued, filled, cancelled,
    orderinfo = rs.robinhood.orders.get_stock_order_info(orderid)
    isfilled = orderinfo['state']
    return isfilled


signin("superseth5374@yahoo.com", "____________")
ticker = input("enter ticker")
print("This is the current price of " + ticker)
print(currentstockprice(ticker))
price = float(input("Enter reference price for stock."))
shares = input("number of shares to purchase")
trailordertype = "percentage"  # dollars or percentages
trailamount = input("Trailing amount")  # trailing buy and sell percentage
orderid = "blank"
ext = True  # input("set orders for extended hours? 0 for True or 1 for False")

print("test")
while True:

    time.sleep(3)
    percent = percentchange(ticker, price)
    print("Percent Change")
    print(percent)
    print("Current Price")
    print(currentstockprice(ticker))
    if percent > 1:
        print("***Positive price change detected.****")
        # below. Submits new order and assigns the returned orderid to the variable orderid.
        orderid = trailingsell(ticker, shares, trailamount, trailordertype, "gfd")
        while orderfilledcheck(orderid) != "filled" and orderfilledcheck(orderid) != "cancelled":  # checks to make the order isnt filled
            percent = percentchange(ticker, price)
            if percent < 0:  # if the stock drops below its reference price the order is canceled.
                cancel(orderid)
                print("Order cancellation sent due to price now dropping.")
                time.sleep(7)
                while orderfilledcheck(orderid) != "cancelled":  # checks orderstatus at 1 sec intervals
                    print("Order cancellation waiting....")     # until the order is actually canceled.
                    time.sleep(1)
                print("Order cancellation complete. Returning to stock monitor")  # prints when status is cancelled.
            print("Waiting for sell order to fill")
            print("Current Price")
            print(currentstockprice(ticker))
            print("Reference Price")
            print(price)
            time.sleep(1)
        if orderfilledcheck(orderid) == "filled":  # confirms that the order has been filled
            print("$$$ SELL ORDER FILLED $$$")
            price = float(input("Enter New Reference Price For"+ticker))  # placeholder until i can figure out how to
    if percent < -1:                                                      # determine the new reference point.
        print("-----Negative price change detected-----")
        orderid = trailingbuy(ticker, shares, trailamount, trailordertype, "gfd")
        while orderfilledcheck(orderid) != "filled" and orderfilledcheck(orderid) != "cancelled":
            percent = percentchange(ticker, price)
            if percent > 0:
                cancel(orderid)
                print("Order cancellation sent due to price now rising.")
                time.sleep(7)
                while orderfilledcheck(orderid) != "cancelled":
                    print("Order cancellation waiting....")
                    time.sleep(1)
                    print("Order cancellation complete. Returning to stock monitor")
            print("Waiting for buy order to fill")
            print("Current Price")
            print(currentstockprice(ticker))
            print("Reference Price")
            print(price)
            time.sleep(1)
        if orderfilledcheck(orderid) == "filled":
            print("$$$ BUY ORDER FILLED $$$")
            price = float(input("Enter New Reference Price For"+ticker))
    print("waiting for significant change in " + ticker + " price")


