import robin_stocks as rs

def signin(username,password):
    rs.login(username=username, password=password, expiresIn=86400, by_sms=True)
                #Above. username and password might not work unless passed in quotes.
def dipmethod():
        # method for determining when a stock is dipping
        # will be used in the while loop to alert the "buy" function of a 5 percent dips.
        # Return either buy or hold

def quarterbuy(investmenttotal):
    return investmenttotal/4

def marketorder(ticker, amount):
    #this is setup to buy crypto for testing purposes.
    #need to figure out how to pass ticker from the function into the buy order as a string.
                                        #below-\/- This needs to be send to robinhood in quotes i think.
    rs.orders.order_buy_crypto_by_quantity("ticker", 20, timeInForce='gtc')
                                                #    /\ above- this is the number of shares/coins purchased.
                                                #     I havent been able to buy in dollars yet. just shares.
                                                #reveived error ['Order quantity has invalid increment.']

def limitsell(percentage):
    #creates a limit order at the percentage above buy price passed to the function.
    #uses buyprice function to determine marketprice. Multiply by 1.15. then create limit order at that price.

def limitorderstatus():
    #used for determining the status of the highest limit order set for this ticker.
    #The idea is that this will be used in the while loop to determine if further buys are to take place.
    #returns executed or unexecuted.
    return "executed"
def buyprice():
    #Method for simplifying the way a buy price is determined.

buycount = 0

#setup code. Not sure where to put this.

#ask for username and password.
Username = input("Robinhood Username")
print(Username)
Password = input("Enter password")
print("********************")
signin(Username,Password)
print("Enter Text Code")

MainTicker= input("Please enter the ticker to buy. All Caps")
PercentGain= input("Please enter the percent gain to sell at. Int only no percent sign")
InvestmentTotal= input("Enter your total investment in the stock.")








while buycount < 4 and limitorderstatus() is not "executed" :
    if dipmethod() == "buy":
        marketorder(MainTicker,quarterbuy(InvestmentTotal))
        limitsell(PercentGain) #passes percentgain to the limitsell function to create limit order 15% above current market.
        buycount += 1

    else:
        dipmethod()





