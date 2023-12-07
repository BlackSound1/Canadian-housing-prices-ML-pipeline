if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

@transformer
def transform(merged_df, *args, **kwargs):
    
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

    # TRain the Ridge model using this alpha value
    best_ridge_model = grid_search.best_estimator_
    best_ridge_model.fit(X_train, y_train)

    ridge_predict = best_ridge_model.predict(X_val)
    rmse = mean_squared_error(y_val, ridge_predict, squared=False)
    
    print(f"The Ridge model has an RMSE of: {rmse}")

    return None


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is None, 'The output is defined'