# 🧩 Lab Reproducible Workflow Tutorial

_(BIDS → DataLad → Snakemake → Integration & FAIR)_

---

## **A. BIDS – Standardized Data Organization**

### 🎯 **Goal**

Learn about BIDS and immediately apply it by BIDS-ifying a dataset.

### 🧠 **Theory**

- Introduce the **BIDS standard**: motivation, structure, metadata files.
    
- Explain key elements:
    
    - `sub-*/ses-*` hierarchy
        
    - `dataset_description.json`
        
    - sidecar JSONs
        
    - modality-specific folders (anat, func, etc.)
        
- Emphasize reproducibility and compatibility with open neuroimaging tools.
    

### 💻 **Practice**

- Each participant:
    
    - Uses **their own dataset** or a **provided demo dataset**.
        
    - Converts it into **BIDS format**:
        
        - Create folder structure and minimal JSON sidecars.
            
        - Validate using a **BIDS Validator**.
            
    - Add metadata fields such as `TaskName`, `Manufacturer`, etc.
        

---

## **B. DataLad – Version Control for Data and Collaboration**

### 🎯 **Goal**

Learn how to use DataLad to manage datasets, track changes, and share data under the shared lab repository.

### 🧠 **Theory**

- Introduce **DataLad concepts**:
    
    - Git + git-annex integration
        
    - **datasets**, **subdatasets**, **remote storage (RIAs)**
        
    - Provenance tracking and reproducibility
        
- Discuss **collaborative structure** of the **lab repository (`slab`)**.
    

### 💻 **Practice**

1. **Clone the lab repository**
    
    ```bash
    datalad clone git@server:/path/to/slab
    ```
    
2. **Add your dataset** as a **subdataset**:
    
    ```bash
    datalad create -d . my_dataset
    datalad save -m "added dataset"
    ```
    
3. **Push your subdataset**:
    
    - Option A: use your **own RIA store** on the lab server (local filesystem)
        
    - Option B: push directly to the **lab RIA store** (shared bare repo)
        
    
    ```bash
    datalad push --to origin
    ```
    
4. **Annotate with metadata** (from BIDS practice)
    
    ```bash
    datalad metadata --set <key>=<value>
    datalad save -m "added metadata"
    ```
    
5. **Sync and verify** updates:
    
    ```bash
    datalad update --merge
    ```
    
    Everyone can now see that multiple subdatasets have been added by others.
    

**🎁 Bonus:**  
Use DataLad to fetch a paper from the shared **lab paperpool**:

```bash
datalad get slab/papers/example.pdf
```

---

## **C. Snakemake – Workflow Management and Automation**

### 🎯 **Goal**

Learn how to define and execute reproducible pipelines operating on BIDS datasets.

### 🧠 **Theory**

- What is a **Snakefile**?
    
- Rules, inputs, outputs, and wildcards.
    
- Workflow visualization (DAGs) and reports.
    
- Integration with version control and DataLad.
    

### 💻 **Practice**

1. Create a **Snakefile** that includes:
    
    - One **MATLAB script** (dummy computation).
        
    - Two **Python scripts**:
        
        - `calc.py` → performs a dummy computation.
            
        - `plot.py` → generates a PNG output.
            
2. Define outputs under `derivatives/`:
    
    ```
    derivatives/
    ├── dummy-mat/
    ├── dummy-py/
    └── dummy-png/
    ```
    
3. Execute the pipeline:
    
    ```bash
    snakemake --cores 2
    ```
    
4. Visualize workflow:
    
    ```bash
    snakemake --dag | dot -Tpng > dag.png
    ```
    
5. **Bonus:** Generate a Snakemake report:
    
    ```bash
    snakemake --report report.html
    ```
    

---

## **D. Integration, FAIR Principles & Sustainability**

### 🎯 **Goal**

Combine all tools under FAIR principles — make workflows reproducible, adaptable, and transparent.

### 🧠 **Theory**

- Summarize:
    
    - **Reproducibility** – “same results anytime.”
        
    - **Adaptability** – modular pipelines and reusable code.
        
    - **Transparency** – open sharing and provenance tracking.
        
- Reference: _Snakemake “Rolling Paper”_ (FAIR workflow concepts).
    

### 💻 **Practice**

1. **Make your Snakemake pipeline a CLI tool**:
    
    - Add a `code/` folder.
        
    - Move Snakefile and scripts inside.
        
    - Create a `pyproject.toml` with an **entry point** to run from command line.
        
    - Install into environment (`conda activate labpy`).
        
    
    ```bash
    pip install -e .
    ```
    
2. **Run the workflow with provenance tracking**:
    
    ```bash
    datalad run "snakemake --cores 2"
    ```
    
3. **Save and push results**:
    
    ```bash
    datalad save -m "run workflow with provenance"
    datalad push
    ```
    
4. **Promote your package** into a **DataLad subdataset**:
    
    ```bash
    datalad create -d slab/packages mytool
    datalad save -m "added CLI tool package"
    ```
    
5. **Write documentation** for your tool under `docs/` (can later integrate with MkDocs).
    
6. **Push to shared RIA store**:
    
    ```bash
    datalad push --to ria-storage
    ```
    
7. Perform all steps on a **feature branch** to protect the main `slab` repository.
    

**🎁 Bonus:**

- Inspect your Snakemake log (`snakemake.log` or `.snakemake/log/`).
    
- Email the generated HTML report to **Anton Sirota** directly from the terminal.  
    _(Yes, emailing an HTML file is possible; just ensure it’s attached or converted to PDF before sending.)_
    

---

## 🧾 Summary Workflow Overview

1. **BIDSify** → make your dataset structured.
    
2. **DataLad** → track and share it reproducibly.
    
3. **Snakemake** → define and execute workflows.
    
4. **Integrate + FAIR** → make it reusable, transparent, and versioned.
    

