import React, {useState, useEffect} from 'react'
import '../App.css';
import Blockchain from "./Blockchain";
function App() {

    const [walletInfo, setWalletInfo] = useState({})

    const getWalletInfo = async ()=>{
        try{
            let res = await fetch('http://127.0.0.1:5000/wallet/info')
            let json = await res.json()
            setWalletInfo(json)
        }catch (e){
            console.log(`Error fetching from getWalletInfo. MSG: ${e.message}`)
        }
    }

    useEffect(()=>{
        getWalletInfo()

    },[])

    const {address, balance} = walletInfo

    return (
        <div className="App">
            <h3>Welcome to pychain</h3>
            <hr/>
            <div>Address: {address}</div>
            <div>Balance: {balance}</div>

            <Blockchain/>
        </div>
    );
}

export default App;
