from typing import Callable
import datetime
import yaml
import boto3

def get_secret_value_from_ssm(secret_name: str, client: boto3.client) -> str:
    """Get secret value from AWS parameter store

    :param secret_name: [description]
    :type secret_name: str
    :param client: [description]
    :type client: boto3.client
    :return: [description]
    :rtype: str
    """    
    response = client.get_parameter(
      Name = secret_name,
      WithDecryption = True
    )

    secret_value = response['Parameter']['Value']
    return secret_value


def read_yaml(path:str) -> dict:
    """Read in configuration from yaml file

    :param path: path to yaml file
    :type path: str
    :return: config
    :rtype: dict
    """    
    try:
        with open(path, 'r') as metadata:
            conf = yaml.safe_load(metadata)
    except yaml.YAMLError as err:
        print(err)
    return conf



def get_execution_dates(execution_date: datetime.date, attribution_window: int):
    """Generator function taking one execution_date and yielding a list of execution_dates with attribution in consideration

    :param execution_date: the specific date when data is pulled
    :type execution_date: str
    :param attribution_window: number of days of attribution
    :type attribution_window: int
    :yield: execution_date up to the beginning of the attribution window
    :rtype: datetime.date
    """
    # TODO. logic needs to be refined if the granularity is hourly not daily
    # if it is older than attribution_window, then no attribution run has to be considered
    beginning_of_attribution_window = datetime.date.today() - datetime.timedelta(attribution_window)


    if execution_date < beginning_of_attribution_window:
        yield execution_date
    else:
        for n in range(attribution_window):
            yield execution_date - datetime.timedelta(days=n)


def attribution_window(num_of_days: int):
    """Decorator to handle data source attribution window 

    :param pull_data_func: function to pull data from source
    :type pull_data_func: Callable[[datetime.date, str, dict], None]
    :return: a wrapper of pull_data_func
    :rtype: Callable[[datetime.date, str, dict], None]
    """
    def decorator(pull_data_func):
        def wrapper(execution_date, *args, **kwargs):
            for ed in get_execution_dates(execution_date, num_of_days):
                print(f"execution_date: {ed}")
                pull_data_func(ed, *args, **kwargs)
        return wrapper
    return decorator