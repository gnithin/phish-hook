console.log("From the background page!");

const displayUrl = (url) => {
  if (!url) {
    return;
  }

  let domain = (new URL(url));
  let hostname = domain.hostname;

  console.log("Domain - ", domain.hostname);

  // TODO: Find malicious content
  if (hostname === "stackoverflow.com") {
    chrome.notifications.create('', {
      title: 'Phishing Alert!',
      message: 'This site may be malicious, click here to know more!',
      iconUrl: '/icons/icon19.png',
      type: 'basic',
    });
  }
}

chrome.notifications.onClicked.addListener((id) => {
  chrome.notifications.clear(id);
  chrome.tabs.create({ url: "src/browser_action/browser_action.html" });
});

// When the url in the tab changes
chrome.tabs.onUpdated.addListener(
  (_, info, __) => {
    if (info && info.url) {
      displayUrl(info.url);
    }
  }
);

// When tabs are switched
chrome.tabs.onActivated.addListener((activeInfo) => {
  chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
    displayUrl(tabs[0].url);
  });
});