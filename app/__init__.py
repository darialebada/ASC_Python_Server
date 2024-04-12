""" __init__.py """
import os
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

webserver = Flask(__name__)

# webserver.tasks_runner = ThreadPool()
# webserver.task_runner.start()

# check if directory exists
if not os.path.exists('results'):
    os.makedirs('results')

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.tasks_runner = ThreadPool(webserver.data_ingestor)

webserver.job_counter = 1

from app import routes
