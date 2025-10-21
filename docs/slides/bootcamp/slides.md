# 🧩 Lab Reproducible Workflow Tutorial

_(BIDS → DataLad → Snakemake → Integration & FAIR)_  
Sirota Lab Meeting — Progressive, reproducible-workflow bootcamp

---

## Why Reproducible Workflows?

- Increasing complexity of neuroimaging analysis
    
- Challenges: sharing, version drift, reruns
    
- Solution: FAIR + modular workflow
    
    - **BIDS**: structure
        
    - **DataLad**: control
        
    - **Snakemake**: automation
        
    - **Integration**: provenance & sharing
        

---

## A. BIDS — Standardized Data Organization

**Goal:** Learn BIDS & immediately apply it.

**Theory**

- Why BIDS; structure & metadata
    
- `sub-*/ses-*`, `dataset_description.json`, sidecars
    

**Practice**

- Convert example dataset to BIDS
    
- Validate with BIDS Validator
    
- Add metadata (`TaskName`, `Manufacturer`, …)
    

Note:  
Talk through motivation; show folder tree; link to validator.

--

### BIDS Folder Skeleton

```text
project/
└─ sub-01/
   └─ anat/
      ├─ sub-01_T1w.nii.gz
      └─ sub-01_T1w.json
dataset_description.json
```

---

## 🧩 Your Turn — BIDS

> 💡 **Hands-on Practice**

- Download a small sample dataset (or use OpenNeuro example).
    
- Organize it into BIDS format (`sub-01/anat/...`).
    
- Run the [BIDS Validator](https://bids-standard.github.io/bids-validator/).
    
- Fix any filename or metadata issues you encounter.
    

🕐 _Take 10 minutes to complete these steps._

---

## B. DataLad — Version Control for Data

**Goal:** manage, track, share datasets.

**Concepts**

- Git + git-annex, datasets, subdatasets, RIA, provenance
    

**Practice**

```bash
datalad create my_dataset
echo "hello" > my_dataset/hello.txt
datalad save -m "add hello"
```

Note:  
Explain `datalad create`, `save`, `get`, `push`.

--

### Add as subdataset & push

```bash
datalad create -d . my_dataset
datalad save -m "added dataset"
datalad push --to origin
```

---

## 🧩 Your Turn — DataLad

> 💡 **Hands-on Practice**

- Run `datalad create test_ds`.
    
- Add and save a small file (`echo "test" > file.txt`).
    
- Explore commands:
    
    - `datalad status`
        
    - `datalad get`
        
    - `datalad push`
        
- Inspect `.git/annex` to see how large files are tracked.
    

🕐 _5 minutes — experiment and share one useful command!_

---

## C. Snakemake — Reproducible Pipelines

**Goal:** define & run pipelines on BIDS data.

**Practice**

```python
# Snakefile
rule all:
    input: "derivatives/dummy-png/out.png"

rule calc:
    output: "derivatives/dummy-py/out.txt"
    shell: "python code/calc.py > {output}"

rule plot:
    input: "derivatives/dummy-py/out.txt"
    output: "derivatives/dummy-png/out.png"
    shell: "python code/plot.py {input} {output}"
```

Note:  
Then run `snakemake --cores 2`; show DAG & report.

--

### Visualize & Report

```bash
snakemake --dag | dot -Tpng > dag.png
snakemake --report report.html
```

---

## 🧩 Your Turn — Snakemake

> 💡 **Hands-on Practice**

- Copy or create the sample `Snakefile`.
    
- Run the workflow:
    
    ```bash
    snakemake --cores 2
    ```
    
- Add a new rule that writes today’s date to a file.
    
- Generate a DAG image and open the `report.html`.
    

🕐 _10 minutes — make your workflow produce something new!_

---

## D. Integration & FAIR

- Reproducibility • Adaptability • Transparency
    
- Package the pipeline; run with provenance
    

```bash
datalad run "snakemake --cores 2"
datalad save -m "run workflow with provenance"
datalad push
```

---

## 🧩 Your Turn — Integration

> 💡 **Hands-on Practice**

- Clone or create a DataLad dataset.
    
- Add your `Snakefile` to the project.
    
- Run your workflow with provenance tracking:
    
    ```bash
    datalad run "snakemake --cores 2"
    ```
    
- View recorded provenance:
    
    ```bash
    datalad run-record show
    ```
    

🕐 _5–10 minutes — confirm your provenance record works._

---

### FAIR Checklist

- **Findable**: DOI / registered repository
    
- **Accessible**: DataLad + open protocols
    
- **Interoperable**: BIDS format
    
- **Reusable**: Metadata + provenance (Snakemake + DataLad)
    

---

✅ _End of Tutorial — Discussion & Q&A_

- What worked smoothly?
    
- What would help you apply this to your own data?
    
- How can we support reproducibility in the lab’s shared workflows?
    

---
