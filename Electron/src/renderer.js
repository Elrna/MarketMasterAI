// renderer.js
let lastPrice = 0;
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
    window.electronAPI.sendData('request-csv-data');

    setInterval(() => {
        window.electronAPI.sendData('request-csv-data');
        console.log('request csv data.');

    }, 60000);

    window.electronAPI.receiveData('csv-data-response', (data) => {
        console.log(data);
        const newPrice = parseFloat(data.lastClose);
        const targetPrice = parseFloat(data.targetData);

        if (!isNaN(newPrice)) {
            updateBTCWidget(newPrice, targetPrice);
        }else{
            console.log('newPrice is not a number.');
        }


        console.log('update BTC widget.');
    });

});

function updateBTCWidget(newPrice, targetPrice) {
    const widgetPrice = document.querySelector('.widget-price');
    const changeIndicator = document.querySelector('.widget-change');
  
    if (widgetPrice && changeIndicator) {
        widgetPrice.textContent = newPrice.toFixed(2); // 価格を小数点以下2桁で表示
        changeIndicator.textContent = raito(targetPrice, newPrice).toFixed(2) + '%'; // 前日比を小数点以下2桁で表示

        // 価格が変動したかどうかをチェック
        if (newPrice !== null) {
            if (newPrice > lastPrice) {
                changeIndicator.classList.remove('negative');
                widgetPrice.classList.remove('negative');
                changeIndicator.classList.add('positive');
                widgetPrice.classList.add('positive');

            } else if (newPrice < lastPrice) {
                changeIndicator.classList.remove('positive');
                widgetPrice.classList.remove('positive');
                changeIndicator.classList.add('negative');
                widgetPrice.classList.add('negative');
            }
        }
        
      lastPrice = newPrice;
    }
  }

  function raito(targetPrice, lastPrice){
    console.log('targetPrice: ' + targetPrice);
    console.log('lastPrice: ' + lastPrice);
    return (targetPrice - lastPrice) / lastPrice * 100;
  }
