from .supamodel import Supamodel

_default_instance = Supamodel()

def login(api_key: str = None):
    _default_instance.login(api_key)

def init(experiment_name: str, config: dict, main_metric: str = None, log_compute: bool = True):
    _default_instance.init(experiment_name, config, main_metric, log_compute)

def log(metric_name: str, value: float):
    _default_instance.log(metric_name, value)
