import { useState, useEffect } from 'react'
// Connects to flask api call for retrieving list of trades
function TradeList({ trades }) {
    return (
        <div>
            <ul>
                {trades.map((trade) => (                // loop over every trade and make one list item per trade
                    <li key={trade.id}>                 {/* key = unique id so React can track each row */}
                        #{trade.id} {trade.ticker} {trade.side} {trade.entry_price} to {trade.exit_price} x{trade.contracts} {trade.notes}
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default TradeList