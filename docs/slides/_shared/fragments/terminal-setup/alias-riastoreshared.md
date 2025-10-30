
Create riastoreshared alias

```bash
# Ensure ~/.bash_aliases exists and add riastoreshared (idempotent)
touch ~/.bash_aliases
if ! grep -qxF 'export riastoreshared=/storage/share/git/ria-store' ~/.bash_aliases; then
  echo 'export riastoreshared=/storage/share/git/ria-store' >> ~/.bash_aliases
  echo "Added riastoreshared to ~/.bash_aliases"
else
  echo "riastoreshared alias already present"
fi
```