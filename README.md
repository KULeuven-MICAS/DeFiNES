# DeFiNES - HPCA23 Artifact Evaluation
DeFiNES: Enabling Fast Exploration of the Depth-first Scheduling Space for DNN Accelerators through Analytical Modeling

In this artifact submission, we provide a guide to replicate the primary
experiments (case study 1) demonstrated in the paper. The
materials include the source codes of DeFiNES and
scripts to auto-run the experiments, collect data, and make
the plots. In the end, we also provide the useful information
on experiment customization, i.e. users can use DeFiNES to
carry out their own DNN accelerator-mapping design space
exploration, considering both layer-by-layer and depth-first
scheduling possibilities.

## Environment

We recommend setting up an anaconda environment.

Use the terminal or an Anaconda Prompt for the following steps:

Create the environment from the environment.yml file:

    conda env create -f environment.yml

The first line of the yml file sets the new environment's name (DeFiNESenv).

Then, activate the new environment:
    
    conda activate DeFiNESenv


## Run

Firstly, 

    python main_artifact.py

Secondly,

    python plot_artifact.py