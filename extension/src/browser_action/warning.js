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
            loading: true,
            data: null,
            error: false,
        };
    }

    componentDidMount() {
        // get id from url 
        const urlParams = new URLSearchParams(window.location.search);
        const id = urlParams.get('id');
        if (id !== null || typeof (id) !== "undefined") {
            this.loadData(id)
        }
    }

    loadData(id) {
        this.setState({ loading: true });
        console.log("Loading data for id - ", id);

        chrome.storage.local.get([id], (result) => {
            console.log('Data from store is - ', result);
            if (result === null || typeof (result) === "undefined") {
                this.setState({ error: true });
                return;
            }

            // Add the data to the state
            this.setState({
                loading: false,
                data: result[id],
            });
        });
    }

    render() {
        if (this.state.loading) {
            /*
            <div className="loading">
                Loading...
            <div>
            */
            return React.createElement(
                'div', { className: "loading" }, "Loading..."
            );
        }

        if (
            this.state.error ||
            this.state.data === null ||
            typeof (this.state.data) === "undefined"
        ) {
            /*
            <div className="error">
                Oops, we messed up! This was not supposed to happen. Please close this page :)
            <div>
            */
            return React.createElement(
                'div', { className: "error" },
                "Oops, we messed up! This was not supposed to happen. Please close this page :)"
            );
        }

        let url = this.state.data.url;

        if (!this.state.data.consensusReached) {
            /*
            <div>
                <h1>Warning!</h1>
                <div>Exercise caution if this site asks for personal information! One of our models flagged this site as potential phishing site. Just letting you know to be cautious!</div>
            </div>
            */
            return React.createElement(
                'div', { className: "warning" }, [
                React.createElement('h1', { key: '1' }, "Warning!"),
                React.createElement('div', { key: '2' }, "Exercise caution if this site asks for personal information! One of our models flagged this site as potential phishing site. Just letting you know to be cautious!")
            ]);
        }

        // It's a phishing site!
        /*
        <div>
            <h1>Alert!</h1>
            <div>Our models flagged this site as a potential Phishing site. Tread lightly, or better yet, close this page!</div>
        </div>
        */
        return React.createElement(
            'div', { className: "alert" }, [
            React.createElement('h1', { key: '1' }, "Alert!"),
            React.createElement('div', { key: '2' }, "Our models flagged this site as a potential Phishing site. Tread lightly, or better yet, close this page!"),
        ]);
    }
}
