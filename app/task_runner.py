""" task_runner.py """
from queue import Queue
from threading import Thread, Event
import json
import os
from app.task_solver import TaskSolver

class ThreadPool:
    """
    You must implement a ThreadPool of TaskRunners
    Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
    If the env var is defined, that is the number of threads to be used by the thread pool
    Otherwise, you are to use what the hardware concurrency allows
    You are free to write your implementation as you see fit, but
    You must NOT:
      * create more threads than the hardware concurrency allows
      * recreate threads for each task
    """
    def __init__(self, data):
        """ default constructor """
        self.tasks_queue = Queue()
        self.num_threads = self.get_num_threads()
        self.threads = []
        self.shutdown_event = Event()
        self.tasks_state = []
        self.data = data
        # create and start threads
        self.create_threads()

    def get_num_threads(self):
        """ get number of threads """
        if 'TP_NUM_OF_THREADS' in os.environ:
            return os.environ['TP_NUM_OF_THREADS']
        return os.cpu_count()

    def create_threads(self):
        """ create threads """
        for i in range(self.num_threads):
            # add thread to list
            self.threads.append(TaskRunner(i, self.tasks_queue, self.tasks_state,
                                           self.shutdown_event, self.data))
            self.threads[i].start()

    # add task to queue as dictionary
    def add_task(self, task, request_type, job_id):
        """ add task to queue """
        task['job_id'] = job_id
        task['request_type'] = request_type
        self.tasks_queue.put(task)
        # remember threads' state - currently running
        self.tasks_state.append({job_id : 'running'})

    def check_valid_job_id(self, job_id):
        """ check if job_id is valid """
        for task in self.tasks_state:
            if job_id in task:
                # job exists in list => valid job_id
                return True
        return False

    def shutdown(self):
        """ set shutdown event to notify threads to stop when queue is empty """
        self.shutdown_event.set()
        # wait for threads to finish all tasks
        while not self.tasks_queue.empty():
            continue
        for thread in self.threads:
            thread.join()


class TaskRunner(Thread):
    """ TaskRunner class - run tasks """
    def __init__(self, idx, tasks_queue, tasks_state, shutdown_event, data):
        """ default constructor """
        Thread.__init__(self)
        self.idx = idx
        self.tasks_queue = tasks_queue
        self.tasks_state = tasks_state
        self.shutdown_event = shutdown_event
        self.data = data
        self.task_solver = TaskSolver(self.data)

    def run(self):
        """ run tasks """
        while True:
            # if event is set an queue empty => time to end thread
            if self.shutdown_event.is_set() and self.tasks_queue.empty():
                break

            # if queue is empty => continue till is_set() ot queue not empty
            # somehow save thread from wainting forever for queue.get()
            if self.tasks_queue.empty():
                continue

            # get task from queue (blocking, so it waits until there is a task in the queue)
            task = self.tasks_queue.get()

            #if task is None and self.shutdown_event.is_set():
            #    break

            # solve task
            result = TaskSolver.solve_task(self.task_solver, task)

            result_status = {'status': 'done', 'data': result}
            # create file and write result to it as json
            file_name = 'results/' + task['job_id'] + '.txt'
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(result_status, f)

            # get job_id index as int
            index = int(task['job_id'].split('_').pop()) - 1
            # mark task as done
            self.tasks_state[index][task['job_id']] = "done"
