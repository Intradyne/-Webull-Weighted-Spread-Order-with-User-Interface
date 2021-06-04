from webull.webull import webull
wb = webull()

# user_code(
#      spread_order is the highest level command and can be called with only 3 arguments
#      spread_order(100,10,5) # will yield a spread of default 7 levels between $5 and $10
#      quantity will be 100 stocks they will be weighted toward the cheaper levels
#      spread_order(100,10,5,w=.1) # w is the weight, at .1 it would be nearly linear
#      finally you can place weighted orders on all these levels with one command
#      spread_order(100,10,5,w=2,sym='SPCE') # more aggressive curve, w=2, not required
#      spread_order calls spread() which creates pairs of levels and weighted #s of stocks
#      then parses the order_list with order_l() which also prints info to the console
#       )

log = False
def getuser():
    global log
    if log:
         return True
    else:
        wb.login('email@gmail.com', 'pa$$word')
        wb.get_trade_token('6-digit-pin')
        print('~~~Logged~~~')
        log = True


def spread_order(Nstocks, hi, lo, lvl=7, w=1, ticker=False, verbose=True):
    # order_list created by spread() sent to order_l()
    # print(Nstocks, hi, lo, lvl, w, ticker)
    if ticker!=False & log==False:
        getuser()
    if int(Nstocks) < 0:
        order_l(spread(-Nstocks, hi, lo, lvl, w), ticker, verbose, 'SELL')
    else:
        order_l(spread(Nstocks, hi, lo, lvl, w), ticker, verbose)


def spread(Nstocks, hi, lo, lvl=7, w=1):
    # creates pairs of levels and weighted #s of stocks

    order_list = {}
    spread = hi - lo
    q = spread/(lvl-1)    # $ between levels

    for x in range(lvl):  # for loop gives each level a weighted value
        y = x/lvl         # y will be the exponentiated
        # below starts lo counts by q, w to skew storing the $value as the key and weight as the element
        order_list[round(lo+(x*q), 2)] = ((-y*y)+1)**w 

    z = sum(order_list.values()) # sum of weights

    for key in order_list:     # converts weighted values to stock numbers
        a = order_list[key]                       # weighted value
        err = (a/z * Nstocks)-int(a/z * Nstocks)  # mostly correcting for rounding
        order_list[key] = int(err+a/z * Nstocks)  # find # of stocks
    return order_list

def order_l(order_list, ticker=False, verbose=False, action='BUY'):
    # orders from an order_list object created by spread()

    if ticker:
        for key in order_list:
            print(ticker, key, order_list[key], action)
            print(wb.place_order(stock=ticker, price=key, quant=order_list[key], action=action))

    # below prints information to console
    if verbose:
        print('------------------------')
        print('[ Level ][ N ] $ Level*n')
        n = 0 # $$.$$ counter used to calculate average
        for key in order_list:
            print('[', key, '] [', order_list[key], '] $', round(key*order_list[key], 2))
            n = key * order_list[key] + n
        print('------------------------')
        print('N_stocks    |', sum(order_list.values())) # give or take 1
        print('$ Max Spent |', round(n, 2))
        print('$ Avg.      |', round(n/sum(order_list.values()), 2))

if __name__ == "__main__":
    wb.place_order(quant=1, price=10.0, action='buy', tId=913254559)
    # user_code()
    # spread_order(10, 10, 5, w=.1, ticker='AMD')
