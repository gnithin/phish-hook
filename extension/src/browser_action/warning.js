window.onload = () => {
    console.log("Page loaded!")

    // get id from url 
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    if (id !== null || typeof (id) !== undefined) {
        loadData(id)
    }
}

const loadData = (id) => {
    console.log("Loading data for id - ", id);

    chrome.storage.local.get([id], function (result) {
        console.log('Value currently is ', result);
    });
}