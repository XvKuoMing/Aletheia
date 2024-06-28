import React from "react";

import "./SearchResults.css"
import {ProductCard} from "./ProductCard";


function asChunk(array, chunkSize) {
    const chunks = [];
    for (let i = 0; i < array.length; i += chunkSize) {
        chunks.push(array.slice(i, i + chunkSize));
    }
    return chunks;
}

export function SearchResults(props) {
    if (props.results && props.results.length > 0) {
        return (
            <div className="card-container">
                {props.results.map(element => 
                            <ProductCard 
                            title={element.name}
                            img={element.img}
                            desc={element.desc}
                            max_price={element.max_price}
                            max_price_shop={element.max_price_shop}
                            min_price={element.min_price}
                            min_price_shop={element.min_price_shop}
                            />
                )}
            </div>
        )
    } else {
        return <p>No products</p>
    }
};