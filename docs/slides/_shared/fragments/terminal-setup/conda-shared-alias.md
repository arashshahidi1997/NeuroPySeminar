
Add conda-shared alias
```bash
# Add conda-shared alias (idempotent)
if ! grep -qxF "alias conda-shared='source /storage/share/python/environments/Anaconda3/etc/profile.d/conda.sh && echo \"→ Using shared Conda\"'" ~/.bashrc; then
  echo "alias conda-shared='source /storage/share/python/environments/Anaconda3/etc/profile.d/conda.sh && echo \"→ Using shared Conda\"'" >> ~/.bashrc
  echo "Added conda-shared alias to ~/.bashrc"
else
  echo "conda-shared alias already present in ~/.bashrc"
fi
```