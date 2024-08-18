
                const React = require('react');
const PropTypes = require('prop-types');
const {serialize} = require('react-serialize');
                const handleClick = null;
                const jsx = <div className="App">
      <button onClick="handleClick">
        <span  />
      </button>
    </div>;
                const json = serialize(jsx);
                console.log(json);
            