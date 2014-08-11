Ochawan.vim
===========

ニコニコ生放送の枠とりと、コメントの送受信ができます。  
if_pythonを必要とします。  
まだalphaバージョンです。  

ブラウザを開くのにopenbrowser.vimを使っています。  
https://github.com/tyru/open-browser.vim  


### コマンド


```
:OchawanStartLive
```

現在のバッファの放送情報に従って、生放送を開始します。  
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

```
:OchawanOnBouyomi {number}
```

`{number}`が `0` 以外の場合、コメントを棒読みちゃんに送り  
読み上げてもらいます。 `0` を指定すると読み上げをやめます。

### 専用バッファのキーマップ


`o` プロンプトへ移動し、日本語入力をONで挿入モードになります。  
`q` バッファを削除します。  
`r` 前のウィンドウに戻ります。  
`t` クリップボードのデータが生放送中のURLの場合、コメントサーバに接続します。  
`@` 184の設定をトグルします。  
`<CR>` プロンプトの行で入力したときにプロンプトの後ろの文字列をコメントします。  
挿入モードで`<CR>`を押した場合も上記と同じ動作をします。  

`b` openbrowser.vimの`<Plug>(openbrowser-smart-search)`を割り当てています。  
`u` openbrowser.vimの`<Plug>(openbrowser-open)`を割り当てています。  



### グローバル変数


`g:ochawan_prompt` バッファのプロンプト `'> '`  
`g:ochawan_buf_height` バッファの高さ `'4'`  
`g:ochawan_is_anonymous` 184の設定 `1`  
`g:ochawan_do_bouyomi` コメントを棒読みちゃんに読ませる `0`  
`g:ochawan_openbrowser_command` ブラウザを開くコマンド `'OpenBrowser'`  

