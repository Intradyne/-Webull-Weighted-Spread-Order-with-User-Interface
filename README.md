# Webull Weighted Spread Order with User Interface

 Project to place multiple orders within a given price range and weight quantity towards a favored price

------------------------

## Requirements

Tkinter and tedchou12/webull python api

------------------------

### Example

This order with 10 buy in levels buys more the lower the dip

![UI IMG](https://github.com/Intradyne/-Webull-Weighted-Spread-Order-with-User-Interface/blob/main/UI.jpg)

Clicking the preview order button will return the following in the terminal and not try to log in to webull. Note that a negative quantity will be a sell order and the higher price should be the favored value.

```bash
[ Level ][ N ] $ Level*n     
[ 50.0 ] [ 13 ] $ 650.0      
[ 61.11 ] [ 13 ] $ 794.43
[ 72.22 ] [ 13 ] $ 938.86
[ 83.33 ] [ 12 ] $ 999.96
[ 94.44 ] [ 12 ] $ 1133.28
[ 105.56 ] [ 11 ] $ 1161.16
[ 116.67 ] [ 9 ] $ 1050.03
[ 127.78 ] [ 8 ] $ 1022.24
[ 138.89 ] [ 6 ] $ 833.34
[ 150.0 ] [ 4 ] $ 600.0
------------------------
N_stocks    | 101       # <--Whoops
$ Max Spent | 9183.3
$ Avg.      | 90.92
```

### Commands

Behind the scenes the UI is sending the inputs to the function spread_order

```python
#      spread_order is the highest level command and can be called with only 3 arguments
    spread_order(100,10,5) # will yield a spread of default 7 levels between $5 and $10
#      quantity will be 100 stocks they will be weighted toward the cheaper levels
    spread_order(100,10,5,w=.1) # w is the weight, at .1 it would be nearly linear
#      finally you can place weighted orders on all these levels with one command
    spread_order(100,10,5,w=2,sym='SPCE') # more aggressive curve, w=2, not required
#      spread_order calls spread() which creates pairs of levels and weighted #s of stocks
#      then parses the order_list with order_l() which also prints info to the console
```

But where the real magic happens is when the command spread() is called, this is where my slightly bugged algorithim splits an order into the requested number of levels across the spread of price ranges, assigning each an exponentially weighted value, then converts the float to an int # of stocks

```python
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
```

## License
[MIT](https://choosealicense.com/licenses/mit/)