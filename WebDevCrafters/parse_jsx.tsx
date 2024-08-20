
                import React from 'react';
                import { serialize } from 'react-serialize';
                import React, { useState } from 'react';
import PropTypes from 'prop-types';

                const TempComponent: React.FC = () => {
                    const [count, setCount] = useState(0);

  const handleIncrement = () => {
    setCount(prevCount => prevCount + 1);
  };

  const handleDecrement = () => {
    setCount(prevCount => prevCount - 1);
  };
                    return (
                        <div>
        Hello World!
      <h2>Simple Counter</h2>
      <p>Count: {count}</p>
      <button onClick={handleIncrement}>Increment</button>
      <button onClick={handleDecrement}>Decrement</button>
    </div>
                    );
                };

                const jsx = <TempComponent />;
                const json = serialize(jsx);
                console.log(JSON.stringify(json));
            