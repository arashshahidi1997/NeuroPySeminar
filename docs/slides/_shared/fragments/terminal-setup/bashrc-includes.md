
Include aliases and functions in .bashrc
If you don't already have the following in ~/.bashrc, add it by running:

```bash
# Append a guarded include block for aliases & functions (idempotent)
BLOCK_START='# >>> seminar includes >>>'
BLOCK_END='# <<< seminar includes <<<'

if ! grep -q "$BLOCK_START" ~/.bashrc; then
cat <<'EOT' >> ~/.bashrc

# >>> seminar includes >>>
# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

if [ -f ~/.bash_functions ]; then
    . ~/.bash_functions
fi
# <<< seminar includes <<<
EOT
  echo "Added seminar include block to ~/.bashrc"
else
  echo "Seminar include block already present in ~/.bashrc"
fi
```