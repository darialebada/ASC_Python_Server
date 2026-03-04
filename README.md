# Le Stats Sportif: Client - Server App

## Organization

### Project Structure

The application implementation is located in the **app/** directory:

- **`__init__.py`**
  - Initializes the web server
  - Creates the directory used for storing request results (if it does not already exist)
  - Initializes the **ThreadPool** (implicitly creating the threads)
  - Starts processing the data from the input file

- **`data_ingestor.py`**
  - Reads and processes data from the input file
  - Stores only the necessary information in a **list of dictionaries**

- **`task_runner.py`**
  - Contains the **ThreadPool** class responsible for managing threads:
    - initializes threads
    - adds tasks to the queue
    - closes threads at the end
  - Contains the **TaskRunner** class representing worker threads (`run()` executes tasks)

- **`task_solver.py`**
  - Contains functions responsible for solving the tasks and computing the requested statistics

- **`routes.py`**
  - Defines the routes used when the server receives requests

- **`logging.py`**
  - Initializes the logger and handler used to record runtime information

The **unittests/** directory contains:

- **`TestWebserver.py`**
  - Tests the correctness of functions from `app/task_solver.py` using two sample queries

- **`test_data.csv`**
  - A small dataset extracted from the main file used for validating functionality

---

## General Approach

When the application starts, all components are automatically initialized:

- the dataset to be processed
- the **ThreadPool**
- the worker threads

The routing logic works as follows:

1. When a request is received, the server checks whether it is still running (i.e., a `graceful_shutdown` request has not been issued).
2. If the server is active:
   - the request data is processed
   - a unique **job_id** is generated
   - the task is sent to the **ThreadPool** and added to the processing queue.

A **synchronized Queue** is used to store tasks.

The **ThreadPool** only adds tasks to the queue. Worker threads retrieve tasks using `Queue.get()`, which is **blocking**, meaning threads wait until tasks are available.

Each task is processed and the result is written to a file named after the **job_id**, after which the task is marked as **completed**.

For **graceful shutdown**, an `Event()` object is used to notify the ThreadPool:

- no new tasks should be added to the queue
- threads should finish execution once the queue becomes empty.

---

## Data Storage

Dictionaries are primarily used for storing and processing data.

Examples:

- Input file data is stored as a **list of dictionaries**
- Tasks are represented as dictionaries containing:
  - `job_id`
  - request type
  - query
  - status (when needed)

---

## Was the Assignment Useful?

Yes. The assignment resembles a **real client–server application**, which is common in practice.  
Additionally, the **unit testing component** was particularly interesting, since testing is not strongly emphasized in many university courses.

---

## Implementation Evaluation

I believe the implementation is **efficient**, especially considering that I had limited experience with Python before this semester.  
Overall, I am satisfied with the result, although there is always room for improvement. With more experience, I might approach the implementation differently.

---

## Implementation Details

The entire assignment specification was implemented:

- routes
- unit tests
- logging

**Challenges encountered:**

- understanding the full requirements initially

Once the design was clear, the implementation progressed smoothly.

**Interesting aspects learned:**

- writing Python code more efficiently
- using **synchronization primitives** for concurrent programming

---

## Resources Used

- Laboratories 2 and 3 from **Concurrent Programming in Python (ASC)**
- Official Python documentation:

  - Queue  
    https://docs.python.org/3/library/queue.html

  - Logging  
    https://docs.python.org/3/library/logging.html

  - RotatingFileHandler  
    https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler

  - unittest  
    https://docs.python.org/3/library/unittest.html

---

## Git Repository

https://github.com/darialebada/ASC_Python_Server
