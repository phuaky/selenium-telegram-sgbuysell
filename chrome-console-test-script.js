function log(message) {
  console.log(`[${new Date().toISOString()}] ${message}`);
}

function findElementWithFallback(parent, selectors) {
  for (let selector of selectors) {
    try {
      const element = parent.querySelector(selector);
      if (element) return element;
    } catch (error) {
      console.warn(`Invalid selector: ${selector}`);
    }
  }
  return null;
}

function extractTextContent(element) {
  return element ? element.textContent.trim() : 'Not found';
}

function findElementByText(parent, text) {
  return Array.from(parent.querySelectorAll('p')).find((el) =>
    el.textContent.trim().includes(text)
  );
}

function analyzeListingCard(card) {
  const titleSelectors = [
    'p[data-testid="listing-card-text-title"]',
    'p[class*="D_lQ"]',
    'p:not([data-testid]):not([class*="D_mc"]):not([class*="D_pc"])',
  ];
  const priceSelectors = [
    'p[data-testid="listing-card-text-price"]',
    'p[class*="D_mc"]',
  ];
  const timeSelectors = ['p[class*="time"]', 'p[class*="D_pc"]'];

  const title = findElementWithFallback(card, titleSelectors);
  const price = findElementWithFallback(card, priceSelectors);
  const sellerName = card.querySelector(
    'p[data-testid="listing-card-text-seller-name"]'
  );
  const time = findElementWithFallback(card, timeSelectors);

  const conditionTypes = [
    'Brand new',
    'Like new',
    'Lightly used',
    'Well used',
    'Heavily used',
  ];
  const condition = conditionTypes
    .map((type) => findElementByText(card, type))
    .find((el) => el);

  const listingId =
    card.getAttribute('data-testid')?.replace('listing-card-', '') ||
    'Not found';

  return {
    id: listingId,
    title: extractTextContent(title),
    price: extractTextContent(price),
    sellerName: extractTextContent(sellerName),
    time: extractTextContent(time),
    condition: extractTextContent(condition),
  };
}

function runTest() {
  log('Starting test...');

  const listingContainer = document.querySelector(
    'div[class*="browse-listings"]'
  );
  if (!listingContainer) {
    log('❌ Listing container not found');
    return;
  }
  log('✅ Listing container found');

  const listingCards = listingContainer.querySelectorAll(
    'div[data-testid^="listing-card-"]'
  );
  log(`Found ${listingCards.length} listing cards`);

  if (listingCards.length === 0) {
    log('❌ No listing cards found');
    return;
  }

  const sampleSize = Math.min(5, listingCards.length);
  for (let i = 0; i < sampleSize; i++) {
    log(`Analyzing listing card ${i + 1}:`);
    const cardData = analyzeListingCard(listingCards[i]);
    console.log(cardData);
  }

  log('Test completed.');
}

runTest();
