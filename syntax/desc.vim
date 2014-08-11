
if exists("b:current_syntax")
  finish
endif

if !exists('main_syntax')
  let main_syntax = 'live_description'
endif

runtime! syntax/html.vim
unlet! b:current_syntax

syn match DescKeyword '^\(Broadcast_on:\|Title:\|Category:\|Tags:\)'
syn match DescBlock '^>>\s*Description\|^Description\s*<<'

hi def link DescKeyword Title
hi def link DescBlock Title

let b:current_syntax = "live_description"
if main_syntax ==# 'live_description'
  unlet main_syntax
endif
