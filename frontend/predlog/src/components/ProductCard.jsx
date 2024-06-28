import React from "react";

import "./ProductCard.css";


export function ProductCard(props) {
    return (
        <div className="card">
            <img src={props.img} alt={props.title} />
            <h2 className="card-title">{props.title}</h2>
            <div className="card-desc">
                <p className="price_shop">Минимальная цена: {props.min_price} руб. <span>{props.min_price_shop}</span></p>
                <p className="price_shop">Максимальная цена: {props.max_price} руб. <span>{props.max_price_shop}</span></p>
            </div>
        </div>
    )
};