# Zillow Project
## A look at predicting home values

## Project Description
The housing market is hard to predict, but through data analysis and machine learning models we can make predictions on what a house value might be based on different features of the house. Through this project I will explore the Zillow data for 2017 single-family properties, determine what features are effective in predicting house prices, and create a predictive model for these type of properties.

## Project Goals
* Identify key features that can be used to create an effective predictive model.
* Use regression models to make house price predictions.
* Use findings to make recommendations and establish a foundation for future work to improve model's performance.

## Initial Thoughts & Questions
My initial hypothesis is that square feet and location are strong drivers of home value.
    1. Is there a significant relationship between square footage and home value?
    2. Is there a significant relationship between the bath-to-bed ratio and home value? 
    3. Does location have a relationship with home value?
    4. Is there a significant relationship between age of the home and home value?

## The Plan
### Aqcuire the data from Codeup mySQL database

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
    1. Is there a significant relationship between square footage and home value?
    2. Is there a significant relationship between the bath-to-bed ratio and home value? 
    3. Does location have a relationship with home value?
    4. Is there a significant relationship between age of the home and home value?

### Develop a model to predict the value of a house
* Use drivers identified through exploration to build different predictive models
* Evaluate models on train and validate data
* Select best model based on highest $r^2 score$
* Evaluate the best model on the test data

### Draw conclusions

## Data dictionary
| Feature | Definition | Type |
|:--------|:-----------|:-------
|**parcelid**| Definition| *int*|
| **bathroooms** | The number of bathrooms in the home. |*float*|
| **bedrooms** | The number of bedrooms in the home.|*int*|
|**square_feet**| Square footage of the house| *int*|
|**year_built**| Year the house was built| *int*|
|**bath_bed_ratio**| The number of bathrooms divided by number of bedrooms| *float*|
|**county**| Name of the county where the house is located| *string*|
|**2017_age**| Age of the house in 2017 (when the data was collected| *int*|
|**Target variable**
|**home_value**| The tax-assessed value of the home. | *float* |


## Steps to Reproduce
1. Clone this repo
2. Acquire the data from Codeup mySQL "zillow" database using your personal ```env.py``` file where you store your ```username```, ```password```, and ```host```
3. Put the data in the file containing the cloned repo.
4. Run notebook.

## Conclusion

### Summary
* ```square_feet``` seems to be a driver of home value
* ```bath_bed_ratio``` seems to be a driver of home value
* ```county``` seems to be a driver of home value
* ```2017_age``` seems to be a driver of home value


### Recommendations
* We should do more research of the areas where these houses are located to have a better understanding of how location is driving home value.
* Dive into our data and see what information has been corrupted and delete those rows so that we can make sure we are using as accurate data as we can.

### Next Steps
* In the next iteration:
    * Look into neighborhoods, and exact location of the houses to see if that will help the model perform better.
    * Look into other features of the house (garage, pool, deck, etc.) to see if they are also drivers of home value.