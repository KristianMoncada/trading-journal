import './App.css'
import TradeForm from './components/TradeForm'
import TradeList from './components/TradeList'
import { useState, useEffect } from 'react'

function App() {
    const [trades, setTrades] = useState([])           // trades = the list (starts empty); setTrades = how we change it and trigger a redraw
 
    const loadTrades = () => {                          // a reusable function that gets the latest trades from Flask
        fetch('http://127.0.0.1:5000/trades')           // send a GET request to your list_trades route
            .then((response) => response.json())        // when Flask answers, turn the response body into JS data
            .then((data) => setTrades(data))            // save that data into state -> React redraws with the new list
    }
 
    useEffect(() => {                                   // run this once, when App first appears on the page
        loadTrades()                                    // load the trades the first time
    }, [])                                              // [] = only once (no infinite loop)
 
    return (
        <>                                              {/* fragment: invisible wrapper */}
            <h1>Trading Journal</h1>                    {/* page title */}
            <TradeForm onTradeAdded={loadTrades} />     {/* pass the loadTrades FUNCTION down so the form can ask for a reload */}
            <TradeList trades={trades} />               {/* pass the trades DATA down so the list can display it */}
        </>
    )
}
 
export default App                                      // let main.jsx import App