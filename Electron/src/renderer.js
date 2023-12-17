// renderer.js

document.addEventListener('DOMContentLoaded', () => {
    
    const navItems = document.querySelectorAll('.nav-item');
    const contentSections = document.querySelectorAll('.content-section');
    // すべてのコンテンツセクションを非表示にする
    contentSections.forEach(section => {
        section.style.display = 'none';
    });

    navItems.forEach(item => {
        item.addEventListener('click', function() {
            // すべてのコンテンツセクションを非表示にする
            contentSections.forEach(section => {
                section.style.display = 'none';
            });

            //クリックされた項目に応じてコンテンツセクションを表示
            const contentId = 'content-' + this.id;
            const activeContent = document.getElementById(contentId);
            console.log(activeContent);

            if(activeContent) {
                activeContent.style.display = 'block';
            }

            //ナビゲーションのアクティブ状態を更新
            navItems.forEach(nav => nav.classList.remove('active-nav-item'));
            this.classList.add('active-nav-item');
        });
    });

    // 初期状態として「Home」をアクティブにする
    const homeContent = document.getElementById('content-home');
    if (homeContent) {
        homeContent.classList.add('visible');
        homeContent.style.display = 'block';
    }
    const homeItem = document.getElementById('home');
    if (homeItem) {
        homeItem.classList.add('active-nav-item');
    }

    //CSVデータ更新の設定
    setInterval(() => {
        const requestCsvData = new Event('request-csv-data');
        document.dispatchEvent(requestCsvData);
    }, 60000);

    window.electronAPI.receiveData('response-data', (data) => {
        const lastElement = data[data.length - 1];
        updateBTCWidget(lastElement.close);
    });

});

function updateBTCWidget(closePrice) {
    const widgetPrice = document.querySelector('.widget-price');
    widgetPrice.textContent = closePrice;
}
