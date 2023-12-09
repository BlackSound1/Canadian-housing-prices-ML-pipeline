if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error


@custom
def transform_custom(merged_df_copy, *args, **kwargs):
    
    # Create data and target variables
    X = merged_df_copy.drop(columns='Average price')
    y = merged_df_copy['Average price']

    # Split into TRAINING and TESTING data
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(X, y, train_size=0.8)

    # Split into TRAINING and VALIDATION data
    Xc_train, Xc_val, yc_train, yc_val = train_test_split(Xc_train, yc_train, train_size=0.8)

    # Figure out what the best alpha value is from a given set
    param_grid = {'alpha' : [12, 15, 20, 25, 30]}
    ridge_model_cleaned = Ridge(alpha=1)
    grid_search_cleaned = GridSearchCV(ridge_model_cleaned, param_grid)
    grid_search_cleaned.fit(Xc_train, yc_train)
    best_param_cleaned = grid_search_cleaned.best_params_
    best_param_cleaned

    # Train the Ridge model using this alpha value
    best_ridge_model_cleaned = grid_search_cleaned.best_estimator_
    best_ridge_model_cleaned.fit(Xc_train, yc_train)

    # Make predictions on the VALIDATION data
    ridge_predict_cleaned = best_ridge_model_cleaned.predict(Xc_val)
    rmse_cleaned = round(mean_squared_error(yc_val, ridge_predict_cleaned, squared=False), 2)
    print(f"The Ridge model has an RMSE of: {rmse_cleaned} with the VALIDATION data")

    # Make predictions on the TESTING data
    ridge_predict_cleaned = best_ridge_model_cleaned.predict(Xc_test)
    rmse_cleaned = round(mean_squared_error(yc_test, ridge_predict_cleaned, squared=False), 2)
    print(f"The Ridge model has an RMSE of: {rmse_cleaned} with the TESTING data")

    avg_of_Average_price_cleaned = round(merged_df_copy['Average price'].mean(), 2)
    print(f"Note that the average housing price is: {avg_of_Average_price_cleaned}")

    return None
