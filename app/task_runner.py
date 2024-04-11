""" task_runner.py """
from queue import Queue
from threading import Thread, Event, Lock
import json
import os

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
            self.threads.append(TaskRunner(i, self.tasks_queue, self.tasks_state, self.data))
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

    def join_threads(self):
        """ join threads """
        # add None to the queue to stop threads after finishing the tasks
        for i in range(self.num_threads):
            self.tasks_queue.put(None)
        for i in range(self.num_threads):
            self.threads[i].join()

class TaskRunner(Thread):
    """ TaskRunner class - run tasks """
    def __init__(self, idx, tasks_queue, tasks_state, data):
        """ default constructor """
        Thread.__init__(self)
        self.idx = idx
        self.tasks_queue = tasks_queue
        self.tasks_state = tasks_state
        self.data = data

    def run(self):
        """ run tasks """
        while True:
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown

            # get task from queue (blocking, so it waints until there is a task in the queue)
            task = self.tasks_queue.get()
            # time to stop programme
            #if task is None:
            #    continue
            # run task

            # check if directory exists
            if not os.path.exists('results'):
                os.makedirs('results')

            result = {}
            # process request
            if task['request_type'] == 'state_mean':
                result = self.state_mean(task['question'], task['state'])
            elif task['request_type'] == 'states_mean':
                result = self.states_mean(task['question'])
            elif task['request_type'] == 'best5':
                result = self.best5(task['question'])
            elif task['request_type'] == 'worst5':
                result = self.worst5(task['question'])
            elif task['request_type'] == 'global_mean':
                result = self.global_mean(task['question'])
            elif task['request_type'] == 'diff_from_mean':
                result = self.diff_from_mean(task['question'])
            elif task['request_type'] == 'state_diff_from_mean':
                result = self.state_diff_from_mean(task['question'], task['state'])
            elif task['request_type'] == 'state_mean_by_category':
                result = self.state_mean_by_category(task['question'], task['state'])
            elif task['request_type'] == 'mean_by_category':
                result = self.get_mean_by_category(task['question'])

            json_string = json.dumps(result)
            # write result to file
            file_name = 'results/' + task['job_id'] + '.txt'
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(json_string)

            # get job_id index as int
            index = int(task['job_id'].split('_').pop()) - 1
            # mark task as done
            self.tasks_state[index][task['job_id']] = "done"


    def get_states_values(self, q):
        """ get states after question and location """
        states_values = {}
        states_num = {}
        # get each row from file
        for row in self.data.list_data:
            #print(row)
            # same question
            if row['Question'] == q:
                if row['Location'] not in states_values:
                    # location hasn't been added yet to dictionary => add it
                    states_values[row['Location']] = float(row['Data_Value'])
                    states_num[row['Location']] = 1
                else:
                    # location already in dictionary => add new value to sum
                    states_values[row['Location']] += float(row['Data_Value'])
                    states_num[row['Location']] += 1
        for state in states_values:
            # average value for each state
            states_values[state] = states_values[state] / states_num[state]
        # return dictionary
        return states_values

    def state_mean(self, q, state):
        """ /api/state_mean """
        numm = 0
        summ = 0
        for row in self.data.list_data:
            if row['Question'] == q and row['Location'] == state:
                # add to sum and count number of values
                summ += float(row['Data_Value'])
                numm += 1

        value = summ / numm
        return {state : value}

    def best5(self, q):
        """ /api/best5 """
        # get average values for each state
        states_values = self.get_states_values(q)
        sorted_states = {}

        if q in self.data.questions_best_is_min:
            order_by = False
        else:
            order_by = True

        # sort states by value and return first 5
        num = 1
        for state in sorted(states_values, key=states_values.get, reverse=order_by):
            sorted_states[state] = states_values[state]
            num += 1
            if num > 5:
                break

        return sorted_states

    def worst5(self, q):
        """ api/worst5 """
        # get average values for each state
        states_values = self.get_states_values(q)
        sorted_states = {}

        if q in self.data.questions_best_is_min:
            order_by = True
        else:
            order_by = False

        # sort states by value in descending order and return first 5
        num = 1
        for state in sorted(states_values, key=states_values.get, reverse=order_by):
            sorted_states[state] = states_values[state]
            num += 1
            if num > 5:
                break
        return sorted_states

    def states_mean(self, q):
        """ /api/states_mean """
        # get average values for each state
        states_values = self.get_states_values(q)
        sorted_states = {}
        # sort states by value
        for state in sorted(states_values, key=states_values.get, reverse=False):
            sorted_states[state] = states_values[state]

        return sorted_states

    def global_mean(self, q):
        """ /api/global_mean """
        sum_global = 0
        num = 0
        for row in self.data.list_data:
            # only look after question (location doesn't matter)
            if row['Question'] == q:
                sum_global += float(row['Data_Value'])
                num += 1
        val = sum_global / num
        return {"global_mean" : val}

    def diff_from_mean(self, q):
        """ /api/diff_from_mean """
        # get average values for each state
        states_values = self.get_states_values(q)
        # get average value for question (from all statess)
        global_mean_var = self.global_mean(q)

        states_diff = {}
        for state_mean in states_values:
            # difference between values for each state
            states_diff[state_mean] = global_mean_var["global_mean"] - states_values[state_mean]

        return states_diff

    def state_diff_from_mean(self, q, state):
        """ /api/state_diff_from_mean """
        # get average value for given state
        state_mean_var = self.state_mean(q, state)
        # get average value for question (from all statess)
        global_mean_var = self.global_mean(q)
        return {state : global_mean_var["global_mean"] - state_mean_var[state]}

    def get_states(self, q):
        """ function that returns a list of all states that answered the given question """
        states = []
        for row in self.data.list_data:
            if row['Question'] == q:
                if row['Location'] not in states:
                    states.append(row['Location'])
        return states

    def get_category_name(self, category, state, stratification_category, stratification):
        """ 
        function that returns a string that represents the category
        for mean_by_category functions
        """
        if category == 'with_state':
            return "('" + state + "', '" + stratification_category + "', '" + stratification + "')"
        return "('" + stratification_category + "', '" + stratification + "')"

    def get_state_mean_by_category(self, q, state, category):
        """ function that returns the average values for each category """
        dict_categories = {}
        dict_num_cat = {}
        for row in self.data.list_data:
            if row['Stratification_Category'] == '' or row['Stratification'] == '':
                continue
            if row['Question'] == q and row['Location'] == state:
                # get category name
                category_name = self.get_category_name(category, state,
                                                        row['Stratification_Category'],
                                                        row['Stratification'])
                if category_name not in dict_categories:
                    # category hasn't been added yet to dictionary => add it
                    dict_categories[category_name] = float(row['Data_Value'])
                    dict_num_cat[category_name] = 1
                else:
                    # category already in dictionary => add new value to sum
                    dict_categories[category_name] += float(row['Data_Value'])
                    dict_num_cat[category_name] += 1

        dict_answer = {}
        # sort after keys (alfabetically)
        for row in sorted(dict_categories.keys()):
            # calculate average value for each category
            dict_answer[row] = dict_categories[row] / dict_num_cat[row]

        return dict_answer

    def get_mean_by_category(self, q):
        """ /api/mean_by_category """
        # get all states that answered the question
        states = self.get_states(q)
        state_values_category = {}

        # get values for states sorted alfabetically
        for state in sorted(states):
            # get average values for all categories for each state
            dict_categories = self.get_state_mean_by_category(q, state, 'with_state')
            # add new pairs key-value to current dictionary
            state_values_category.update(dict_categories)

        return state_values_category

    def state_mean_by_category(self, q, state):
        """ /api/state_mean_by_category """
        # get average values for all categories for given state
        dict_categories = self.get_state_mean_by_category(q, state, 'no_state')
        # add values to dictionary
        return {state : dict_categories}
