""" routes.py """
import json
from flask import request, jsonify
from app import webserver

@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """ /api/post_endpoint """
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)

    # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """ /api/get_results/<job_id> """
    # Check if job_id is valid
    if webserver.tasks_runner.check_valid_job_id(job_id) is False:
        return jsonify({'status': 'Invalid job_id'})

    index_res = int(job_id.split('_').pop()) - 1
    if webserver.tasks_runner.tasks_state[index_res][job_id] == 'done':
        # Read the result from disk
        file_name = 'results/' + job_id + '.txt'
        with open(file_name, 'r', encoding='utf-8') as f:
            res = json.load(f)
        return jsonify({
            'status': 'done',
            'data': res
        })
    # If not, return running status
    return jsonify({'status': 'Still running'})


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    request_type = 'states_mean'
    job_id = ''
    with webserver.tasks_runner.lock:
        job_id = 'job_id_' + str(webserver.job_counter)
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(data, request_type, job_id)

    return jsonify({'job_id': job_id})


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    request_type = 'state_mean'
    job_id = ''
    with webserver.tasks_runner.lock:
        job_id = 'job_id_' + str(webserver.job_counter)
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(data, request_type, job_id)

    return jsonify({'job_id': job_id})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    request_type = 'best5'
    job_id = ''
    with webserver.tasks_runner.lock:
        job_id = 'job_id_' + str(webserver.job_counter)
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(data, request_type, job_id)

    return jsonify({'job_id': job_id})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    request_type = 'worst5'
    job_id = ''
    with webserver.tasks_runner.lock:
        job_id = 'job_id_' + str(webserver.job_counter)
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(data, request_type, job_id)

    return jsonify({'job_id': job_id})


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    request_type = 'global_mean'
    job_id = ''
    with webserver.tasks_runner.lock:
        job_id = 'job_id_' + str(webserver.job_counter)
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(data, request_type, job_id)

    return jsonify({'job_id': job_id})


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    request_type = 'diff_from_mean'
    job_id = ''
    with webserver.tasks_runner.lock:
        job_id = 'job_id_' + str(webserver.job_counter)
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(data, request_type, job_id)

    return jsonify({'job_id': job_id})


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    request_type = 'state_diff_from_mean'
    job_id = ''
    with webserver.tasks_runner.lock:
        job_id = 'job_id_' + str(webserver.job_counter)
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(data, request_type, job_id)

    return jsonify({'job_id': job_id})


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    request_type = 'mean_by_category'
    job_id = ''
    with webserver.tasks_runner.lock:
        job_id = 'job_id_' + str(webserver.job_counter)
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(data, request_type, job_id)

    return jsonify({'job_id': job_id})


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    request_type = 'state_mean_by_category'
    job_id = ''
    with webserver.tasks_runner.lock:
        job_id = 'job_id_' + str(webserver.job_counter)
        webserver.job_counter += 1

    webserver.tasks_runner.add_task(data, request_type, job_id)

    return jsonify({'job_id': job_id})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    """ index """
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    """ get_defined_routes """
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
