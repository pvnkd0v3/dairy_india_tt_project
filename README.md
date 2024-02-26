# Dairy India Tripleten Project
This repository contains the code and data for an exploratory data analysis project for Sprint 4 of TripleTen's Data Science course. This project is an analysis on dairy sales in India from 2019-2022 that seeks out to find any possible trends in the data's variables. Specifically, it is explored whether any possible trends are correlated with onset of the COVID-19 lockdowns as the time frame that the data spans encompasses them.

## Data
The data used in this project is dairy_dataset.csv and contains data on 4325 sales of dairy products across India from 2019-2022.

## Files
- dairy_dataset.csv: Dataset used in the project's analysis
- dairy_india.ipynb: Jupyter notebook containing the full analysis on the dataset
- app.py: Contains snippets of code from dairy.ipynb used to display data visualizations and project info in a Streamlit app
- .streamlit: contains a config.toml file that makes the Streamlit compatable with Render app hosting site
- requirements.txt: A file containing the project's required packages
- EDA_env.yml: file used to create the neccesary conda enviroment for the project

## Environment
To reproduce the project's analysis, create a conda environment using the EDA_env.yml file:
```bash
conda env create -f EDA_env.yml
conda activate EDA_env
```

## Usage
To run the dairy_india.ipynb notebook, enter the following command in the conda environment while in the project's directory:
```bash
jupyter notebook dairy_india.ipynb
```

To run the projects app.py app in Streamlit, enter the following command in the conda environment while in the project's directory:
```bash
streamlit run app.py
```
Render link: https://dairy-india-tt-project.onrender.com/

## Results
T-tests performed in dairy_india.ipynb yielded p-values much higher than the significance threshold of 0.5 when testing if these variables differed in the years 2019 (the year before before the COVID-19 lockdowns began) and 2020 (the year the lockdowns began) relative to the other years in the dataset:
- The volume of dairy sold
- The price of dairy sold per unit
- The total revenue from diary sales
- The volume of dairy reorded by customers

## Conclusion
Given the high p-values from each variable's t-tests, a solid correlation between dairy sales across India and the onset of the COVID-19 lockdowns cannot be made. In order to be sure this correlation does or doesn;t exist, however, additional data including a higher number of sales spanning across a longer time period surrounding the onset of th COVID-19 lockdowns would be needed.


