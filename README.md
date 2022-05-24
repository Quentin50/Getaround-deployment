# Project with Jedha

### Links
## Presentation video
Recording... 
## Dashboard
[GetAround Dashboard](https://getaround-dashboard-qg2022.herokuapp.com/)

I am using the free Heroku version so allow up to one minute to get the first response if the API is sleeping. Furthermore, I won't support it in the future so it may not be working anymore after December 2022.


### Objective
GetAround is a company that allows car owners to rent their cars to customers. Sometimes a customer might be late to checkout and the next customer might have to wait to checkin. It leads to cancellations, have a negative impact on the company revenues and image. The goal of this project is to be able to anticipate late checkouts, and evaluate the impact of some measures on car owners revenues. 

The technical goal of this project is to deploy multiple tools related to data science:
- a web dashbord acessible anywhere
- an web API exposing a machine learning prediction route
- a web MLFlow server to exchange with peer data scientists

## Dataset
* [Delay Analysis](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx) 👈 Data Analysis 
* [Pricing Optimization](https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv) 👈 Machine Learning: place it in api/data

## Prerequisites


### Dependencies
- The source code is written in Python 3.
- Docker is necessary to build and run localy the docker images
- Heroku CLI is necessary to upload images to Heroku 

## Usage
### Dashboard
Build the docker image with build.bat (easiy adaptable for linux if needed).
Run the docker image localy with run.bat or upload it to heroku with heroku CLI.

### API

### MLFlow

## Team contributors
Quentin Gottafray

## References

