const MAX_TEXT_LENGTH = 20000;

function getElementText(root) {
  const nodes = Array.from(root.querySelectorAll('h1, h2, h3, p, li'));
  return nodes
    .map((node) => node.textContent?.trim() || '')
    .filter(Boolean)
    .join('\n\n');
}

function getPageText() {
  const selection = window.getSelection()?.toString().trim();
  if (selection) {
    return selection;
  }

  const article = document.querySelector('article');
  if (article) {
    const text = getElementText(article);
    if (text.length > 100) {
      return text.slice(0, MAX_TEXT_LENGTH);
    }
  }

  const roleArticle = document.querySelector('[role="article"]');
  if (roleArticle) {
    const text = getElementText(roleArticle);
    if (text.length > 100) {
      return text.slice(0, MAX_TEXT_LENGTH);
    }
  }

  const paragraphs = Array.from(document.querySelectorAll('p'))
    .map((p) => p.textContent?.trim() || '')
    .filter(Boolean);

  if (paragraphs.length >= 3) {
    return paragraphs.join('\n\n').slice(0, MAX_TEXT_LENGTH);
  }

  const bodyText = document.body.innerText?.trim() || '';
  return bodyText.slice(0, MAX_TEXT_LENGTH);
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message?.type === 'getPageData') {
    const pageData = {
      url: window.location.href,
      title: document.title || '',
      content: getPageText(),
    };
    sendResponse(pageData);
  }
});
