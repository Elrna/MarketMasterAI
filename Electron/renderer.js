

document.getElementById('sidebar').addEventListener('click', function(e) {
    if (e.target && e.target.nodeName === "LI") {
        changeContent(e.target.id);
    }
});

function changeContent(contentId) {
    const content = document.getElementById('main-content');
    // コンテンツをクリア
    content.innerHTML = '';

    // 各タブの内容をダミーデータで生成
    switch(contentId) {
        case 'home':
            // ホームのコンテンツを設定
            fetchAndDisplayNews();
            break;
        case 'stocks':
            // 株価のコンテンツを設定
            content.innerHTML = '<h1>株価</h1><p>チャート機能がここに表示されます。</p>';
            break;
        case 'analysis':
            // 分析のコンテンツを設定
            content.innerHTML = '<h1>分析</h1><p>市場分析結果がここに表示されます。</p><p>LSTM株価予測: 予測値がここに表示されます。</p><p>総合スコア: スコアがここに表示されます。</p>';
            break;
        case 'auto-trading':
            // 自動トレーディングのコンテンツを設定
            content.innerHTML = '<h1>自動トレーディング</h1><p>設定した指標: 指標がここに表示されます。</p><p>自動取引履歴がここに表示されます。</p>';
            break;
        case 'portfolio':
            // ポートフォリオのコンテンツを設定
            content.innerHTML = '<h1>ポートフォリオ</h1><p>資産: 資産額がここに表示されます。</p><p>損益: 損益がここに表示されます。</p><p>予想税金: 税金がここに表示されます。</p>';
            break;
        default:
            content.innerHTML = '<h1>選択したタブの名前が表示されます</h1>';
    }
}

changeContent('home');