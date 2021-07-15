" --------------------------------------显示-------------------------------"
" 搜索高亮
set hlsearch
" 显示行号
set number
" 显示列号
set ruler
" 显示当前命令
set showcmd
" 开启语法高亮
syntax on
set t_Co=256
"colorscheme ego

" --------------------------------------vim基本设置-------------------------------"
set encoding=gbk
let &termencoding=&encoding
set fileencodings=gb18030,utf-8,ucs-bom,gbk
let g:winManagerWindowLayout = 'BufExplorer|TagList'
let Tlist_Use_Right_Window=1
"禁止响铃
set visualbell t_vb=

" 鼠标可点击移动光标
" set mouse=a

"窗口间快速移动
nmap ,j <c-w>j
nmap ,h <c-w>h
nmap ,k <c-w>k
nmap ,l <c-w>l

" 识别.conf文件类型
au BufNewFile,BufRead *.conf set filetype=conf
" 只有当文件是c,cpp,python,sh时，设置缩进
autocmd FileType c,cpp,python,sh set tabstop=4 shiftwidth=4 softtabstop=4 expandtab
set autoindent
" 括号自动补全，并移动光标至括号中间
"inoremap " ""<ESC>i
"inoremap ' ''<ESC>i
"inoremap ( ()<ESC>i
"inoremap { {}<ESC>i
"inoremap [ []<ESC>i

" 在当前窗口中，如果单行长度过长，则能显示多少就显示多少，不需要将整行显示出来
set display=lastline

" protobuf语法高亮
augroup filetype
  au! BufRead,BufNewFile *.proto setfiletype proto
augroup end

" 设置当前行的颜色和高亮
"set cursorline
"hi CursorLine cterm=NONE ctermbg=darkyellow ctermfg=lightgreen
set cursorline
hi CursorLine cterm=NONE ctermbg=240 ctermfg=lightgreen
set cursorcolumn
hi CursorColumn cterm=NONE ctermbg=240
"空格向下翻页
nmap <space> <pagedown>
"空格向上翻页
nmap <cr><cr> <pageup>

" 更改list显示下不可见字符的替换符
set list
set listchars=tab:>-,trail:-

" --------- status line, command line {{{3
set statusline=%<%F\ %y\ %m%r%=0x%B\ %l/%L,%c%V\ [b%nw%{winnr()}]
" always display status line, 0 never, 1 more than 2 windows, 2 always
set laststatus=2
" ruler, command line appearance, if laststatus == 2, ruler is useless
set noruler " ru
set rulerformat =%30(%<%y\ %m%r%=0x%B\ %l,%c%V\ [%n]\ %P%)
" --------------------------------------文件类型---------------------------"
" 开启类型检测
filetype on
" 开启文件类型插件
" filetype plugin on
" 开启文件类型缩进插件
" filetype plugin indent on
filetype indent on
set backspace=indent,eol,start
" --------------------------------------undo-------------------------------"
set nobackup
" --------------------------------------折叠-------------------------------"
set foldmethod=indent
" 打开文件时默认不折叠代码
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
" 自动添加python注释
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
