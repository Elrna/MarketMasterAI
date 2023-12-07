// ニュースデータを取得して表示する関数
function fetchAndDisplayNews() {

    const filePath = 'D:/MarketMasterAI/bin/trending_news.json';

    if (window.electronAPI && window.electronAPI.readJsonFile) {
        window.electronAPI.readJsonFile(filePath, (err, data) => {
            if (err) {
                console.error('Failed to read JSON file', err);
                return;
            }

            const newsData = data;

            // ニュースコンテナを取得
            const newsContainer = document.getElementById('main-content');

            // 既存のニュースをクリア
            newsContainer.innerHTML = '';

            // ニュースデータをループしてHTMLを生成
            newsData.forEach(news => {
                const newsItem = `
                    <div class="news-item">
                        <h3>${news.title}</h3>
                        <a href="${news.link}" target="_blank">詳細を見る</a>
                    </div>
                `;
                newsContainer.innerHTML += newsItem;
            });
        });

    } else {
        console.error('electronAPI or electronAPI.readJsonFile is not available', window.electronAPI);
    }
}

module.exports = fetchAndDisplayNews;
