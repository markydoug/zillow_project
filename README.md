# Zillow Project
## A look at predicting home values

## Project Description
The housing market is hard to predict, but through data analysis and machine learning models we can make predictions on what a house value might be based on different features of the house. Through this project I will explore the Zillow data for 2017 single-family properties, determine what features are effective in predicting house prices, and create a predictive model for these type of properties.

## Project Goals
* Identify key features that can be used to create an effective predictive model.
* Use regression models to make house price predictions.
* Use findings to make recommendations and establish a foundation for future work to improve model's performance.

## Initial Thoughts
My initial hypothesis is that .

## The Plan
* Aqcuire the data from Codeup mySQL database

### Prepare data
#### Dropped rows:
* Duplicates   
* Rows having 0 bedrooms AND 0 bathrooms 
* Rows having more than 10,000 square feet (because these are large and can scew the data)
* Rows containing null values in any column

#### Created features
* ```county``` (names based on the fips code):  
    - 6037: LA
    - 6059: Orange 
    - 6111: Ventura 
* ```bath_bed_ratio``` 
    - Column displaying bathrooms/bedrooms

#### Other prep
* Split data into train, validate, and test (65/20/15)

### Explore data in search of drivers of churn
    * Answer the following initial question
        * 
        * 

* Develop a model to predict the value of a house
    * 
    * 
    * 

* Draw conclusions

## Data dictionary
| Feature | Definition | Type |
|:--------|:-----------|:-------
|**???**| Definition| *type*|
|**???**| Definition| *type*|
|**???**| Definition| *type*|
|**???**| Definition| *type*|
|**???**| Definition| *type*|
|**???**| Definition| *type*|
|**???**| Definition| *type*|
|**Target variable**
|**home_value**| Appraised home value | *float* |


## Steps to Reproduce
1. Clone this repo
2. Acquire the data from Codeup mySQL "telco" database using your personal ```env.py``` file where you store your ```username```, ```password```, and ```host```
3. Put the data in the file containing the cloned repo.
4. Run notebook.

## Takeaways and Conclusions
* 
* 

## Recommendations
* :
    * 
    * 
    * 

## Next Steps
* In the next iteration:
    * 
    * 