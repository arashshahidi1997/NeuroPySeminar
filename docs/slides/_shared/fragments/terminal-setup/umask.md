### UMASK for contribution (optional)

```bash
# set umask so that new file creation preserves group permissions (idempotent)
if ! grep -qxF 'umask 0002' ~/.bashrc; then
  echo 'umask 0002' >> ~/.bashrc
  echo "Added 'umask 0002' to ~/.bashrc"
else
  echo "'umask 0002' already present in ~/.bashrc"
fi
Warning: Under shared folders, others can modify files you create if group permissions allow it.
