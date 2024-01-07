
document.addEventListener('DOMContentLoaded', function() {
    setupNavigation();
    initializeContentSections();
    setupCryptoWidgets();
    startWidgetUpdateInterval();
    continuouslyUpdateNews(300000);
});


function setupNavigation() {
    
    console.log("test setup navigation")

    const navItems = document.querySelectorAll('.nav-item');
    const contentSections = document.querySelectorAll('.content-section');

    navItems.forEach(item => {
        item.addEventListener('click', function() {
            toggleContentSections(contentSections, this);
            toggleActiveNavItem(navItems, this);
        });
    });

    setActiveContentAndNavItem('home');

}

function initializeContentSections() {
    
    console.log("test initialize content sections")

    const contentSections = document.querySelectorAll('.content-section');
    contentSections.forEach(section => section.style.display = 'none');

    const homeContent = document.getElementById('content-home');
    if (homeContent) {
        homeContent.classList.add('visible');
        homeContent.style.display = 'block';
    }

}

function toggleContentSections(contentSections, clickedItem) {
    contentSections.forEach(section => {
        section.style.display = 'none';
    })

    const activeSection = document.getElementById('content-' + clickedItem.id);
    if(activeSection) {
        activeSection.style.display = 'block';
    }
}

function toggleActiveNavItem(navItems, activeItem) {
    navItems.forEach(nav => nav.classList.remove('active-nav-item'));
    activeItem.classList.add('active-nav-item');
}

function setActiveContentAndNavItem(itemId) {
    const content = document.getElementById('content-' + itemId);
    const item = document.getElementById(itemId);

    if (content) {
        content.style.display = 'block';
    }
    if (item) {
        item.classList.add('active-nav-item');
    }
}

function setupCryptoWidgets() {

    console.log("test setup crypto widgets")
    
    const cryptoData = [
        { symbol: 'BTC', widgetPrice: 'BTCPrice', widgetChange: 'BTCRaito' },
        { symbol: 'ETH', widgetPrice: 'ETHPrice', widgetChange: 'ETHRaito' },
        { symbol: 'XRP', widgetPrice: 'XRPPrice', widgetChange: 'XRPRaito' },
        { symbol: 'SOL', widgetPrice: 'SOLPrice', widgetChange: 'SOLRaito' },
        { symbol: 'AVAX', widgetPrice: 'AVAXPrice', widgetChange: 'AVAXRaito'},
        { symbol: 'JPY', widgetPrice: 'JPYPrice', widgetChange: 'JPYRaito'}
    ];

    cryptoData.forEach(({ symbol, widgetPrice, widgetChange }) => {
        const priceElement= document = document.getElementById(widgetPrice);
        const changeElement = document.getElementById(widgetChange);
        

        window.electronAPI.sendData('s' + symbol + 'USDT-current-price');
        window.electronAPI.receiveData('r' + symbol + 'USDT-current-price', (data) => {
            updateWidget(data.currentPrice, data.previousPrice, priceElement, changeElement);
        });
    });
}

function startWidgetUpdateInterval(){

    console.log("test start widget update interval")

    const updateInterval = 60000;

    setInterval(() => {
        setupCryptoWidgets();
    }, updateInterval);
}

function updateWidget(currentPrice, previousPrice, widgetPrice, widgetChange) {

    currentPrice = parseFloat(currentPrice);
    previousPrice = parseFloat(previousPrice);
    const beforeRaito = ((currentPrice - previousPrice) / previousPrice) * 100;

    if (widgetPrice && widgetChange){
        widgetPrice.textContent = currentPrice.toFixed(2);
        widgetChange.textContent = beforeRaito.toFixed(2) + '%';

        if (currentPrice !== null){
            if (currentPrice > previousPrice) {

                widgetChange.classList.remove('negative');
                widgetPrice.classList.remove('negative');

                widgetChange.classList.add('positive');
                widgetPrice.classList.add('positive');
            
            } else if (currentPrice < previousPrice) {
            
                widgetChange.classList.remove('positive');
                widgetPrice.classList.remove('positive');

                widgetChange.classList.add('negative');
                widgetPrice.classList.add('negative');
            
            }
        }
    }    
}

function updateNewsData (newsData) {

    const newsList = document.getElementById('news-list');
    console.log("ここまできてる");
    newsList.innerHTML = '';

    newsData.forEach((newsItem, index) => {
        const listItem = document.createElement('li');
        listItem.classList.add('news-item');

        listItem.innerHTML = `
            <span class="news-index">${index + 1}.</span>
            <span class="news-title">${newsItem.title}</span>
            <a href="${newsItem.link}" class="news-link" target="_blank">→</a>
        `;

        newsList.appendChild(listItem);
    });
}

function continuouslyUpdateNews(interval) {

    window.electronAPI.sendData('request-news-data');
    
    setInterval(() => {
        
        console.log("test continuously update news")

        window.electronAPI.sendData('request-news-data');

    }, interval);
}

window.electronAPI.receiveData('response-news-data', (data) => {
    updateNewsData(data);
});

