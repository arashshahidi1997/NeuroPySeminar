> [!steps]
> 1. clone the sirocampus (skip)
> 2. define a project (project template cookiecutter - put templates under sirocampus/code/templates) (skip)
> 3. install (ephemeral) a dataset (the ds-bidsmini) as raw (let's prepare bidsmini)
> 4. make a new derivative subdataset (literal and cogpy cli tool)
> 5. make a Snakefile under workflow (add given rules)
> 	- single file rule
> 	- snakemake run
> 	- look at the log
> 	- datalad save -m "single file"
> 	- multifile rule and equivalent snakebids rule
> 	- datalad run 
> 	- datalad update bidsmini (new subject is added)
> 	- datalad rerun
> 6. snake report
> 7. history command > chatgpt/copilot summarize > tutorialcmds
> 8. make a markdown under docs/tutorial of sirocampus > add tutorial
> 9. write a tutorial-methods.md with citing @ zotero in vscode, for the multitaper method
> 10. add your scripts under labpy and push


1. setup
open vscode
ctrl shfit p

```bash
ssh beta
```

1. clone the sirocampus
	```bash
	datalad install -
	```
2. define a project (project template cookiecutter - put templates under sirocampus/code/templates)
3. install (ephemeral) a dataset (the ds-bidsmini) as raw
4. make a new derivative subdataset (literal and cogpy cli tool)
5. make a Snakefile under workflow (add given rules)
	- single file rule
	- snakemake run
	- look at the log
	- datalad save -m "single file"
	- multifile rule and equivalent snakebids rule
	- datalad run 
	- datalad update bidsmini (new subject is added)
	- datalad rerun
6. snake report
7. history command > chatgpt/copilot summarize > tutorialcmds
8. make a markdown under docs/tutorial of sirocampus > add tutorial
9. write a tutorial-methods.md with citing @ zotero in vscode, for the multitaper method
10. add your scripts under labpy and push

# Snakemake tutorial
important points to be demonstrated:
- shell rule
- rule single file
- config file
- matlab rule
- scaling: rule wildcards
- scaling: snakebids

Bonus:
- plot rule
- rst captions
- snake report

to be effective we can try this in the context of one matlab function of the lab. For instance spectrogram.

# Sirocampus

```bash
sirocampus (the sirotalab super repository)
├── bib (lab paper pool > linked with Zotero)
├── data (datalad superdataset containing all sirota lab datasets)
│   ├── ds-msol
│   ├── ds-gecog
│   ├── ds-pixecog
│   └── ... To be added by you 🎨! 
├── docs (lab documents based on Diataxis framework)
│   ├── logs
│   ├── how-to
│   ├── reference
│   ├── tutorials
│   └── explanation
└── code (sirota lab code)
    ├── lib (library of third-party tools)
    ├── cogpy (ecog package)
    ├── labbox (lab MATLAB toolbox)
    └── labpy (lab Python package)
```

explanation (cognition) > tutorial (action)
docs -> Diataxis

> [!prep]-
> 