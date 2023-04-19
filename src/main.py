import time

from flask import Flask, jsonify, request


app = Flask(__name__)


services = {}


@app.route('/services', methods=['GET'])
def get_all_services():
    return jsonify(services)


@app.route('/services/<service_name>', methods=['GET'])
def get_service_by_name(service_name: str):
    if service_name in services:
        return jsonify(services[service_name])
    else:
        return jsonify({'error': 'Service not found'})


@app.route('/services', methods=['POST'])
def post_service():
    service = request.json
    if service:
        name = service['name']
        description = service['description']
        state = service['state']

        if name not in services:
            services[name] = {'description': description, 'state': state, 'history': []}
        else:
            services[name]['description'] = description
            services[name]['state'] = state

        services[name]['history'].append({'state': state, 'time': time.time()})
        return jsonify(services[name])


@app.route('/services/sla', methods=['GET'])
def get_sla():
    total_services = len(services)

    if total_services:
        not_working_services = 0

        for service in services.values():
            if service['state'] != 'working':
                not_working_services += 1

        sla = 1 - (not_working_services / total_services)
        sla_percent = round(sla * 100, 3)
        return jsonify({'sla': sla_percent})
    else:
        return jsonify({'sla': 'No servers'})


if __name__ == '__main__':
    app.run(debug=True)  # Testing (debugging) only
