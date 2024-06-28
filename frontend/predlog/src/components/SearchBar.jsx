import React, { useState } from 'react';
import {FaSearch} from "react-icons/fa";

import "./SearchBar.css";

export function SearchBar(props) {
    const [input, setInput] = useState("")

    const fetchData = (value) => {
        fetch("http://localhost:8080/"+value,
          {
            method: 'GET',
            mode: 'cors', // cross origin
            headers: {
              'Content-Type': 'application/json'
            },
            cache: 'force-cache',
            next: {revalidate: 3600}
          }
        )
        .then((response) => response.json())
        .then((json) => {
          props.setResults(json.results)
          //console.log(json);
        })
    };
    // https://stackoverflow.com/questions/69246976/how-to-cache-react-component-fetches
    const handleChange = (value) => {
        setInput(value);
        fetchData(value);
    };

    return (
        <div className='input-wrapper'>
          <FaSearch id="search-icon"/>
          <input 
          placeholder='Что вы хотите купить?'
          value={input}
          onChange={
            (e) => handleChange(e.target.value)
          }
          />
        </div>
    )
};