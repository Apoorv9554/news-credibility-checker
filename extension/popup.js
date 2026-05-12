const backendEndpoint = 'http://127.0.0.1:8001/api/check';
const urlInput = document.getElementById('url');
const titleInput = document.getElementById('title');
const contentInput = document.getElementById('content');
const analyzeBtn = document.getElementById('analyzeBtn');
const copyUrlBtn = document.getElementById('copyUrl');
const statusEl = document.getElementById('status');
const resultEl = document.getElementById('result');
const summaryEl = document.getElementById('summary');
const backendSourceEl = document.getElementById('backend_source');
const rawResponseEl = document.getElementById('rawResponse');

const fields = {
  credibility: document.getElementById('credibility'),
  fake_probability: document.getElementById('fake_probability'),
  clickbait_score: document.getElementById('clickbait_score'),
  news_verification_score: document.getElementById('news_verification_score'),
  stance_score: document.getElementById('stance_score'),
  source_reputation: document.getElementById('source_reputation'),
};

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.style.color = isError ? '#fb7185' : '#a5b4fc';
}

function setLoading(isLoading) {
  analyzeBtn.disabled = isLoading;
  analyzeBtn.textContent = isLoading ? 'Analyzing...' : 'Analyze Page';
}

function getSummary(credibility) {
  if (credibility >= 75) {
    return { text: 'Likely credible — the news appears trustworthy.', className: 'safe' };
  }
  if (credibility >= 50) {
    return { text: 'Partially credible — review carefully.', className: 'moderate' };
  }
  return { text: 'Potential risk — the article may be unreliable.', className: 'risky' };
}

function clearResult() {
  resultEl.classList.add('hidden');
  summaryEl.textContent = '';
  summaryEl.className = 'summary';
  backendSourceEl.textContent = '-';
  rawResponseEl.value = '';
}

function normalizeScore(value) {
  if (typeof value === 'number') return value;
  if (typeof value === 'string' && value.trim() !== '') {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : NaN;
  }
  return NaN;
}

function computeFallbackCredibility(data) {
  const fake = normalizeScore(data.fake_probability);
  const verification = normalizeScore(data.news_verification_score);
  const stance = normalizeScore(data.stance_score);
  const clickbait = normalizeScore(data.clickbait_score);

  if ([fake, verification, stance, clickbait].some(Number.isNaN)) {
    return NaN;
  }

  const fakeComponent = Math.max(0.5, 1 - fake);
  let credibility = (
    0.25 * fakeComponent +
    0.40 * verification +
    0.30 * stance +
    0.05 * clickbait
  ) * 100;

  if (verification >= 0.8 && stance >= 0.7) {
    credibility += 5;
  }

  return Math.min(100, Math.round(credibility * 100) / 100);
}

function formatModelScore(value) {
  if (!Number.isFinite(value)) {
    return '-';
  }

  return `${value.toFixed(4)} (${(value * 100).toFixed(2)}%)`;
}

function showResult(response) {
  const { endpoint, data } = response;
  const credibilityValue = normalizeScore(data.credibility_score ?? data.credibility);
  const finalCredibility = Number.isNaN(credibilityValue)
    ? computeFallbackCredibility(data)
    : credibilityValue;

  const responseMap = {
    credibility: finalCredibility,
    fake_probability: normalizeScore(data.fake_probability),
    clickbait_score: normalizeScore(data.clickbait_score),
    news_verification_score: normalizeScore(data.news_verification_score),
    stance_score: normalizeScore(data.stance_score),
    source_reputation: normalizeScore(data.source_reputation),
  };

  Object.entries(fields).forEach(([key, el]) => {
    const value = responseMap[key];
    if (key === 'credibility') {
      el.textContent = Number.isFinite(value) ? `${value.toFixed(2)}%` : '-';
      return;
    }

    el.textContent = formatModelScore(value);
  });

  const summary = getSummary(Number.isFinite(finalCredibility) ? finalCredibility : 0);
  summaryEl.textContent = summary.text;
  summaryEl.classList.add(summary.className);
  backendSourceEl.textContent = endpoint;
  rawResponseEl.value = JSON.stringify(data, null, 2);
  resultEl.classList.remove('hidden');
}

