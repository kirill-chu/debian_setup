set guifont=Monospace\ 12

function! FontSize(delta)
    let winpos = win_screenpos(0)
    let old_lines = &lines
    let old_columns = &columns
    
    let font = &guifont
    let size = matchstr(font, '\d\+$')
    if size != ''
        let new_size = size + a:delta
        if new_size > 6 && new_size < 50
            let &guifont = substitute(font, '\d\+$', new_size, '')

            set lines=999 columns=999
            " set lines=old_lines columns=old_columns
            " redraw!

        endif
    endif
endfunction

nnoremap <C-=> :call FontSize(1)<CR>
nnoremap <C-_> :call FontSize(-1)<CR>
nnoremap <C-0> :set guifont=Monospace\ Regular\ 12<CR>

" nnoremap <C-+> :set guifont=Monospace\ Regular\ 18<CR>
" nnoremap <C--> :let guifont=Monospace\ Regular\ 12<CR>
" nnoremap <C-0> :set guifont=Monospace\ Regular\ 12<CR>
" nnoremap <C-=> :set guifont=Monospace\ Regular\ 16<CR>
" nnoremap <C-_> :set guifont=Monospace\ Regular\ -1<CR>
" nnoremap <C-_> :let &guifont=substitute(&guifont, ' \d\+$', '\=submatch(0)-1', '')
" substitute(&guifont, '\d\+$', '\=submatch(0)-1', '')
" nnoremap <C-kPlus> :set guifont=Monospace\ Regular\ +1<CR>
" nnoremap <C-kMinus> :set guifont=Monospace\ Regular\ -1<CR>

