

document.addEventListener('DOMContentLoaded', () => {
    
    const navItems = document.querySelectorAll('.nav-item');
    const contentSections = document.querySelectorAll('.content-section');

    const btc_widgetPrice =  document.getElementById('BTCPrice');
    const btc_changeIndicator = document.getElementById('BTCRaito');
    const eth_widgetPrice = document.getElementById('ETHPrice');
    const eth_changeIndicator = document.getElementById('ETHRaito');
    const xrp_widgetPrice = document.getElementById('XRPPrice');
    const xrp_changeIndicator = document.getElementById('XRPRaito');
    const sol_widgetPrice = document.getElementById('SOLPrice');
    const sol_changeIndicator = document.getElementById('SOLRaito');


    contentSections.forEach(section => {
        section.style.display = 'none';
    });

    navItems.forEach(item => {
        item.addEventListener('click', function() {

            contentSections.forEach(section => {
                section.style.display = 'none';
            });

            const contentId = 'content-' + this.id;
            const activeContent = document.getElementById(contentId);
            console.log(activeContent);

            if(activeContent) {
                activeContent.style.display = 'block';
            }

            navItems.forEach(nav => nav.classList.remove('active-nav-item'));
            this.classList.add('active-nav-item');
        });
    });

    const homeContent = document.getElementById('content-home');
    if (homeContent) {
        homeContent.classList.add('visible');
        homeContent.style.display = 'block';
    }
    const homeItem = document.getElementById('home');
    if (homeItem) {
        homeItem.classList.add('active-nav-item');
    }

    window.electronAPI.sendData('sBTCUSDT-current-price');

    window.electronAPI.receiveData('rBTCUSDT-current-price', (data) => {

        var currentPrice = data.currentPrice;
        var previousPrice = data.previousPrice;

        updateWidget(currentPrice, previousPrice, btc_widgetPrice, btc_changeIndicator);
    });

    window.electronAPI.sendData('sETHUSDT-current-price');

    window.electronAPI.receiveData('rETHUSDT-current-price', (data) => {

        var currentPrice = data.currentPrice;
        var previousPrice = data.previousPrice;
        
        updateWidget(currentPrice, previousPrice, eth_widgetPrice, eth_changeIndicator);

    });

    window.electronAPI.sendData('sXRPUSDT-current-price');

    window.electronAPI.receiveData('rXRPUSDT-current-price', (data) => {

        var currentPrice = data.currentPrice;
        var previousPrice = data.previousPrice;
        
        updateWidget(currentPrice, previousPrice, xrp_widgetPrice, xrp_changeIndicator);

    });

    window.electronAPI.sendData('sSOLUSDT-current-price');

    window.electronAPI.receiveData('rSOLUSDT-current-price', (data) => {

        var currentPrice = data.currentPrice;
        var previousPrice = data.previousPrice;
        
        updateWidget(currentPrice, previousPrice, sol_widgetPrice, sol_changeIndicator);

    });
});

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
