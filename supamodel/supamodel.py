import requests
import time
import threading
import subprocess
    

class Supamodel:
    def __init__(self):
        self.url = 'https://api.cerelyze.com/'

    def login(self, api_key: str = None):
        self.api_key = api_key
    
    def init(self, experiment_name: str, config: dict, main_metric: str = None, log_compute: bool = True):
        self.experiment_name = experiment_name
        self.config = config
        self.main_metric = main_metric
        self.exp_id = self.create_experiment()
        if log_compute:
            print("Starting GPU logging...")
            self.start_gpu_monitor()
        print(f"Experiment created with id: {self.exp_id}")

    def create_experiment(self):
        response = requests.post(self.url + 'create_experiment', json={"api_key": self.api_key, "experiment_name": self.experiment_name, "config": self.config, "main_metric": self.main_metric})
        return response.json()

    def _log_metrics(self, metrics: dict):
        try:
            response = requests.post(self.url + 'log_metrics', json={"api_key": self.api_key, "experiment_id": self.exp_id, "metrics": metrics})
        except Exception as e:
            print(f"An error occurred while logging metrics: {e}")
            return None
        
        return response.json()
    
    def log(self, metric_name: str, value: float):
        try:
            self._log_metrics({metric_name: value})
        except Exception as e:
            print(f"An error occurred while logging metrics: {e}")
            return None
    
    def log_compute(self, metrics: dict):
        try:
            response = requests.post(self.url + 'log_compute', json={"api_key": self.api_key, "experiment_id": self.exp_id, "metrics": metrics})
        except Exception as e:
            print(f"An error occurred while logging compute: {e}")
            return None
        
        return response.json()

    def start_gpu_monitor(self):
        def monitor():
            while True:
                gpu_usages = self.get_gpu_usage()
                if gpu_usages:
                    self.log_compute({"gpu_usage": max(gpu_usages)}) # <-- need to change this later to log multiple gpus
                else:
                    print("Could not get GPU usage")
                    break
                time.sleep(1)
        
        thread = threading.Thread(target=monitor)
        thread.daemon = True
        thread.start()
    
    def get_gpu_usage(self):
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'], 
                                    capture_output=True, text=True, check=True)
            
            gpu_usages = [int(usage) for usage in result.stdout.strip().split('\n')]
            return gpu_usages
        except Exception as e:
            print(f"An error occurred while running nvidia-smi, make sure you have a machine with a GPU, or set log_compute=False in the init method")
            return None

