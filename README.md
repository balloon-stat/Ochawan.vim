Ochawan.vim
===========

ニコニコ生放送の枠とりとコメントの送信、受信ができます。  
if_pythonを必要とします。  
まだalphaバージョンです。  

ブラウザを開くのにopenbrowser.vimが使っています。  
https://github.com/tyru/open-browser.vim  

#### コマンド

```
:OchawanStartLive
```

現在のバッファに書かれた放送情報に従って、生放送を開始します。  
放送情報の記述方法は`nicolive_sample.desc`を参考にしてください。  

```
:OchawanOpenBuf
```

コメントの送受信を行う専用のバッファを開きます。  

```
:OchawanConnectOnClip
```

クリップボードのデータが生放送中のURLかどうかを試し、  
放送中のURLの場合、コメントサーバに接続します。  

```
:OchawanSendMsg {string}
```

`{string}`とコメントします。  
コメントサーバに接続してある必要があります。  

### 専用バッファのキーマップ

`o` 日本語入力をONにして、入力待ちになります。  
`q` バッファを削除します。  
`r` 前のウィンドウに戻ります。  
`t` クリップボードのデータが生放送中のURLの場合、コメントサーバに接続します。  
`@` 184の設定をトグルします。  
`<CR>` プロンプトの行で入力したときにプロンプトの後ろの文字列をコメントします。  
挿入モードで`<CR>`を押した場合も上記と同じ動作をします。  

`b` openbrowser.vimの`<Plug>(openbrowser-smart-search)`を割り当てています。  

#### グローバル変数

`g:ochawan_prompt` バッファのプロンプト `'> '`  
`ochawan_buf_height` バッファの高さ `'4'`  
`ochawan_is_anonymous` 184の設定 `1`  