async function getPageDataFromScripting(tabId) {
  return new Promise((resolve, reject) => {
    chrome.scripting.executeScript(
      {
        target: { tabId },
        func: () => {
          const getMetaContent = (selectors) => {
            for (const selector of selectors) {
              const el = document.querySelector(selector);
              if (el?.content?.trim()) {
                return el.content.trim();
              }
            }
            return '';
          };

          const getElementText = (root) => {
            return Array.from(root.querySelectorAll('h1, h2, h3, p, li'))
              .map((node) => node.textContent?.trim() || '')
              .filter(Boolean)
              .join('\n\n');
          };

          const selection = window.getSelection()?.toString().trim();
          if (selection) {
            return { url: window.location.href, title: document.title || '', content: selection };
          }

          const metaDescription = getMetaContent([
            'meta[name="description"]',
            'meta[property="og:description"]',
            'meta[name="twitter:description"]',
          ]);

          const article = document.querySelector('article');
          if (article) {
            const text = getElementText(article);
            if (text.length > 100) {
              return {
                url: window.location.href,
                title: document.title || '',
                content: `${metaDescription ? metaDescription + '\n\n' : ''}${text}`.slice(0, 20000),
              };
            }
          }

          const main = document.querySelector('main') || document.querySelector('[role="main"]');
          if (main) {
            const text = getElementText(main);
            if (text.length > 100) {
              return {
                url: window.location.href,
                title: document.title || '',
                content: `${metaDescription ? metaDescription + '\n\n' : ''}${text}`.slice(0, 20000),
              };
            }
          }

          const paragraphs = Array.from(document.querySelectorAll('p'))
            .map((p) => p.textContent?.trim() || '')
            .filter(Boolean);

          if (paragraphs.length >= 3) {
            return {
              url: window.location.href,
              title: document.title || '',
              content: `${metaDescription ? metaDescription + '\n\n' : ''}${paragraphs.join('\n\n')}`.slice(0, 20000),
            };
          }

          return {
            url: window.location.href,
            title: document.title || '',
            content: `${metaDescription ? metaDescription + '\n\n' : ''}${document.body.innerText || ''}`.slice(0, 20000),
          };
        },
      },
      (results) => {
        if (chrome.runtime.lastError) {
          return reject(chrome.runtime.lastError.message);
        }
        resolve(results?.[0]?.result || null);
      }
    );
  });
}

async function loadPageData() {
  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    if (!tabs[0]?.id) {
      setStatus('Unable to access active tab.', true);
      return;
    }

    const tabId = tabs[0].id;

    chrome.tabs.sendMessage(tabId, { type: 'getPageData' }, async (response) => {
      if (chrome.runtime.lastError || !response) {
        try {
          const pageData = await getPageDataFromScripting(tabId);
          if (!pageData) {
            throw new Error('No page data returned');
          }
          urlInput.value = pageData.url || '';
          titleInput.value = pageData.title || '';
          contentInput.value = pageData.content || '';
          return;
        } catch (error) {
          setStatus('Unable to read page content. Refresh the page and try again.', true);
          return;
        }
      }

      urlInput.value = response.url || '';
      titleInput.value = response.title || '';
      contentInput.value = response.content || '';
    });
  });
}

async function fetchBackend(payload) {
  const response = await fetch(backendEndpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    const detail = errorBody ? `: ${errorBody.slice(0, 180)}` : '';
    throw new Error(`Backend error ${response.status} at ${backendEndpoint}${detail}`);
  }

  return {
    endpoint: backendEndpoint,
    data: await response.json(),
  };
}

async function analyzePage() {
  clearResult();

  const title = titleInput.value.trim();
  const content = contentInput.value.trim();
  const payload = {
    title,
    content,
  };

  if (!payload.title || !payload.content) {
    setStatus('Title and content are required.', true);
    return;
  }

  setLoading(true);
  setStatus('Sending extracted article to backend...');

  try {
    const data = await fetchBackend(payload);
    showResult(data);
    setStatus('Analysis complete.');
  } catch (error) {
    const message = error?.message || 'Unknown backend error';
    setStatus(`Error: ${message}. Make sure the same backend used by the web page is running on 127.0.0.1:8001.`, true);
  } finally {
    setLoading(false);
  }
}

function copyUrl() {
  if (!urlInput.value) {
    setStatus('Nothing to copy.', true);
    return;
  }

  navigator.clipboard.writeText(urlInput.value)
    .then(() => setStatus('Page URL copied to clipboard.'))
    .catch(() => setStatus('Unable to copy URL.', true));
}

analyzeBtn.addEventListener('click', analyzePage);
copyUrlBtn.addEventListener('click', copyUrl);
window.addEventListener('DOMContentLoaded', loadPageData);
