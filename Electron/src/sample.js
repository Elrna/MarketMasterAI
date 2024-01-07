function sample () {
    var shell = new ActiveXObject('WSctipt.Shell');
    shell.Run('D:/MarketMasterAI/bin/getPrice_BTCUSDT_ochlv.exe salad 0', 0, true); 
}

sample();