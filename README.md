# AgriTech-USGS-LIDAR

## About the project
- This project aims to allow you retrieve visualize USGS 3DEP lidar point cloud data.
## Overview 

We work at an AgriTech, which has a mix of domain experts, data scientists, data engineers. As part of the data engineering team, We are tasked to produce an easy to use, reliable and well designed python module that domain experts and data scientists can use to fetch, visualise, and transform publicly available satellite and LIDAR data. In particular, our code should interface with USGS 3DEP and fetch data using their API. 

## Steps 
- Data Fetching and Loading: From [USGS 3DEP](https://registry.opendata.aws/usgs-lidar/). Our task is to write a modular python code/package to connect to the API, query the data model to select with  a specified input and get a desired output
- Terrain Visualization: To include an option to graphically display the returned elevation files as either a 3D render plot or as a heatmap. The following is an example visualisation.
- Data Transformation

## Structure 
- Script: Where python scripts will be found which will include scripts for data fitching, visualization and others.
- Notebook: Where we will explore using using the python files inside script folder

## Built with 
- PDal
- Shapely
- Geopandas
- Matplotlib

## Prerequisites
These are the prerequistites that users need beforehand to install and use this code

- PDAL
- geopandas
- numpy
- pandas
- Shapely

### Contact 
dbulom12@gmail.com

 



