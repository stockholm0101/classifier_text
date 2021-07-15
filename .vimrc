" --------------------------------------��ʾ-------------------------------"
" ��������
set hlsearch
" ��ʾ�к�
set number
" ��ʾ�к�
set ruler
" ��ʾ��ǰ����
set showcmd
" �����﷨����
syntax on
set t_Co=256
"colorscheme ego

" --------------------------------------vim��������-------------------------------"
set encoding=gbk
let &termencoding=&encoding
set fileencodings=gb18030,utf-8,ucs-bom,gbk
let g:winManagerWindowLayout = 'BufExplorer|TagList'
let Tlist_Use_Right_Window=1
"��ֹ����
set visualbell t_vb=

" ���ɵ���ƶ����
" set mouse=a

"���ڼ�����ƶ�
nmap ,j <c-w>j
nmap ,h <c-w>h
nmap ,k <c-w>k
nmap ,l <c-w>l

" ʶ��.conf�ļ�����
au BufNewFile,BufRead *.conf set filetype=conf
" ֻ�е��ļ���c,cpp,python,shʱ����������
autocmd FileType c,cpp,python,sh set tabstop=4 shiftwidth=4 softtabstop=4 expandtab
set autoindent
" �����Զ���ȫ�����ƶ�����������м�
"inoremap " ""<ESC>i
"inoremap ' ''<ESC>i
"inoremap ( ()<ESC>i
"inoremap { {}<ESC>i
"inoremap [ []<ESC>i

" �ڵ�ǰ�����У�������г��ȹ�����������ʾ���پ���ʾ���٣�����Ҫ��������ʾ����
set display=lastline

" protobuf�﷨����
augroup filetype
  au! BufRead,BufNewFile *.proto setfiletype proto
augroup end

" ���õ�ǰ�е���ɫ�͸���
"set cursorline
"hi CursorLine cterm=NONE ctermbg=darkyellow ctermfg=lightgreen
set cursorline
hi CursorLine cterm=NONE ctermbg=240 ctermfg=lightgreen
set cursorcolumn
hi CursorColumn cterm=NONE ctermbg=240
"�ո����·�ҳ
nmap <space> <pagedown>
"�ո����Ϸ�ҳ
nmap <cr><cr> <pageup>

" ����list��ʾ�²��ɼ��ַ����滻��
set list
set listchars=tab:>-,trail:-

" --------- status line, command line {{{3
set statusline=%<%F\ %y\ %m%r%=0x%B\ %l/%L,%c%V\ [b%nw%{winnr()}]
" always display status line, 0 never, 1 more than 2 windows, 2 always
set laststatus=2
" ruler, command line appearance, if laststatus == 2, ruler is useless
set noruler " ru
set rulerformat =%30(%<%y\ %m%r%=0x%B\ %l,%c%V\ [%n]\ %P%)
" --------------------------------------�ļ�����---------------------------"
" �������ͼ��
filetype on
" �����ļ����Ͳ��
" filetype plugin on
" �����ļ������������
" filetype plugin indent on
filetype indent on
set backspace=indent,eol,start
" --------------------------------------undo-------------------------------"
set nobackup
" --------------------------------------�۵�-------------------------------"
set foldmethod=indent
" ���ļ�ʱĬ�ϲ��۵�����
set foldlevelstart=99


func SetTitle()
    if expand("%:e") == "py"
        call PythonHead()
    elseif expand("%:e") == "cpp"
        call CppHead()
    elseif expand("%:e") == 'h'
        call HFileHead()
    elseif expand("%:e") == 'sh'
        call ShellHead()
    endif
endfunc

"map <F4> :call SetTitle() <cr>'s
autocmd BufNewFile *.py,*.[ch],*.hpp,*.cpp,Makefile,*.mk,*.sh exec ":call SetTitle()"
" �Զ����pythonע��
func PythonHead()
    call append(0, "\#!/usr/bin/env python")
    call append(1, "\# -*- coding: gbk -*-")
    call append(2, "\"\"\"")
    call append(3, "  Author: work@company.com")
    call append(4, "  Date  : ".strftime("%y/%m/%d %H:%M:%S"))
    call append(5, "  File  : ".expand("%"))
    call append(6, "  Desc  : ")
    call append(7, "\"\"\"")
    call append(8, "")
    call append(9, "import sys")
    call append(10, "")
    call append(11, 'if __name__ == "__main__":')
    call append(12, "    pass")
endfunc

func CppHead()
    call append(0, "\/***************************************************************************************************")
    call append(1,  " * Author: work@company.com")
    call append(2,  " * Create: ".strftime("%y/%m/%d %H:%M:%S"))
    call append(3,  " * File  : ".expand("%"))
    call append(4,  " * Description: ")
    call append(5,  " * Copyright (c) ".strftime("%Y")." Baidu.com, Inc. All Rights Reserved")
    call append(6,  "***************************************************************************************************\/")
endfunc

func HFileHead()
    call append(0, "\/***************************************************************************************************")
    call append(1,  " * Author: work@company.com")
    call append(2,  " * Create: ".strftime("%y/%m/%d %H:%M:%S"))
    call append(3,  " * File  : ".expand("%"))
    call append(4,  " * Description: ")
    call append(5,  " * Copyright (c) ".strftime("%Y")." Baidu.com, Inc. All Rights Reserved")
    call append(6,  "***************************************************************************************************\/")
    call append(7,  "")
    call append(8,  "#ifndef __".toupper(expand("%:t:r"))."_H__")
    call append(9,  "#define __".toupper(expand("%:t:r"))."_H__")
    call append(10, "")
    call append(11, "")
    call append(12, "")
    call append(13, "")
    call append(14, "")
    call append(15, "#endif //__".toupper(expand("%:t:r"))."_H__")
endfunc

func ShellHead()
    call append(0, "\#!/bin/bash")
    call append(1, "\#==================================================================================================#")
    call append(2, "\# Author: work@company.com")
    call append(3, "\# Date  : ".strftime("%y/%m/%d %H:%M:%S"))
    call append(4, "\# File  : ".expand("%"))
    call append(5, "\# Description: ")
    call append(6, "\#==================================================================================================#")
endfunc
