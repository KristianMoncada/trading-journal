trades = []
counter = 1

class Trade:
    # Trade constructor
    def __init__(self, id, ticker, side, entry_price, exit_price, contracts, notes):
        self.id = id
        self.ticker = ticker
        self.side = side
        self.entry_price = entry_price
        self.exit_price = exit_price
        self.contracts = contracts
        self.notes = notes

    # Return object as dictionary so that Flask can JSONify the object since anything sent over HTTP has to be text
    def to_dict(self):
        return {
            'id': self.id,
            'ticker': self.ticker,
            'side': self.side,
            'entry_price': self.entry_price,
            'exit_price': self.exit_price,
            'contracts': self.contracts,
            'notes': self.notes
        }
# Created a trade by passing it the trade details and auto assigning an id to that trade using the counter
def add_trade(ticker, side, entry_price, exit_price, contracts, notes):
    global counter
    trade = Trade(counter, ticker, side, entry_price, exit_price, contracts, notes)
    trades.append(trade)
    counter += 1
    return trade
# The user will give us an id to identify the trade we want to delete and with that we search through our list to remove the trade with the matching id
def remove_trade(id):
    for trade in trades:
        if trade.id == id:
            trades.remove(trade)
            return "Trade removed successfully"
    return 'Trade could not be found'

def all_trades(): 
    for trade in trades:
        print(trade.to_dict())


        