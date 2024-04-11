""" task_runner.py """
from queue import Queue
from threading import Thread, Event, Lock
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
        self.lock = Lock()
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
            self.threads.append(TaskRunner(i, self.tasks_queue, self.tasks_state,
                                           self.shutdown_event, self.data))
            self.threads[i].start()

    # add task to queue as dictionary
    def add_task(self, task, request_type, job_id):
        """ add task to queue """
        task['job_id'] = job_id
        task['request_type'] = request_type
        self.tasks_queue.put(task)
        self.tasks_state.append({job_id : 'running'})

    def check_valid_job_id(self, job_id):
        """ check if job_id is valid """
        for task in self.tasks_state:
            if job_id in task:
                return True
        return False

    def shutdown(self):
        """ shutdown threads """
        self.shutdown_event.set()


class TaskRunner(Thread):
    """ TaskRunner class - run tasks """
    def __init__(self, idx, tasks_queue, tasks_state, shutdown_event, data):
        """ default constructor """
        Thread.__init__(self)
        self.idx = idx
        self.tasks_queue = tasks_queue
        self.tasks_state = tasks_state
        self.event = shutdown_event
        self.data = data
        self.task_solver = TaskSolver(self.data)

    def run(self):
        """ run tasks """
        while True:
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            if self.event.is_set():
                break

            # get task from queue (blocking, so it waints until there is a task in the queue)
            task = self.tasks_queue.get()

            # check if directory exists
            if not os.path.exists('results'):
                os.makedirs('results')

            result = TaskSolver.solve_task(self.task_solver, task)

            result_status = {'status': 'done', 'data': result}
            # write result to file
            file_name = 'results/' + task['job_id'] + '.txt'
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(result_status, f)

            # get job_id index as int
            index = int(task['job_id'].split('_').pop()) - 1
            # mark task as done
            self.tasks_state[index][task['job_id']] = "done"

            self.tasks_queue.task_done()

        # end job
        self.join()
