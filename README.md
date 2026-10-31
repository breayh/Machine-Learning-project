# Machine-Learning-project
This repository contains an academic science project that evaluates machine learning models for predicting language endangerment from a defined risk tiers. Utilizing a cleaned dataset ($N = 2,635$) from 2010 of socio-economic and demographic indicators, the project compares a baseline Linear Regression model against a non-linear Random Forest Regressor to analyze global language preservation dynamics.

# Language Endangerment Prediction

Predicts global language endangerment tiers (0–4) from The Guardian article[2] using socio-economic and demographic indicators[3], such as number of speakers or GDP per capita.

## Overview
This project compares a baseline **Linear Regression** model against a non-linear **Random Forest Regressor** to analyze the factors influencing language endangerment. 

## Project Structure
- `report.pdf` - Full academic report document.
- `ML project/data.ipynb` - Data preprocessing, modeling, and evaluation script.

All **data** has been collected from sources:
- **[1] Kaggle:** [Extinct Languages Dataset](https://www.kaggle.com/datasets/the-guardian/extinct-languages/data)
- **[2] The Guardian:** [Endangered languages: the full list](https://www.theguardian.com/news/datablog/2011/apr/15/language-extinct-endangered#data)
- **[3] World Bank:** [World Development Indicators](https://databank.worldbank.org/source/world-development-indicators)
- **[4] PyPI:** [wbgapi Python Package](https://pypi.org/project/wbgapi/)
