# Figure Source Data and Code

Figure source data and code accompanying the paper: 

Model accompanying the paper:

Opposing range-dependent interactions create complex spatial patterns of antibiotic tolerance in multispecies biofilms.
Bottacin G, Raach B, Fröhlich L, Künnecke J, Kaczmarczyk A, Tejada-Arranz A, Ugolini GS, Stocker R, Jenal U, Bumann D, Dittrich PS, Schubert OT, van Vliet S. PNAS (2026)

Code and analysis by Giulia Bottacin and Simon van Vliet.

## Related resources

- Preprint: [bioRxiv](https://doi.org/10.64898/2026.02.04.703747)
- A complementary repository with code of model and parameter inference is available [GitHub](https://github.com/simonvanvliet/SpatialToleranceModel)
- Raw data is available on BioImageArchive.

## Installation

To set up the required Python environment, use the provided `environment.yml` file with conda:

```bash
conda env create -f environment.yml
```

This will create a new conda environment named `spatial_tolerance_env` with all required dependencies.

To activate the environment:

```bash
conda activate spatial_tolerance_env
```

## Overview

Repository contains all figure source data files and Jupyter notebooks needed to reproduce figures from paper. In addition, all analysis code is provided to re-process output of image segmentation pipeline to recreate figure source data files. Rerunning this analysis requires access to raw data as provided on BioImageArchive

Data and analysis code organized into subfolders by figure and panel. There are two types of workflows:

### Image Analysis Panels

```
panel_name/
├── analysis_code/     # Processed images → CSV data
└── figure_code/        # CSV data → PDF figures
```

The analysis_code subfolder contains notebooks used to process segmented images to create processed data files. Code is provided for reference only, running it requires downloading the raw data files from the BioImageArchive. Output of scripts is stored in figure_code subfolder.

The figure_code contains processed data files (Figure source data) and code needed to replicate figures, these can be run without downloading additional data

Minimal code is provided to reproduce figures containing model predictions and parameter inferences, for the full code is available on a [second GitHub repository](https://github.com/simonvanvliet/SpatialToleranceModel)

### Direct Data Plotting

```
panel_name/
├── data.xlsx          # Experimental data
└── notebook.ipynb     # Data → PDF figure
```

Contains data files (Figure source data) and code needed to replicate figures.