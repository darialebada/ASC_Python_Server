""" task_solver.py """

class TaskSolver:
    """ TaskSolver class - solve tasks """
    def __init__(self, data):
        """ Initialize TaskSolver class """
        self.data = data

    def solve_task(self, task):
        """ solve task """
        task_res = {}
        if task['request_type'] == 'state_mean':
            task_res = self.state_mean(task['question'], task['state'])
        elif task['request_type'] == 'states_mean':
            task_res = self.states_mean(task['question'])
        elif task['request_type'] == 'best5':
            task_res = self.best5(task['question'])
        elif task['request_type'] == 'worst5':
            task_res = self.worst5(task['question'])
        elif task['request_type'] == 'global_mean':
            task_res = self.global_mean(task['question'])
        elif task['request_type'] == 'diff_from_mean':
            task_res = self.diff_from_mean(task['question'])
        elif task['request_type'] == 'state_diff_from_mean':
            task_res = self.state_diff_from_mean(task['question'], task['state'])
        elif task['request_type'] == 'state_mean_by_category':
            task_res = self.state_mean_by_category(task['question'], task['state'])
        elif task['request_type'] == 'mean_by_category':
            task_res = self.get_mean_by_category(task['question'])
        return task_res

    def get_states_values_helper(self, q):
        """ get states after question and location """
        states_values = {}
        states_num = {}
        # get each row from file
        for row in self.data.list_data:
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
        states_values = self.get_states_values_helper(q)
        sorted_states = {}

        if q in self.data.questions_best_is_min:
            order_by = False
        else:
            order_by = True

        # sort states by value and return first 5
        num = 0
        for state in sorted(states_values, key=states_values.get, reverse=order_by):
            sorted_states[state] = states_values[state]
            num += 1
            if num == 5:
                break

        return sorted_states

    def worst5(self, q):
        """ api/worst5 """
        # get average values for each state
        states_values = self.get_states_values_helper(q)
        sorted_states = {}

        if q in self.data.questions_best_is_min:
            order_by = True
        else:
            order_by = False

        # sort states by value in descending order and return first 5
        num = 0
        for state in sorted(states_values, key=states_values.get, reverse=order_by):
            sorted_states[state] = states_values[state]
            num += 1
            if num == 5:
                break

        return sorted_states

    def states_mean(self, q):
        """ /api/states_mean """
        # get average values for each state
        states_values = self.get_states_values_helper(q)
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
        states_values = self.get_states_values_helper(q)
        # get average value for question (from all states)
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
        # get average value for question (from all states)
        global_mean_var = self.global_mean(q)
        return {state : global_mean_var["global_mean"] - state_mean_var[state]}

    def get_states_helper(self, q):
        """ function that returns a list of all states that answered the given question """
        states = []
        for row in self.data.list_data:
            if row['Question'] == q:
                if row['Location'] not in states:
                    states.append(row['Location'])
        return states

    def get_category_name_helper(self, category, state, stratification_category, stratification):
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
                # ignore rows with empty values
                continue
            if row['Question'] == q and row['Location'] == state:
                # get category name
                category_name = self.get_category_name_helper(category, state,
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
        # sort after keys (alphabetically)
        for row in sorted(dict_categories.keys()):
            # calculate average value for each category
            dict_answer[row] = dict_categories[row] / dict_num_cat[row]

        return dict_answer

    def get_mean_by_category(self, q):
        """ /api/mean_by_category """
        # get all states that answered the question
        states = self.get_states_helper(q)
        state_values_category = {}

        # get values for states sorted alphabetically
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
