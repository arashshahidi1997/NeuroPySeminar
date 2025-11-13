# Holoviews

---

## Step 0: Setup
Open VSCode, Remote-SSH: Connect to Host and open the folder:

```bash
/storage2/arash/teaching/neuropy/<your_name>
```

At this point you probably have a shortcut to this folder in your VSCode.

Then activate the `neuropy-env` environment:

```bash
conda activate neuropy-env
```

---

## Step 1: Get the holoviews tutorial repository
cd to your NeuroPySeminar folder:
```bash
cd NeuroPySeminar
```

Update the repository content:

```bash
datalad update --merge
```

then get the holoviews subdataset:
```bash
datalad get tutorials/holoviews
```

It will start downloading the contents from [holoviews github repository](https://github.com/holoviz/holoviews/tree/main)

NOTE: if you get an error here, please see the next slide

---

In case of an error in the last step, you can try to clone the holoviews repository manually:

```bash
datalad install -d . -s "https://github.com/holoviz/holoviews/tree/main" tutorials/holoviews
```

or without `-d .` in case of issues:

```bash
datalad install -s "https://github.com/holoviz/holoviews/tree/main" tutorials/holoviews
```

---

## Step 2: Open the first notebook

In your VSCode file explorer, navigate to the folder:
```bash
NeuroPySeminar/tutorials/holoviews/examples/getting_started
```

Or simply run the following in your terminal:
```bash
code tutorials/holoviews/examples/getting_started/1-Introduction.ipynb
```

---

There are 5 notebooks in this folder. Open the first one:
```bash
1-Introduction.ipynb   
2-Customization.ipynb  
3-Tabular_Datasets.ipynb  
4-Gridded_Datasets.ipynb
5-Live_Data.ipynb
```

---


