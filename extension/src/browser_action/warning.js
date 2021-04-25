window.onload = () => {
    console.log("Page loaded!")

    ReactDOM.render(
        React.createElement(Warning, {}),
        document.getElementById('root')
    );
};

class Warning extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            data: null,
        };
    }

    componentDidMount() {
        // get id from url 
        const urlParams = new URLSearchParams(window.location.search);
        const id = urlParams.get('id');
        if (id !== null || typeof (id) !== undefined) {
            this.loadData(id)
        }
    }

    loadData(id) {
        console.log("Loading data for id - ", id);
        chrome.storage.local.get([id], (result) => {
            console.log('Value currently is ', result);
            // Change the state
            this.setState({ data: result[id] });
        });
    }

    render() {
        let url = ""
        if (this.state.data) {
            url = this.state.data.url;
        }

        /*
        <div>
            <h1>Warning!</h1>
            <div>Exercise caution if this site asks for personal information! One of our models flagged this site as potential phishing site. Just letting you know to be cautious!</div>
        </div>
        */
        return React.createElement(
            'div', null, [
            React.createElement('h1', { key: '1' }, "Warning!"),
            React.createElement('div', { key: '2' }, "Exercise caution if this site asks for personal information! One of our models flagged this site as potential phishing site. Just letting you know to be cautious!")
        ]
        );
    }
}
