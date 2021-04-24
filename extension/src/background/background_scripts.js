console.log("From the background page!");

const BASE_URL = "http://localhost:9999";
const DETECT_ENDPOINT = `${BASE_URL}/detect`;

const detectMalicious = async (url) => {
  // Make the api call 

  const response = await fetch(DETECT_ENDPOINT, {
    method: 'POST',
    // mode: 'cors', // no-cors, *cors, same-origin
    // credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    // redirect: 'follow', // manual, *follow, error
    // referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: new URLSearchParams({
      'url': url
    }),
  });
  return response.json();
}

const processUrl = async (url) => {
  if (!url || typeof (url) === "undefined" || url === null) {
    return;
  }

  const resp = await detectMalicious(url);
  console.log("RESPONSE - ", resp);

  if (!resp.is_phishing) {
    return;
  }

  chrome.notifications.create('', {
    title: 'Phishing Alert!',
    message: 'This site may be malicious, click here to know more!',
    iconUrl: '/icons/icon19.png',
    type: 'basic',
  });
}

chrome.notifications.onClicked.addListener((id) => {
  chrome.notifications.clear(id);
  chrome.tabs.create({ url: "src/browser_action/browser_action.html" });
});

// When the url in the tab changes
chrome.tabs.onUpdated.addListener(
  async (_, info, __) => {
    if (info && info.url) {
      await processUrl(info.url);
    }
  }
);

// When tabs are switched
chrome.tabs.onActivated.addListener((activeInfo) => {
  chrome.tabs.query({ active: true, lastFocusedWindow: true }, async tabs => {
    await processUrl(tabs[0].url);
  });
});