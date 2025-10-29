--- 
title: "Bootcamp II — Progressive, Reproducible Workflow"
author: "Arash Shahidi"
theme: "black"
width: 1280 
height: 720 
---

# 🧩 Lab Reproducible Workflow Tutorial

_(BIDS → DataLad → Snakemake → Integration & FAIR)_  
Sirota Lab Meeting — Progressive, reproducible-workflow bootcamp


---


### 🧰 **Setup Conda (Shared vs Personal)**

#### 🟢 **If you already have your own Conda (If not > next slide)**

Don’t re-initialize — just temporarily source the shared one when you need it:

```bash
# Use the shared Conda installation for this session

source /storage/share/python/environments/Anaconda3/etc/profile.d/conda.sh

conda activate cogpy
```

💡 This doesn’t overwrite your personal Conda.

To return to your own environment, just:

```bash
source ~/.bashrc
```

(or however you normally load your personal Conda).


---

#### ⚙️ **If you don’t have Conda at all**

Initialize your shell using the shared Conda:

```bash

/storage/share/python/environments/Anaconda3/bin/conda init bash

source ~/.bashrc

```

> This will set up Conda automatically every time you open a new shell.

---

**Summary:**

* ✅ Existing Conda users → just `source` the shared `conda.sh` when needed.

* 🆕 No Conda yet → `conda init` with the shared installation once.

**Next**:

clone the BIDS project scaffold:
```
cookiecutter /storage2/arash/codes/Tools/cookiecutter/cookiecutter-bids-extended
```

---

cookicutter output
```bash
Copy code
? project_slug [tutorial-bids]: myproj
Output:

arduino
Copy code
myproj/
├── raw/
├── sourcedata/
├── derivatives/
├── code/
├── docs/
├── logs/
├── workflow/
│   ├── scripts/
│   │   ├── python-script.py
│   │   └── matlab-script.m
│   ├── notebooks/
│   ├── report/
│   └── Snakefile
├── config/
│   └── config.yaml
├── results/
├── dataset_description.json
└── README.md
```

---

## **A. BIDS – Standardized Data Organization**

### 🎯 **Goal**

Learn about BIDS and immediately apply it by BIDS-ifying a dataset.

