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

## **A. BIDS – Standardized Data Organization**

### 🎯 **Goal**

Learn about BIDS and immediately apply it by BIDS-ifying a dataset.

---

### 🧠 **Theory**

- Introduce the **BIDS standard**: motivation, structure, metadata files.
    
- Explain key elements:
    
    - `sub-*/ses-*` hierarchy
        
    - `dataset_description.json`
        
    - sidecar JSONs
        
    - modality-specific folders (`anat`, `func`, `dwi`, etc.)
        
- Emphasize reproducibility and compatibility with open neuroimaging tools.
    

---

### 💻 **Practice**

- Each participant:
    
    - Uses **their own dataset** or a **provided demo dataset**.
        
    - Converts it into **BIDS format**:
        
        - Create folder structure and minimal JSON sidecars.
            
        - Validate using a **BIDS Validator**.
            
    - Add metadata fields such as `TaskName`, `Manufacturer`, etc.
        

**Note:** Talk through motivation; show folder tree; link to validator.

---

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

- Download a small sample dataset (or use an OpenNeuro example).
    
- Organize it into BIDS format (`sub-01/anat/...`).
    
- Run the **BIDS Validator**: [https://bids-standard.github.io/bids-validator/](https://bids-standard.github.io/bids-validator/)
    
- Fix any filename or metadata issues you encounter.
    

🕐 _Take 10 minutes to complete these steps._

---

## **B. DataLad – Version Control for Data and Collaboration**

### 🎯 **Goal**

Learn how to use DataLad to manage datasets, track changes, and share data under the shared lab repository.

---

### 🧠 **Theory**

- Introduce **DataLad concepts**:
    
    - Git + git-annex integration
        
    - **datasets**, **subdatasets**, **remote storage (RIAs)**
        
    - Provenance tracking and reproducibility
        
- Discuss **collaborative structure** of the **lab repository (`slab`)**.
    

---

### 💻 **Practice**

1. **Clone the lab repository**
    

```bash
datalad clone git@server:/path/to/slab
```

---

2. **Add your dataset** as a **subdataset**:
    

```bash
datalad create -d . my_dataset
datalad save -m "added dataset"
```

---

3. **Push your subdataset**:
    

- Option A: use your **own RIA store** on the lab server (local filesystem)
    
- Option B: push directly to the **lab RIA store** (shared bare repo)
    

```bash
datalad push --to origin
```

---

4. **Annotate with metadata** (from BIDS practice)
    

```bash
datalad metadata --set <key>=<value>
datalad save -m "added metadata"
```

---

5. **Sync and verify** updates:
    

```bash
datalad update --merge
```

Everyone can now see that multiple subdatasets have been added by others.

---

**🎁 Bonus:**  
Use DataLad to fetch a paper from the shared **lab paperpool**:

```bash
datalad get slab/papers/example.pdf
```

---

**Concept Recap Commands**

```bash
datalad create my_dataset
echo "hello" > my_dataset/hello.txt
datalad save -m "add hello"
# explain: datalad create, save, get, push
```

---

### Add as subdataset & push (alt minimal example)

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
    
- (If access) clone `slab` and add a subdataset on a **feature branch**.
    

🕐 _5 minutes — experiment and share one useful command!_

---

## **C. Snakemake – Workflow Management and Automation**

### 🎯 **Goal**

Learn how to define and execute reproducible pipelines operating on BIDS datasets.

---

### 🧠 **Theory**

- What is a **Snakefile**?
    
- Rules, inputs, outputs, and wildcards.
    
- Workflow visualization (DAGs) and reports.
    
- Integration with version control and DataLad.
    

---

### 💻 **Practice**

1. Create a **Snakefile** that includes:
    
    - One **MATLAB script** (dummy computation).
        
    - Two **Python scripts**:
        
        - `calc.py` → performs a dummy computation.
            
        - `plot.py` → generates a PNG output.
            

---

2. Define outputs under `derivatives/`:
    

```
derivatives/
├── dummy-mat/
├── dummy-py/
└── dummy-png/
```

---

3. Execute the pipeline:
    

```bash
snakemake --cores 2
```

---

4. Visualize workflow:
    

```bash
snakemake --dag | dot -Tpng > dag.png
```

---

5. **Bonus:** Generate a Snakemake report:
    

```bash
snakemake --report report.html
```

---

**Minimal Example Snakefile**

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

---

## 🧩 Your Turn — Snakemake

> 💡 **Hands-on Practice**

- Copy or create the sample `Snakefile`.
    
- Run the workflow:
    
    ```bash
    snakemake --cores 2
    ```
    
- Add a **new rule** that writes today’s date to a file.
    
- Generate a **DAG image** and open the `report.html`.
    

🕐 _10 minutes — make your workflow produce something new!_

---

## **D. Integration, FAIR Principles & Sustainability**

### 🎯 **Goal**

Combine all tools under FAIR principles — make workflows reproducible, adaptable, and transparent.

---

### 🧠 **Theory**

- Summarize:
    
    - **Reproducibility** – “same results anytime.”
        
    - **Adaptability** – modular pipelines and reusable code.
        
    - **Transparency** – open sharing and provenance tracking.
        
- Reference: _Snakemake “Rolling Paper”_ (FAIR workflow concepts).
    

---

### 💻 **Practice**

1. **Make your Snakemake pipeline a CLI tool**:
    
    - Add a `code/` folder.
        
    - Move Snakefile and scripts inside.
        
    - Create a `pyproject.toml` with an **entry point** to run from command line.
        
    - Install into environment (`conda activate labpy`).
        

```bash
pip install -e .
```

---

2. **Run the workflow with provenance tracking**:
    

```bash
datalad run "snakemake --cores 2"
```

---

3. **Save and push results**:
    

```bash
datalad save -m "run workflow with provenance"
datalad push
```

---

4. **Promote your package** into a **DataLad subdataset**:
    

```bash
datalad create -d slab/packages mytool
datalad save -m "added CLI tool package"
```

---

5. **Write documentation** for your tool under `docs/` (can later integrate with MkDocs).
    

---

6. **Push to shared RIA store**:
    

```bash
datalad push --to ria-storage
```

---

7. Perform all steps on a **feature branch** to protect the main `slab` repository.
    

---

**🎁 Bonus:**

- Inspect your Snakemake log (`snakemake.log` or `.snakemake/log/`).
    
- Email the generated HTML report to **Anton Sirota** directly from the terminal (attach the file or convert to PDF first).
    

---

## 🧩 Your Turn — Integration

> 💡 **Hands-on Practice**

- Clone or create a DataLad dataset.
    
- Add your `Snakefile` to the project (ideally under `code/`).
    
- Run your workflow with provenance tracking:
    
    ```bash
    datalad run "snakemake --cores 2"
    ```
    
- View recorded provenance:
    
    ```bash
    datalad run-record show
    ```
    
- Create a **feature branch**, add a brief `README.md`, and push to the **RIA store**.
    

🕐 _5–10 minutes — confirm your provenance record works._

---

## FAIR Checklist

- **Findable**: DOI / registered repository
    
- **Accessible**: DataLad + open protocols
    
- **Interoperable**: BIDS format
    
- **Reusable**: Metadata + provenance (Snakemake + DataLad)
    

---

## 🧾 Summary Workflow Overview

1. **BIDSify** → make your dataset structured.
    
2. **DataLad** → track and share it reproducibly.
    
3. **Snakemake** → define and execute workflows.
    
4. **Integrate + FAIR** → make it reusable, transparent, and versioned.
    

---

## ✅ End of Tutorial — Discussion & Q&A

- What worked smoothly?
    
- What would help you apply this to your own data?
    
- How can we support reproducibility in the lab’s shared workflows?