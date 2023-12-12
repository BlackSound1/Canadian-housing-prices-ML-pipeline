from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
import pandas as pd
from os import path
from datetime import datetime

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(data: list, **kwargs) -> None:
    # Get the current datetime
    now = datetime.now()
    now = now.strftime('%Y-%m-%d--%H:%M:%S')

    # Get the respective data
    rmse_data = data[0]
    price_data = data[1]

    # Convert it to Pandas objects
    rmse_data = pd.Series(rmse_data)
    price_data = pd.DataFrame(price_data)

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'comp333-data'
    object_key = f'Results/Uncleaned/RMSE_data-{now}.json'

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        rmse_data,
        bucket_name,
        object_key,
    )

    object_key = f'Results/Uncleaned/price_data-{now}.json'

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        price_data,
        bucket_name,
        object_key,
    )
