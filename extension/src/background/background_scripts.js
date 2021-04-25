console.log("From the background page!");

const BASE_URL = "http://localhost:9999";
const DETECT_ENDPOINT = `${BASE_URL}/detect`;

const detectUrlPhishing = async (url) => {
  const defaultResp = {
    isPhishing: false,
    consensusReached: true,
  };

  // Make the api call 
  console.log("URL - ", url);

  try {
    const response = await fetch(DETECT_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        'url': url
      }),
    });

    const respJson = await response.json();
    console.log("RESPONSE - ", respJson)

    if (respJson.success) {
      defaultResp.consensusReached = respJson["consensus_reached"]
      defaultResp.isPhishing = respJson["is_phishing"]
    }

  } catch (e) {
    console.log("Error in fetch - ", e)
  }

  return defaultResp
}

const processUrl = async (url) => {
  if (!url || typeof (url) === "undefined" || url === null) {
    return;
  }

  const { isPhishing, consensusReached } = await detectUrlPhishing(url);
  console.log("RESPONSE - isPhishing - ", isPhishing);
  console.log("RESPONSE - consensusReached - ", consensusReached);

  if (!consensusReached) {
    // TODO: Think about consensus not reached
    console.log("Consensus has not been reached!")
    chrome.notifications.create('', {
      title: 'Caution!',
      message: 'Exercise caution when submitting personal data to this site. Click here to know more!',
      iconUrl: '/icons/icon19.png',
      type: 'basic',
    });
    return;
  }

  if (isPhishing) {
    chrome.notifications.create('', {
      title: 'Phishing Alert!',
      message: 'This site may be malicious, Click here to know more!',
      iconUrl: '/icons/icon19.png',
      type: 'basic',
    });
  }
}

chrome.notifications.onClicked.addListener((id) => {
  chrome.notifications.clear(id);
  chrome.tabs.create({ url: "src/browser_action/warning.html" });
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