| Title                                       | Speaker  | Year | Occasion                                                                | Location | Video                                                      | Slides                        |
| ------------------------------------------- | -------- | ---- | ----------------------------------------------------------------------- | -------- | ---------------------------------------------------------- | ----------------------------- |
| BIDS: underlying data management principles | Remi Gau | 2022 | Open Research at the Wellcome Center for Integrative Neuroimaging (WIN) | Online   | [link](https://vimeo.com/showcase/7645853/video/668642973) | [link](https://osf.io/h6gsr/) |

[BEP 032: Microelectrode electrophysiology](https://bids.neuroimaging.io/extensions/beps/bep_032.html#bep-032-microelectrode-electrophysiology)

---

###   **Theory**

- Introduce the **BIDS standard**: motivation, structure, metadata files.
    
- Explain key elements:
    
    - `sub-*/ses-*` hierarchy
        
    - `dataset_description.json`
        
    - sidecar JSONs
        
    - modality-specific folders (`ecephys`, `motion`, `anat`, `ieeg`, etc.)
        
- Emphasize reproducibility and compatibility with open neuroimaging tools.
    

---

### 💻 **Practice**

- Each participant:
    
    - Uses **their own dataset** or a **provided demo dataset**.
        
    - Converts it into **BIDS format**:
        
        - Create folder structure and minimal JSON sidecars.

---

### BIDS Folder Skeleton

```text
project/
└─ sub-01/
   └─ ses-01/
      ├─ motion/
      └─ ecephys/
        ├─ sub-01_ses-01_ecephys.lfp
        └─ sub-01_ses-01_ecephys.json
        
dataset_description.json
```

---

## **B. DataLad – Version Control for Data and Collaboration**

### 🎯 **Goal**

Learn how to use DataLad to manage datasets, track changes, and share data under the shared lab repository.


---

###   **Theory**

- Introduce **DataLad concepts**:
    
    - Git + git-annex integration
        
    - **datasets**, **subdatasets**, **remote storage (RIAs)**
        
    - Provenance tracking and reproducibility
        
- Discuss **collaborative structure** of the **lab repository (`slab`)**.
    

---

### 🧩 Your Turn

1. **Add your dataset** as a **subdataset**:

```bash
# Initialize superdataset with text2git configuration
datalad create -c text2git -f .

# Make 'raw' a subdataset (force, link to current dataset)
datalad create -d . --force raw

# Save subdataset registration
datalad save -m "Promote raw/ to subdataset"
```

---

> 💡 **Hands-on Practice**

- Download a small sample dataset (or use an OpenNeuro example).

```bash
 mkdir resources
 # datalad install -d . -s ///openneuro/<dataset_id> <shortname>
 datalad install -d . -s ///openneuro/ds004598 resources/ds-lfplintrack
```


---

3. **Verify structure**
```bash
datalad subdatasets
```
subdataset(ok): raw (dataset)
subdataset(ok): resources/ds-lfplintrack (dataset)

---

# OpenNeuro Datasets

| ID                                                                 | Species           | Modality                    | Type   | Notes                                                        |
| ------------------------------------------------------------------ | ----------------- | --------------------------- | ------ | ------------------------------------------------------------ |
| [ds003463](https://openneuro.org/datasets/ds003463/versions/1.0.2) | Mouse & Rat       | MRI (Mn-enhanced)           | Animal | In vivo MRI for 5×FAD mice and TgF344-AD rats.               |
| [ds003325](https://openneuro.org/datasets/ds003325/versions/1.0.0) | Mouse             | MRI (T1w)                   | Animal | TDP-43 knock-in mouse model of ALS-FTD.                      |
| [ds006746](https://openneuro.org/datasets/ds006746)                | Mouse             | MRI (Mn2+ enhanced)         | Animal | 3D RARE Mn(II)-enhanced MRI, 24 mice (2 rearing conditions). |
| [ds006670](https://openneuro.org/datasets/ds006670)                | Mouse             | MRI (T1w, T2w)              | Animal | Structural adulthood MRI in C57BL/6J mice.                   |
| [ds004913](https://openneuro.org/datasets/ds004913/versions/1.0.0) | Rat               | fMRI + Optogenetics         | Animal | Optogenetic DBS fMRI in Parkinsonian rats.                   |
| [ds005093](https://openneuro.org/datasets/ds005093/versions/1.0.0) | Non-human Primate | Imaging (PET/MRI)           | Animal | NHP study of microglia activation (TBS course).              |
| [ds000241](https://openneuro.org/datasets/ds000241/versions/00002) | Multiple species  | Imaging (various)           | Animal | “Animal Kingdom 6 Species” comparative dataset.              |
| [ds004161](https://openneuro.org/datasets/ds004161)                | Sheep             | MRI / Imaging               | Animal | Turone Sheep Chronic Stress (TSCS) study.                    |
| [ds004598](https://openneuro.org/datasets/ds004598/versions/1.0.0) | Rat               | LFP (electrophysiology)     | Animal | LFP during linear-track task in TgF344-AD rats.              |
| [ds006269](https://openneuro.org/datasets/ds006269)                | Rat               | EEG                         | Animal | 6-hour tethered EEG recordings in Syngap1 rats.              |
| [ds006366](https://openneuro.org/datasets/ds006366/versions/1.0.1) | Mouse             | EEG / Sleep                 | Animal | Mouse Sleep Staging Validation (EEG).                        |
| [ds005688](https://openneuro.org/datasets/ds005688)                | Animal            | Electrophysiology / Optical | Animal | visStim dataset – non-MRI animal neurophysiology.            |
| [ds004509](https://openneuro.org/datasets/ds004509/versions/1.0.0) | Rat               | Electrophysiology / Optical | Animal | Visual-deprivation remapping in rats (non-MRI).              |
| [ds005700](https://openneuro.org/datasets/ds005700/versions/1.0.0) | Human             | fMRI                        | Human  | NeuroEmo Emotion Recognition fMRI dataset (~7 GB BIDS).      |
| [ds005126](https://openneuro.org/datasets/ds005126/versions/1.0.0) | Human             | fMRI                        | Human  | ColorSimilarity fMRI study (~36 GB).                         |
| [ds005880](https://openneuro.org/datasets/ds005880/versions/1.0.2) | Human             | fMRI                        | Human  | “Diminished Seventh Chord” fMRI study.                       |
| [ds004517](https://openneuro.org/datasets/ds004517/versions/1.0.0) | Human             | EEG                         | Human  | EEG dataset for semantic decoding of imagined animals.       |
| [ds004514](https://openneuro.org/datasets/ds004514/versions/1.1.1) | Human             | EEG + fNIRS                 | Human  | Simultaneous EEG/fNIRS recordings.                           |

---

## 🧩 Your Turn — DataLad

> 💡 **Hands-on Practice**

- Run `datalad create test_ds`.
    
- Add and save a small file (`echo "test" > file.txt`).
    - `datalad status`    
    - `datalad save -m "<message>"`

    - `datalad get`
        
- Inspect `.git/annex` to see how large files are tracked.
    

🕐 _5 minutes — experiment and share one useful command!_

---

## **C. Snakemake – Workflow Management and Automation**

### 🎯 **Goal**

Learn how to define and execute reproducible pipelines operating on BIDS datasets.

Snakemake tutorial slides: https://slides.com/johanneskoester/snakemake-tutorial

---

###   **Theory**

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

###   **Theory**

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

## Why Reproducible Workflows?

- Increasing complexity of neuroimaging analysis
    
- Challenges: sharing, version drift, reruns
    
- Solution: FAIR + modular workflow
    
    - **BIDS**: structure
        
    - **DataLad**: control
        
    - **Snakemake**: automation
        
    - **Integration**: provenance & sharing

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
