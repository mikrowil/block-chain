import React,{useState, useEffect} from "react";
import blockpi from "../apis/blockpi";
import Block from "./Block";

const Blockchain = () => {
    const [blockchain, setBlockchain] = useState([])

    const getBlockchain = async () =>{
        let res = await blockpi.get('/blockchain')
        let json = await res.data
        setBlockchain(json)
    }

    useEffect((()=>{
        getBlockchain()
    }),[])

    return(
        <div className={"Blockchain"}>
            <h3>Blockchain</h3>
            <div>{blockchain.map((value)=>(
                <Block key={value.hash} block={value}/>
            ))}</div>
        </div>
    )
}


export default Blockchain
