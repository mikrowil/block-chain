import React, {useState} from "react";
import {Button} from 'react-bootstrap'
import {MILLI_PY} from "../config";
import Transaction from "./Transaction";

const ToggleTransactionDisplay = ({block}) => {
    const [displayTransaction, setDisplayTransaction] = useState(false)
    const {data} = block

    const toggleDisplay = () => {
        setDisplayTransaction(!displayTransaction)
    }

    if (displayTransaction) {
        return (
            <div>
                {
                    data.map((transaction) => (
                        <div key={transaction.id}>
                            <hr/>
                            <Transaction transaction={transaction}/>
                        </div>
                    ))
                }
                <br/>
                <Button
                    variant={"danger"}
                    size={"sm"}
                    onClick={toggleDisplay}
                >
                    Show Less
                </Button>
            </div>
        )
    }

    return <div>
        <br/>
        <Button
            variant={"danger"}
            size={"sm"}
            onClick={toggleDisplay}
        >
            Show More
        </Button>
    </div>
}

const Block = ({block}) => {
    const {timestamp, hash} = block
    const hashDisplay = `${hash.substring(0, 15)}...`
    const timestampDisplay = new Date(timestamp / MILLI_PY).toLocaleString();

    return <div className={"Block"}>
        <div>
            Hash: {hashDisplay}
        </div>
        <div>Timestamp: {timestampDisplay}</div>
        <ToggleTransactionDisplay block={block}/>
    </div>
}

export default Block
