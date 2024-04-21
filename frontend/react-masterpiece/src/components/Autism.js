import React from 'react';
import axios from 'axios';
import '../../src/css/autism.css';

class Autism extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: null
        };
    }

    componentDidMount() {
        // Call the endpoint when the component mounts
        this.fetchHighlights();
    }

    fetchHighlights = () => {
        // Make a GET request to fetch highlights
        axios.get('http://localhost:5000/get_highlights')
            .then(response => {
                // Update state with the received data
                this.setState({ data: response.data });
            })
            .catch(error => {
                console.error('Error fetching highlights:', error);
            });
    };

    render() {
        const { data } = this.state;
        const title = 'In Retrospect.....';
        const buttons = data ? Object.keys(data) : []; // Use data keys as buttons

        return (
            <div>
                {/* Render header with title */}
                <span className="post"><Header title={title} /></span>
                {/* Render accordion with fetched data */}
                {data && <Accordion data={data} buttons={buttons} />}
                {/* Render button to fetch highlights */}
                {!data && <button onClick={this.fetchHighlights}>Fetch Highlights</button>}
            </div>
        );
    }
}

class Header extends React.Component {
    render() {
        return (
            <h1>{this.props.title}</h1>
        );
    }
}

class Accordion extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activeButton: null
        };
    }

    handleButtonClick = (button) => {
        this.setState({ activeButton: button });
    };

    render() {
        const { data, buttons } = this.props;
        const { activeButton } = this.state;

        return (
            <div className="accordion">
                {buttons.map((button, index) => (
                    <AccordionItem
                        key={index}
                        button={button}
                        isActive={button === activeButton}
                        items={formatData(data)[button]}
                        onClick={this.handleButtonClick}
                    />
                ))}
            </div>
        );
    }
}

class AccordionItem extends React.Component {
    render() {
        const { button, isActive, items, onClick } = this.props;

        return (
            <div>
                <button
                    className={`accordion__button ${isActive ? 'active' : ''}`}
                    onClick={() => onClick(button)}
                >
                    {button}<span className="fas fa-plus"></span>
                </button>
                <p className={`accordion__content ${isActive ? 'active' : ''}`}>
                    {items.split(',\n').map((tuple, index) => (
                        <span key={index}>
                            <span className="person1">{tuple.split(':')[0]}</span><span className="Colon">:</span> <span className="person2">{tuple.split(':')[1]}</span>
                            <br />
                        </span>
                    ))}
                </p>
            </div>
        );
    }
}

function formatData(data) {
    const formattedData = {};
    for (const button in data) {
        if (Array.isArray(data[button])) {
            formattedData[button] = data[button].map(tuple => tuple.join(':')).join(',\n');
        } else {
            formattedData[button] = data[button];
        }
    }
    return formattedData;
}

export default Autism;
