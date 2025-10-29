---
title: "VSCode Guide"
author: "Sirota Lab"
theme: "black"
width: 1280
height: 720
---

# VSCode Guide


---

# 🧠 NeuroPy VSCode Setup Guide

### 1. Open VSCode

Press

```
Ctrl + Shift + P
```

A command box will appear.

### 2. Connect via Remote-SSH

Type and select:

```
Remote-SSH: Connect to Host...
```

Enter your host (replace `<XX>` with your ephys ID):

```bash
ephys<XX>@gamma3
```

Enter your **password** when prompted.

### 3. Open Folder

Select:

```
Open Folder
```

By default, `/home/ephys<XX>` will appear.
Delete it and instead type:

```bash
/storage2/arash/teaching/neuropy/<name>
```

> Replace `<name>` with your **first name in lowercase**.

When prompted, select:

> ✅ Yes, I trust the authors

---

### 4. Activate the `neuropy-env` environment

Open VSCode terminal

```bash
Ctrl + J
```

In the VSCode terminal, run:

```bash
conda activate neuropy-env
```

---

### 5. Set Python Inerpreter to `neuropy-env`

```bash
Ctrl + Shift + P
```
type:
```
Python: Select Interpreter
```
choose `neuropy-env`

---

### 6. For `jupyter notebooks`: Set kernel to `neuropy-env`

1. Click on the **kernel name** in the top-right of VSCode.
2. Choose **Python Environments** → select:

   ```
   neuropy-env
   ```

---

✅ **Done!** You’re ready to start working in the NeuroPy environment.

---

