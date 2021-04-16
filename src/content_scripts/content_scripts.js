chrome.extension.onMessage.addListener(
  function (request, sender, sendResponse) {
    chrome.pageAction.show(sender.tab.id);
    sendResponse();
  }
);

console.log("From the background page!");

chrome.tabs.onUpdated.addListener(
  (_, info, __) => {
    if (info && info.url) {
      console.log("Change url - ", info.url);
    }
  }
);

chrome.tabs.onActivated.addListener((activeInfo) => {
  console.log("On Activated called!");
  chrome.tabs.query({ active: true, lastFocusedWindow: true }, tabs => {
    let url = tabs[0].url;
    console.log("Current url - ", url);
  });
});