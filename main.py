import tkinter as tk
import time, cbpro


# ------- Define Global Variables -------- #
LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)
MID_FONT = ("Verdana", 10)
WS_URL = "wss://ws-feed-public.sandbox.pro.coinbase.com"        # SANDBOX
# WS_URL = "wss://ws-feed.pro.coinbase.com"
API_URL = "https://api-public.sandbox.pro.coinbase.com"  # SANDBOX
# API_URL = "https://api.pro.coinbase.com"
API_KEY = ""  # SANDBOX
# API_KEY = ""
API_SECRET = ""  # SANDBOX
# API_SECRET = ""
API_PASS = ""
auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASS, api_url=API_URL)
# ws_client = MyWebsocketClient()
public_client = cbpro.PublicClient()
client = [auth_client, public_client]
mode = 1           # set to 0 for real run, -1 or 1 for test run
quote_track = {'ETH-USD': [], 'BTC-USD': [], 'LTC-USD': []}
delay = 0       # used to run select parts every "delay" iterations
account_ids = {"USD": 0, "BTC": 0, "ETH": 0, "LTC": 0}
# --------------------------------------- #



def main():
    global account_ids
    if mode == 0:
        accounts = client[mode].get_accounts()  # returns an array of account dictionaries
        account_ids['USD'] = extract_account_id(accounts, "USD")
        account_ids['BTC'] = extract_account_id(accounts, "BTC")
        account_ids['ETH'] = extract_account_id(accounts, "ETH")
        account_ids['LTC'] = extract_account_id(accounts, "LTC")

    gui_loop()



def gui_loop():
    global BTC_limit_entry_box, ETH_limit_entry_box, LTC_limit_entry_box
    root = tk.Tk()
    root.geometry('600x300')
    root.title('Crypto-Trader by Kendall Ayers')

    container = tk.Frame(root)
    container.configure(background='black')
    container.pack(side="top", fill="both", expand=True)
    rows = cols = 0
    while rows < 10:
        container.rowconfigure(rows, weight=1)
        rows += 1
    while cols < 7:
        container.columnconfigure(cols, weight=1)
        cols += 1

    label = tk.Label(container, text="Crypto-Trader", font=LARGE_FONT, background="white")
    label.grid(row=1, column=3, sticky="n")

    BTC_buy_label = tk.Label(container, text="Buy BTC", font=MID_FONT, bg="black", fg="white")
    BTC_buy_label.grid(row=3, column=1)
    BTC_buy_label.bind('<Button-1>', place_BTC_buy)

    ETH_buy_label = tk.Label(container, text="Buy ETH", font=MID_FONT, bg="black", fg="white")
    ETH_buy_label.grid(row=5, column=1)
    ETH_buy_label.bind('<Button-1>', place_ETH_buy)

    LTC_buy_label = tk.Label(container, text="Buy LTC", font=MID_FONT, bg="black", fg="white")
    LTC_buy_label.grid(row=7, column=1)
    LTC_buy_label.bind('<Button-1>', place_LTC_buy)

    BTC_buy_fees_label = tk.Label(container, text="Fees Buy BTC", font=MID_FONT, bg="black", fg="white")
    BTC_buy_fees_label.grid(row=3, column=4)
    BTC_buy_fees_label.bind('<Button-1>', place_BTC_fees_buy)

    ETH_buy_fees_label = tk.Label(container, text="Fees Buy ETH", font=MID_FONT, bg="black", fg="white")
    ETH_buy_fees_label.grid(row=5, column=4)
    ETH_buy_fees_label.bind('<Button-1>', place_ETH_fees_buy)

    LTC_buy_fees_label = tk.Label(container, text="Fees Buy LTC", font=MID_FONT, bg="black", fg="white")
    LTC_buy_fees_label.grid(row=7, column=4)
    LTC_buy_fees_label.bind('<Button-1>', place_LTC_fees_buy)

    BTC_sell_label = tk.Label(container, text="Sell BTC", font=MID_FONT, bg="black", fg="white")
    BTC_sell_label.grid(row=3, column=2)
    BTC_sell_label.bind('<Button-1>', place_BTC_sell)

    ETH_sell_label = tk.Label(container, text="Sell ETH", font=MID_FONT, bg="black", fg="white")
    ETH_sell_label.grid(row=5, column=2)
    ETH_sell_label.bind('<Button-1>', place_ETH_sell)

    LTC_sell_label = tk.Label(container, text="Sell LTC", font=MID_FONT, bg="black", fg="white")
    LTC_sell_label.grid(row=7, column=2)
    LTC_sell_label.bind('<Button-1>', place_LTC_sell)

    BTC_sell_fees_label = tk.Label(container, text="Fees Sell BTC", font=MID_FONT, bg="black", fg="white")
    BTC_sell_fees_label.grid(row=3, column=5)
    BTC_sell_fees_label.bind('<Button-1>', place_BTC_fees_sell)

    ETH_sell_fees_label = tk.Label(container, text="Fees Sell ETH", font=MID_FONT, bg="black", fg="white")
    ETH_sell_fees_label.grid(row=5, column=5)
    ETH_sell_fees_label.bind('<Button-1>', place_ETH_fees_sell)

    LTC_sell_fees_label = tk.Label(container, text="Fees Sell LTC", font=MID_FONT, bg="black", fg="white")
    LTC_sell_fees_label.grid(row=7, column=5)
    LTC_sell_fees_label.bind('<Button-1>', place_LTC_fees_sell)

    BTC_limit_entry_box = tk.Entry(container)
    BTC_limit_entry_box.grid(row=3, column=3)

    ETH_limit_entry_box = tk.Entry(container)
    ETH_limit_entry_box.grid(row=5, column=3)

    LTC_limit_entry_box = tk.Entry(container)
    LTC_limit_entry_box.grid(row=7, column=3)


    try:
        while True:
            root.update_idletasks()
            root.update()
    except Exception as e:
        print(e)
        root.destroy()


