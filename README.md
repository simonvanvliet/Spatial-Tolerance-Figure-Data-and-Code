# Figure Source Data and Code

Figure source data and code accompanying the paper: Opposing Range-Dependent Interactions Create Complex Spatial Patterns of Antibiotic Tolerance in Multispecies Biofilms

Code and analysis by Giulia Bottacin and Simon van Vliet.

## Overview

Data and analysis code organized by figure and panel. Two types of workflows:

### Image Analysis Panels

```
panel_name/
├── analysis_code/     # Processed images → CSV data
└── figure_code/        # CSV data → PDF figures
```

The analysis_code subfolder contains notebooks used to process segmented images to create processed data files. Code is provided for reference only, running it requires access to raw data files. Output of scripts is stored in figure_code subfolder.

The figure_code contains processed data files (Figure source data) and code needed to replicate figures.

### Direct Data Plotting

```
panel_name/
├── data.xlsx          # Experimental data
└── notebook.ipynb     # Data → PDF figure
```

Contains data files (Figure source data) and code needed to replicate figures.

## Related Content

Code for figures 3 and 4 can be found on: [github.com/simonvanvliet/SpatialToleranceModel](https://github.com/simonvanvliet/SpatialToleranceModel).
