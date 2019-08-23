
vim-enhanced:
  pkg.installed

/etc/vimrc:
  file.managed:
    - source:
      - salt://vimrc.vim
    - user: root
    - group: root
    - mode: '0644'

