#!/bin/bash

set -eo pipefail

pacman -Sy --noconfirm \
  base-devel \
  git \
  zsh \
  bash \
  vim \
  neovim \
  python-neovim \
  tmux \
  curl \
  ripgrep \
  shellcheck \
  fzf

chsh -s /bin/zsh

if [[ -n "$DEVBOX_ALL" ]]; then
  DEVBOX_PYTHON=yes
  DEVBOX_NODE=yes
  DEVBOX_JAVA=yes
  DEVBOX_CLANG=yes
  DEVBOX_RUST=yes
fi

if [[ -n "$DEVBOX_PYTHON" ]]; then
  pacman -Sy --noconfirm python
fi

if [[ -n "$DEVBOX_NODE" ]]; then
  pacman -Sy --noconfirm \
    nodejs \
    yarn
fi

if [[ -n "$DEVBOX_CLANG" ]]; then
  pacman -Sy --noconfirm \
    clang \
    llvm
fi

if [[ -n "$DEVBOX_JAVA" ]]; then
  pacman -Sy --noconfirm \
    java-runtime-common \
    java-environment-common
fi

if [[ -n "$DEVBOX_RUST" ]]; then
  curl -s -f https://sh.rustup.rs > rust-install.sh
  sh rust-install.sh -y
  rm rust-install.sh
fi
