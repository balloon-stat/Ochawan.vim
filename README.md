Ochawan.vim
===========

�j�R�j�R�������̘g�Ƃ�ƁA�R�����g�̑���M���ł��܂��B  
if_python��K�v�Ƃ��܂��B  
�܂�alpha�o�[�W�����ł��B  

�u���E�U���J���̂�openbrowser.vim���g���Ă��܂��B  
https://github.com/tyru/open-browser.vim  


### �R�}���h


```
:OchawanStartLive
```

���݂̃o�b�t�@�̕������ɏ]���āA���������J�n���܂��B  
�������̋L�q���@��`nicolive_sample.desc`���Q�l�ɂ��Ă��������B  

```
:OchawanOpenBuf
```

�R�����g�̑���M���s����p�̃o�b�t�@���J���܂��B  

```
:OchawanConnectOnClip
```

�N���b�v�{�[�h�̃f�[�^������������URL���ǂ����������A  
��������URL�̏ꍇ�A�R�����g�T�[�o�ɐڑ����܂��B  

```
:OchawanSendMsg {string}
```

`{string}`�ƃR�����g���܂��B  
�R�����g�T�[�o�ɐڑ����Ă���K�v������܂��B  

```
:OchawanOnBouyomi {number}
```

`{number}`�� `0` �ȊO�̏ꍇ�A�R�����g��_�ǂ݂����ɑ���  
�ǂݏグ�Ă��炢�܂��B `0` ���w�肷��Ɠǂݏグ����߂܂��B

### ��p�o�b�t�@�̃L�[�}�b�v


`o` �v�����v�g�ֈړ����A���{����͂�ON�ő}�����[�h�ɂȂ�܂��B  
`q` �o�b�t�@���폜���܂��B  
`r` �O�̃E�B���h�E�ɖ߂�܂��B  
`t` �N���b�v�{�[�h�̃f�[�^������������URL�̏ꍇ�A�R�����g�T�[�o�ɐڑ����܂��B  
`@` 184�̐ݒ���g�O�����܂��B  
`<CR>` �v�����v�g�̍s�œ��͂����Ƃ��Ƀv�����v�g�̌��̕�������R�����g���܂��B  
�}�����[�h��`<CR>`���������ꍇ����L�Ɠ�����������܂��B  

`b` openbrowser.vim��`<Plug>(openbrowser-smart-search)`�����蓖�ĂĂ��܂��B  
`u` openbrowser.vim��`<Plug>(openbrowser-open)`�����蓖�ĂĂ��܂��B  



### �O���[�o���ϐ�


`g:ochawan_prompt` �o�b�t�@�̃v�����v�g `'> '`  
`g:ochawan_buf_height` �o�b�t�@�̍��� `'4'`  
`g:ochawan_is_anonymous` 184�̐ݒ� `1`  
`g:ochawan_do_bouyomi` �R�����g��_�ǂ݂����ɓǂ܂��� `0`  
`g:ochawan_openbrowser_command` �u���E�U���J���R�}���h `'OpenBrowser'`  

