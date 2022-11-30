# DeFiNES: Enabling Fast Exploration of the Depth-first Scheduling Space for DNN Accelerators through Analytical Modeling - HPCA23 Artifact Evaluation

## Abstract
Our artifact provides a guide to replicate the primary
experiments (case study 1) demonstrated in this paper. Since
case study 2 and 3 are equivalently performing case study 1
multiple times (for different workload and HW architecture
combinations) and will take a long time to run and generate
multi-Gigabytes of data, we here focus on case study 1.


The included materials are the source code of DeFiNES and
the scripts to auto-run the experiments, collect data, and make
the plots. In the end, we also provide the useful information
on experiment customization, i.e. users can use DeFiNES to
carry out their own DNN accelerator-schedule design space
exploration, considering both layer-by-layer and depth-first
scheduling possibilities.

## Installation

1) Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) environment

2) Download DeFiNES (`git clone` this repo)

3) Use a terminal or an Anaconda Prompt for the following steps:
   -  `cd` into the DeFiNES repo
   -  Create the conda environment from the environment.yml file
       ```
       conda env create -f environment.yml
       ```
   -  Activate the new environment:
       ```
       conda activate DeFiNESenv
       ```

## Run

After the previous Installation is done, two steps are required to run the case study 1 and reproduce the overall
comparison result (Fig. 12) and the detailed analysis results (Fig. 13, Fig. 14, Fig. 15, Fig. 6(left), Fig. 9 and Fig. 10).

> Note that the below two steps need to run in sequence in the DeFiNES repo.

### Step 1 
Run
```
python main_artifact.py
```

#### What does this script do?
It applies 108 depth-first scheduling options (3 modes
with 6×6 X-Dim and Y-Dim tile size combinations) for
processing FSRCNN on Meta-proto-like DF architecture.

#### Runtime?
18 hours with the default setting (using 1 CPU thread
and set `loma_lpf_limit=8`). loma_lpf_limit is
a speed-quality tradeoff tuning knob. User can change
its value in [main_artifact.py](/main_artifact.py#L70). The larger it is, the
longer the program runs, and possibly the better the result
found. For all the experiments in the paper, we set it to
8 to guarantee the best results can be found.


For testing purpose, users can set `loma_lpf_limit=6`, the total runtime will be reduced dramatically from
18 hours to 45 minutes, while some design points’ best
found energy will increase by a few percents. So, the
figures plotted in this case will be slightly different than
the original ones in the paper.

#### What results are expected? 
When the program finishes, an overall energy and latency comparison figure will be plotted for these 108 depth-first scheduling options (Fig. 12), and 108 result pickle files (.pkl) will be saved under the `result_saving_path` defined in the [main_artifact.py](/main_artifact.py#L13) (by default, it is `.\result_pickle_files\`).


### Step 2
Run
```
python plot_artifact.py
```

#### What does this script do?
It extracts the required information from the generated
result pickle files and makes the plots.

#### Runtime?
1 minute

#### What results are expected? 
Multiple detailed analysis figures: Fig. 13, Fig. 14, Fig. 15, Fig. 6(left), Fig. 9 and Fig. 10.

> In the end, all the plots will be saved to `.\result_plot\` as PDF files.

## Experiment Customization
The goal of this work is to provide an open-source framework for DNN accelerator architecture-schedule optimization,
which allows users to plug in their own setting files and perform customized design space exploration experiments.
For this, users need to provide DeFiNES with the inputs listed in Fig. 5: a workload, a HW architecture, and some
depth-first scheduling parameters (in which the Fuse depth is set automatically by DeFiNES, thus no need to provide).

This work has [5 workloads](/inputs/WL) (inside of each folder) and [10 HW architectures](/inputs/HW) modelled for the case study 2 and 3. Users can perform
experiments on them, modify them to try new design options, or create own workloads and/or HW architectures following the same data formats in these example setting files. You can find more details on how to set the input files [here](https://zigzag-project.github.io/zigzag/user-guide.html).

Some example commands users can run (Use `python main.py --help` to see what each argument means):
```
python main.py --accelerator inputs.HW.Edge_TPU_like --workload inputs.WL.Edge_TPU_like.workload_mccnn --dfmode 1 --tilex 16 --tiley 8
python main.py --accelerator inputs.HW.Edge_TPU_like --workload inputs.WL.Edge_TPU_like.workload_mobilenetv1 --dfmode 1 --tilex 7 --tiley 7
python main.py --accelerator inputs.HW.Meta_prototype --workload inputs.WL.Meta_prototype.workload_fsrcnn --dfmode 123 --tilex 96 --tiley 72
```
The results are saved as pickle files (.pkl) in the pre-defined `result_saving_path`. User can use/modify the functions provided in [plot_artifact.py](/plot_artifact.py) and
[plot_helper_funcs.py](/plot_helper_funcs.py) to extract various data from the pickle files and visualize the results.

---
We are continually improving the framework, and welcoming all questions and feedback. 

We hope our tool can help other researchers to better explore and understand the vast DNN accelerator architecture-and-scheduling design space and can offer the best design solutions.







