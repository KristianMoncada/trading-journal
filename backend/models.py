class Trade:
    def __init__(self, id, ticker, side, entry_price, exit_price, contracts, notes):
        self.id = id
        self.ticker = ticker
        self.side = side
        self.entry_price = entry_price
        self.exit_price = exit_price
        self.contracts = contracts
        self.notes = notes

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
    

    
        