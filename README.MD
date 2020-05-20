# Kmer Pathogen Identification Pipeline 

This GUI tool identifies which bacteria/virus, plasmids, and antibiotic resistance genes are contained in you NGS DNA sequences.
It uses [Mash Screen](https://mash.readthedocs.io/en/latest/tutorials.html) to identify the pathogens and plasmids.
KMA to identify which antibiotic resistance genes.
The overall goal is to use Kmer based alignment to quickly perform the above steps in less than 5-10 minutes per sample.

## Summary - Installation 
1. Clone Repository 
2. Install Conda if not already in environment
3. Create conda environment
4. Download Mash libraries.

## Summary - How to run after installation.
1. Activate conda environment - `conda activate KPIP`
2. Run the GUI - `~/KPIP/KPIP_GUI.py`

### Install git for Debian systems using the following command (if necessary)
```
sudo apt update
sudo apt install git
```

## Clone this code using GIT
```
git clone https://github.com/jiangweiyao/KPIP.git
```

## Install Miniconda (if no Conda is installed on system).
Detailed instruction on the the Miniconda website for installing and configuring Miniconda:
https://conda.io/projects/conda/en/latest/user-guide/install/linux.html

You can run the prepackaged script `install_miniconda.sh` in the repository to install into your home directory (recommended) by using the following command assuming SanitizeMe is downloaded into your home directory:
```
. ~/KPIP/install_miniconda.sh
```

### Build the environment. Need to do once.

We use conda to create an environment (that we can activate and deactivate) to install our dependent software and resolve their dependencies. This environment is called "KPIP". 

```
conda create -n KPIP python=3 gooey tabulate pandas mash kma -y
```

The command to generate the environment is in the included `conda_env.txt` file. 

## Run the code.

Activating your environment makes the software you installed in that environment available for use. You will see "(KPIP)" in front bash after activation.
```
conda activate KPIP
```
Run the code (change path if it is installed else where.)
```
~/KPIP/KPIP_GUI.py
```

When you are finished running the workflow, exit out of your environment by running `conda deactivate`. Deactivating your environment exits out of your current environment and protects it from being modified by other programs. You can build as many environments as you want and enter and exit out of them. Each environment is separate from each other to prevent version or dependency clashes. The author recommands using Conda/Bioconda to manage your dependencies.

## Author
- Jiangwei Yao

## License 
Apache License 2.0