def get_bid(coin):
    book = client[mode].get_product_order_book(coin, level=2)
    return float(book.get('bids')[0][0])


def get_ask(coin):
    book = client[mode].get_product_order_book(coin, level=2)
    return float(book.get('asks')[0][0])


def place_BTC_buy(event=None):
    client[mode].cancel_all(product='BTC-USD')
    if len(str(BTC_limit_entry_box.get())) > 1:
        price = float(BTC_limit_entry_box.get())
    else:
        price = get_ask('BTC-USD') - .01
    account = client[mode].get_account(account_ids['USD'])
    size = (float(account['balance']) - .1) / price
    size = truncate(size, 8)
    print(client[mode].buy(price=price, size=size, product_id='BTC-USD', post_only=True))  # limit order to buy size ETH at $price


def place_BTC_fees_buy(event=None):
    client[mode].cancel_all(product='BTC-USD')
    account = client[mode].get_account(account_ids['USD'])
    price = get_ask('BTC-USD')
    size = (float(account['balance']) - .1) / price
    size = truncate(size, 8)
    print(client[mode].buy(type='market', size=size, product_id='BTC-USD', post_only=False))


def place_ETH_buy(event=None):
    client[mode].cancel_all(product='ETH-USD')
    if len(str(ETH_limit_entry_box.get())) > 1:
        price = float(ETH_limit_entry_box.get())
    else:
        price = get_ask('ETH-USD') - .01
    account = client[mode].get_account(account_ids['USD'])
    size = (float(account['balance']) - .1) / price
    size = truncate(size, 8)
    print(client[mode].buy(price=price, size=size, product_id='ETH-USD', post_only=True))


def place_ETH_fees_buy(event=None):
    client[mode].cancel_all(product='ETH-USD')
    account = client[mode].get_account(account_ids['USD'])
    price = get_ask('ETH-USD')
    size = (float(account['balance']) - .1) / price
    size = truncate(size, 8)
    print(client[mode].buy(type='market', size=size, product_id='ETH-USD', post_only=False))


def place_LTC_buy(event=None):
    client[mode].cancel_all(product='LTC-USD')
    if len(str(LTC_limit_entry_box.get())) > 1:
        price = float(LTC_limit_entry_box.get())
    else:
        price = get_ask('LTC-USD') - .01
    account = client[mode].get_account(account_ids['USD'])
    size = (float(account['balance']) - .1) / price
    size = truncate(size, 8)
    print(client[mode].buy(price=price, size=size, product_id='LTC-USD', post_only=True))


def place_LTC_fees_buy(event=None):
    client[mode].cancel_all(product='LTC-USD')
    account = client[mode].get_account(account_ids['USD'])
    price = get_ask('LTC-USD')
    size = (float(account['balance']) - .1) / price
    size = truncate(size, 8)
    print(client[mode].buy(type='market', size=size, product_id='LTC-USD', post_only=False))


def place_BTC_sell(event=None):
    client[mode].cancel_all(product='BTC-USD')
    if len(str(BTC_limit_entry_box.get())) > 1:
        price = float(BTC_limit_entry_box.get())
    else:
        price = get_bid('BTC-USD') + .01
    account = client[mode].get_account(account_ids['BTC'])
    size = account['balance']
    print(client[mode].sell(price=price, size=size, product_id='BTC-USD', post_only=True))


def place_BTC_fees_sell(event=None):
    client[mode].cancel_all(product='BTC-USD')
    account = client[mode].get_account(account_ids['BTC'])
    size = account['balance']
    print(client[mode].sell(type='market', size=size, product_id='BTC-USD', post_only=False))


def place_ETH_sell(event=None):
    client[mode].cancel_all(product='ETH-USD')
    if len(str(ETH_limit_entry_box.get())) > 1:
        price = float(ETH_limit_entry_box.get())
    else:
        price = get_bid('ETH-USD') + .01
    account = client[mode].get_account(account_ids['ETH'])
    size = account['balance']
    print(client[mode].sell(price=price, size=size, product_id='ETH-USD', post_only=True))


def place_ETH_fees_sell(event=None):
    client[mode].cancel_all(product='ETH-USD')
    account = client[mode].get_account(account_ids['ETH'])
    size = account['balance']
    print(client[mode].sell(type='market', size=size, product_id='ETH-USD', post_only=False))


def place_LTC_sell(event=None):
    client[mode].cancel_all(product='LTC-USD')
    if len(str(LTC_limit_entry_box.get())) > 1:
        price = float(LTC_limit_entry_box.get())
    else:
        price = get_bid('LTC-USD') + .01
    account = client[mode].get_account(account_ids['LTC'])
    size = account['balance']
    print(client[mode].sell(price=price, size=size, product_id='LTC-USD', post_only=True))


def place_LTC_fees_sell(event=None):
    client[mode].cancel_all(product='LTC-USD')
    account = client[mode].get_account(account_ids['LTC'])
    size = account['balance']
    print(client[mode].sell(type='market', size=size, product_id='LTC-USD', post_only=False))


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


def extract_account_id(accounts, product):
    for account in accounts:
        print("account : " + account)
        if account.get('currency') == product:
            return account.get('id')


if __name__ == "__main__":
    main()
