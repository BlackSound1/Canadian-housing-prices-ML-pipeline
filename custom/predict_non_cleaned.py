if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

from utilities import date_numeric

@custom
def transform_custom(merged_df, *args, **kwargs):
    
    # Create data and target variables
    X = merged_df.drop(columns='Average price')
    y = merged_df['Average price']

    # Split TRAINING and TESTING data
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)

    # Split TRAINING and VALIDATION data
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, train_size=0.8)

    # Figure out what the best alpha value is from a given set
    param_grid = {'alpha' : [12, 15, 20, 25, 30]}
    ridge_model = Ridge(alpha=1)
    grid_search = GridSearchCV(ridge_model, param_grid)
    grid_search.fit(X_train, y_train)
    best_param = grid_search.best_params_

    # Train the Ridge model using this alpha value
    best_ridge_model = grid_search.best_estimator_
    best_ridge_model.fit(X_train, y_train)

    # Make predictions on the VALIDATION data
    ridge_predict = best_ridge_model.predict(X_val)
    rmse = round(mean_squared_error(y_val, ridge_predict, squared=False), 2)
    
    print(f"The Ridge model has an RMSE of: {rmse} with the VALIDATION data")

    # Make predictions on the TESTING data
    ridge_predict = best_ridge_model.predict(X_test)
    rmse = round(mean_squared_error(y_test, ridge_predict, squared=False), 2)

    print(f"The Ridge model has an RMSE of: {rmse} with the TESTING data")

    avg_of_Average_price = round(merged_df['Average price'].mean(), 2)

    print(f"Note that the average housing price is: {avg_of_Average_price}\n")

    # Check our non-cleaned predictions against actual known values for 2020, 2021, and 2022
    columns_ = ['Date', 'Real GDP Growth', 'Unemp. Rate', 'Emp. Growth',
                'CPI Inflation', 'Core Inflation (CPIX)', 'GDP Inflation',
                '10 Year  Bnchmk. Govt. Bond Rate', 'Exchange Rate         (U.S.$)',
                'US Real GDP Growth', "US Gov't Bond Rate (10 years)",
                'US CPI Inflation', 'US GDP Inflation', 'Oil Price   WTI   $US/Barrel',
                'Gas Price  Henry Hub   $US/mmbtu', 'ATOM_V41693242', 'CPIW',
                'CPI_COMMON', 'CPI_MEDIAN', 'CPI_TRIM', 'STATIC_CPIXFET',
                'STATIC_TOTALCPICHANGE', 'GDP (millions 2012 Constant Price)',
                'One storey price', 'Two storey price', 'Townhouse price',
                'Apartment price', 'interest rate', 'Housing index',
                'Number of families', 'Number of immigrants', 'Population']

    l_2020 = [[date_numeric('2020-09'), -5.8, 9.7, -5.5, 0.7, 1.2, 0.3, 0.7, 74.2, -4.3,
                0.8, 1.2, 0.9, 39, 2.1, 1.0, 1.1, 1.4, 2.0, 1.8, 0.8,
                0.5, 1927305.0, 488100, 742100, 527000, 439800, 0.5,
                106.5, 10330000, 226309, 38007166]]
    test_df_2020 = pd.DataFrame(data=l_2020, columns=columns_)
    print(f"Non-cleaned predicted value for 2020-09: {round(list(best_ridge_model.predict(test_df_2020))[0], 2)}. Actual value for 2020-09: 601193.53")

    l_2021 = [[date_numeric('2021-09'), 5, 7.6, 4.6, 3.1, 2.6, 7.1, 1.3, 79.9, 5.9, 1.4, 4.2,
               3.7, 66, 3.5, 3.7, 3.5, 3.1, 3, 3.5, 3.2, 4.4, 2009220,618200, 927600,
               645200, 498700, 0.5, 118.5, 10470000, 226309, 38226498]]
    test_df_2021 = pd.DataFrame(data=l_2021, columns=columns_)
    print(f"Non-cleaned predicted value for 2021-09: {round(list(best_ridge_model.predict(test_df_2021))[0], 2)}. Actual value for 2021-09: 684798.12")

    l_2022 = [[date_numeric('2022-09'), 3.2, 5.4, 3.5, 6.8, 5.4, 8.3, 2.8, 77.9, 1.7, 2.8, 7.9,
               7.1, 97, 7.1, 6, 6, 6, 5, 5.3, 5.4, 6.9, 2078250, 625200, 953100,
               687400, 544800, 1.25, 126, 10610000, 492984, 38929902]]
    test_df_2022 = pd.DataFrame(data=l_2022, columns=columns_)
    print(f"Non-cleaned predicted value for 2022-09: {round(list(best_ridge_model.predict(test_df_2022))[0], 2)}. Actual value for 2022-09: 639485.32")

    return None
