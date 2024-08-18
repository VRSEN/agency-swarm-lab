import React from 'react';
import PropTypes from 'prop-types';

const app = () => {
const handleClick = () => console.log('App clicked');

    return (
        <div className="App">
          <button onClick="handleClick">
            <span  />
            <button >
              <span >
                Hello, world!
              </span>
            </button>
          </button>
        </div>
    );
};

export default app;
