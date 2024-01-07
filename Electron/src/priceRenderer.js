<<<<<<< HEAD
<<<<<<< HEAD

document.addEventListener('DOMContentLoaded', () => {
  
  function addTradingViewWidget() {

    const chartContainer = document.getElementById('chartContainer');
    const priceChartElement = document.getElementById('priceChart');
    if (!priceChartElement) {
      console.error('priceChart element not found');
      return;
    }
  
    var navHeight = document.querySelector('.nav').offsetHeight;

    var chartHeight = window.innerHeight - navHeight - 100;

    const script = document.createElement('script');
    script.src = 'https://s3.tradingview.com/tv.js';
    script.async = true;
    script.onload = () => {
      new TradingView.widget({
        "container_id": priceChartElement.id,
        "width": '70%',
        "height": chartHeight,
        "symbol": "ByBit:BTCUSDT",
        "interval": "60",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "ja",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "withdateranges": true,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "show_popup_button": true,
        "popup_width": '800',
        "popup_height": '600',
      });
    };

    document.body.appendChild(script);
  }

  // ウィジェットを追加する関数を呼び出します。
  addTradingViewWidget();

  window.electronAPI.sendData('request-indicators-data');

  // mainプロセスからのデータレスポンスを受け取る
  window.electronAPI.receiveData('response-indicators-data', (data) => {
    if (data.error) {
      console.error('Error:', data.error);
    } else {
      updateIndicatorsStatus(data);
    }
  });
});

function updateIndicatorsStatus(data) {
  for (const indicator in data) {
    const indicatorElement = document.getElementById(`${indicator}-indicator`);
    if (data[indicator]) {
      indicatorElement.classList.add('active');
      indicatorElement.classList.remove('inactive');
    } else {
      indicatorElement.classList.add('inactive');
      indicatorElement.classList.remove('active');
    }
  }
}
=======
=======
>>>>>>> 7c0f11edcfe2c5065551d8214761ecb4cc2be555

document.addEventListener('DOMContentLoaded', () => {
  
  function addTradingViewWidget() {

    const chartContainer = document.getElementById('chartContainer');
    const priceChartElement = document.getElementById('priceChart');
    if (!priceChartElement) {
      console.error('priceChart element not found');
      return;
    }
  
    var navHeight = document.querySelector('.nav').offsetHeight;

    var chartHeight = window.innerHeight - navHeight - 100;

    const script = document.createElement('script');
    script.src = 'https://s3.tradingview.com/tv.js';
    script.async = true;
    script.onload = () => {
      new TradingView.widget({
        "container_id": priceChartElement.id,
        "width": '70%',
        "height": chartHeight,
        "symbol": "ByBit:BTCUSDT",
        "interval": "60",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "ja",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "withdateranges": true,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "show_popup_button": true,
        "popup_width": '800',
        "popup_height": '600',
      });
    };

    document.body.appendChild(script);
  }

  // ウィジェットを追加する関数を呼び出します。
  addTradingViewWidget();

  window.electronAPI.sendData('request-indicators-data');

  // mainプロセスからのデータレスポンスを受け取る
  window.electronAPI.receiveData('response-indicators-data', (data) => {
    if (data.error) {
      console.error('Error:', data.error);
    } else {
      updateIndicatorsStatus(data);
    }
  });
});

function updateIndicatorsStatus(data) {
  for (const indicator in data) {
    const indicatorElement = document.getElementById(`${indicator}-indicator`);
    if (data[indicator]) {
      indicatorElement.classList.add('active');
      indicatorElement.classList.remove('inactive');
    } else {
      indicatorElement.classList.add('inactive');
      indicatorElement.classList.remove('active');
    }
  }
}
<<<<<<< HEAD
>>>>>>> 7c0f11edcfe2c5065551d8214761ecb4cc2be555
=======
>>>>>>> 7c0f11edcfe2c5065551d8214761ecb4cc2be555
