const { app, BrowserWindow, ipcMain, Menu } = require('electron');
const fs = require('fs');
const axios = require('axios');
const path = require('path');
const csv = require('csv-parser');


const jPaths = "D:/MarketMasterAI/Def/Path.json";
var filePaths = [];

app.whenReady().then(() => {
  filePaths = loadFilePathJson();
  createWindow();
  /*continuouslyRunExe(filePaths.exe_paths['Technical'], 300000);*/
  continuouslyRunExe(filePaths.exe_paths['getNews'], 300000);
});

ipcMain.on('request-indicators-data', (event) => {
  readFileAsync(filePaths.json_paths['Technical'], event, 'response-indicators-data');
});

ipcMain.on('request-path-list', (event) => {
  event.reply('path-list', filePaths);
});

ipcMain.on('request-news-data', (event) => {
  
  console.log('request news data')
  fs.readFile(filePaths.json_paths['News'], 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading file:', err);
      event.reply('response-news-data', { error: 'ファイル読み込みエラー' });
    } else {
      event.reply('response-news-data', JSON.parse(data));
    }
  });
});

ipcMain.on('request-LSTM_output', (event) => {
  readCSV(event, 'response-LSTM_output');
});

['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'SOLUSDT', 'AVAXUSDT'].forEach(symbol => {
  ipcMain.on(`s${symbol}-current-price`, async (event) => {
    try {
      const [currentPrice, previousPrice] = await getCurrentAndPreviousPrice(symbol);
      event.reply(`r${symbol}-current-price`, { currentPrice, previousPrice });
    } catch (error) {
      console.error(`Error getting price for ${symbol}:`, error);
      event.reply(`r${symbol}-current-price`, { error: '価格データの取得に失敗しました' });
    }
  });
});


app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    }
  });

  Menu.setApplicationMenu(null);
  mainWindow.loadFile('index.html');
  mainWindow.maximize();
}

async function getCurrentAndPreviousPrice(symbol) {
  const priceUrl = `https://api.binance.com/api/v3/ticker/price?symbol=${symbol}`;
  const klinesUrl = `https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=1d&startTime=${Date.now() - 86400000}&endTime=${Date.now()}`;

  const [currentPriceData, previousPriceData] = await Promise.all([
    getPriceData(priceUrl),
    getPriceData(klinesUrl)
  ]);

  const currentPrice = currentPriceData.price;
  const previousPrice = previousPriceData[0][1];

  return [currentPrice, previousPrice];
}

async function getPriceData(url) {
  try {
    const response = await axios.get(url);

    return response.data;
  } catch (error) {
    throw error; // エラーを再スローして、呼び出し元でキャッチできるようにする
  }
}

function loadFilePathJson() {
  try {
    const data = fs.readFileSync(jPaths, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error('Error reading file paths:', error);
    return null;
  }
}

function readFileAsync(filePath, event, replyChannel) {
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading file:', err);
      event.reply(replyChannel, { error: 'ファイル読み込みエラー' });
    } else {
      event.reply(replyChannel, JSON.parse(data));
    }
  });
}

function readCSV(event, replyChannel) {
  const filePath = filePaths.csv_paths['LSTM_output'];
  let data = [];

  fs.createReadStream(filePath)
    .pipe(csv())
    .on('data', (row) => {
        data.push(row);
    })
    .on('end', () => {
        event.reply(replyChannel, data);
    })
    .on('error', (error) => {
      console.error('Error reading CSV file:', error);
      event.reply(replyChannel, { error: 'Error reading CSV file' });
    });
}

function runExe(filePath){
    // 非同期処理で子プロセスを起動
    const child = spawn(filePath);
    console.log('exe prosecc start.');

    child.stdout.on('data', (data) => {
      console.log(`stdout: ${data}`);
    });
  
    child.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });
  
    child.on('close', (code) => {
      console.log(`child process exited with code ${code}`);
    });
  
    child.on('error', (err) => {
      console.error('Failed to start subprocess.', err);
    });
}

function continuouslyRunExe(filePath, interval) {
  setInterval(() => {
    /*runExe(filePath)
      .then(code => console.log(`Execution completed with code: ${code}`))
      .catch(err => console.error('Execution failed:', err));*/
  }, interval);
}