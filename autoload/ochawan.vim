
let s:save_cpo = &cpo
set cpo&vim

let s:ochawan_is_initialized = 0

let s:path = expand("<sfile>:p:h")
python <<EOM
import sys, vim
if not vim.eval('s:path') in sys.path:
  sys.path.append(vim.eval('s:path'))
EOM

function! s:init()
  if s:ochawan_is_initialized
    return 1
  endif
  if !has("python")
    echoerr "This plugin needs python"
    return 0
  endif
  python from Broadcast import Broadcast
  python ochawan = Broadcast(vim.eval('$HOME'))
  if g:ochawan_is_bouyomi
    python ochawan.doBouyomi()
  endif
  let s:ochawan_is_initialized = 1
  return 1
endfunction

function! ochawan#live()
  if s:init()
    if exists("g:openbrowser_open_filepath_in_vim")
      let save_op = g:openbrowser_open_filepath_in_vim
      let g:openbrowser_open_filepath_in_vim = 0
      python ochawan.live()
      let g:openbrowser_open_filepath_in_vim = save_op
    else
      python ochawan.live()
    endif
  endif
endfunction

function! ochawan#connect()
  if s:init()
    let url = getreg('+')
    let prefix = 'http://live.nicovideo.jp/watch/'
    if url !~# '^'.prefix
      return
    endif
    let url = substitute(url, prefix, '', '')
    let idx = stridx(url, '?')
    let lvid = strpart(url, 0, idx == -1 ? strlen(url) : idx)
    python ochawan.connect(vim.eval('lvid'))
    echo "connect: ".lvid
  endif
endfunction

function! ochawan#open()
  if s:init()
    call s:open_buf()
    call cursor(1, strlen(g:ochawan_prompt))
    if s:is_connect()
      call s:writing()
    endif
  endif
endfunction

function! s:is_connect()
  redir => x
    silent python print ochawan.is_connect()
  redir END
  "echom 'connect: '.x
  return  strpart(x, 1) == 'True'
endfunction

function! s:open_buf()
  let bufwn = bufwinnr('ochawan_chat')
  if bufwn > 0
    execute bufwn.'wincmd w'
    return
  endif
  if bufexists('ochawan_chat')
    belowright sbuffer ochawan_chat
    execute g:ochawan_buf_height.' wincmd _'
    call setline(1, g:ochawan_prompt)
    return
  endif
  execute 'silent belowright split ochawan_chat'
  execute g:ochawan_buf_height.' wincmd _'
  call setline(1, g:ochawan_prompt)
  call s:poll()
  call s:settings_chat_buf()
  let &filetype = 'ochawan_chat'
  setlocal buftype=nofile
  setlocal noswapfile
  python ochawan_buf = vim.current.buffer
endfunction

function! s:writing()
  call setline(1, g:ochawan_prompt)
  startinsert
  call cursor(1, strlen(g:ochawan_prompt)+1)
  let &iminsert = 2
endfunction

function! s:settings_chat_buf()
  nmap <buffer> b <Plug>(openbrowser-smart-search)
  nmap <buffer> u <Plug>(openbrowser-open)
  nnoremap <silent> <buffer> o :<C-u>call <SID>writing()<CR>
  nnoremap <silent> <buffer> q :<C-u>bwipeout<CR>
  nnoremap <silent> <buffer> r :<C-u>wincmd p<CR>
  nnoremap <silent> <buffer> t :<C-u>call ochawan#connect()<CR>
  nnoremap <silent> <buffer> @ :<C-u>call <SID>toggle_anonym()<CR>
  inoremap <silent> <buffer> <C-@> <ESC>:call <SID>toggle_anonym()<CR>a
  nnoremap <silent> <buffer> <CR> :<C-u>call <SID>send_message()<CR>
  inoremap <silent> <buffer> <CR> <ESC>:call <SID>send_message()<CR>a
  inoremap <silent> <buffer> <Up> <Nop>
  inoremap <silent> <buffer> <Down> <Nop>
  setlocal nonumber
endfunction

function! s:toggle_anonym()
  let g:ochawan_is_anonymaous = !g:ochawan_is_anonymaous
  if g:ochawan_is_anonymaous
    echo "set to say anonymous"
  else
    echo "set to say non-anonymous"
  endif
endfunction

function! s:poll()
  augroup ochawan_chat
    autocmd!
    autocmd BufDelete <buffer> call s:exit_live()
    autocmd CursorHold  * silent call feedkeys("g\<ESC>", 'n')
    "autocmd CursorHoldI * silent call feedkeys("\<C-g>\<ESC>", 'n')
    autocmd CursorHold,CursorHoldI * python ochawan.rendering(ochawan_buf)
  augroup END
endfunction

function! s:exit_live()
  augroup ochawan_chat
    autocmd!
  augroup END
  python ochawan.stop()
  echo "Exit ochawan"
endfunction

function! s:send_message()
  let line = getline(1)
  if line =~# '^'.g:ochawan_prompt
    let text = strpart(line, 2)
    call ochawan#send(text)
  endif
  call setline(1, g:ochawan_prompt)
  call cursor(1, strlen(g:ochawan_prompt))
endfunction

function! ochawan#send(text)
  let body = iconv(a:text, &encoding, "utf-8")
  python ochawan.send(vim.eval('body'),vim.eval('g:ochawan_is_anonymaous'))
endfunction

function! ochawan#bouyomi(do)
  if s:init()
    if a:do
      python ochawan.doBouyomi()
    else
      python ochawan.dontBouyomi()
    endif
  endif
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo

