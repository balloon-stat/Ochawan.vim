
if exists('g:loaded_ochawan')
  finish
endif

let s:save_cpo = &cpo
set cpo&vim

command! -nargs=0 OchawanStartLive call ochawan#live()
command! -nargs=0 OchawanOpenBuf call ochawan#open()
command! -nargs=0 OchawanConnectLive call ochawan#connect()
command! -nargs=1 OchawanSendMsg call ochawan#send(<q-args>)

let g:ochawan_prompt = get(g:, 'ochawan_prompt', '> ')
let g:ochawan_buf_height = get(g:, 'ochawan_buf_height', '4')
let g:ochawan_is_anonymaous = get(g:, 'ochawan_is_anonymous', 1)
let g:loaded_ochawan = 1

let &cpo = s:save_cpo
unlet s:save_cpo

