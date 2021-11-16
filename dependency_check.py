import requests
import json
with open('requirements.txt', 'r') as f:
    dependencies = f.readlines()
    f.close()
    dependencies_json = []
    dependencies = [ dependency.replace('\n','')  for dependency in dependencies if dependency != '\n']

    for dependency in dependencies:
        req_json= {}
        not_specified_version = True
        dependency_split = dependency.split('==')
        if len(dependency_split) > 1:
            not_specified_version = False
            url = 'https://pypi.org/pypi/' + dependency_split[0] + '/json'
            req = requests.request(method='GET', url=url)
            req_json = req.json()

            dependencies_json.append({
                "packageName": dependency_split[0],
                "currentVersion": dependency_split[1],
                "latestVersion": req_json['info']['version'],
                "outOfDate": dependency_split[1] != req_json['info']['version']
            })

        dependency_split = dependency.split('<=')
        if len(dependency_split) > 1:
            not_specified_version = False
            url = 'https://pypi.org/pypi/' + dependency_split[0] + '/json'
            req = requests.request(method='GET', url=url)
            req_json = req.json()

            dependencies_json.append({
                "packageName": dependency_split[0],
                "currentVersion": dependency_split[1],
                "latestVersion": req_json['info']['version'],
                "outOfDate": dependency_split[1] != req_json['info']['version']
            })

        dependency_split = dependency.split('>=')
        if len(dependency_split) > 1:
            not_specified_version = False
            url = 'https://pypi.org/pypi/' + dependency_split[0] + '/json'
            req = requests.request(method='GET', url=url)
            req_json = req.json()

            dependencies_json.append({
                "packageName": dependency_split[0],
                "currentVersion": req_json['info']['version'],
                "latestVersion": req_json['info']['version'],
                "outOfDate": req_json['info']['version'] != req_json['info']['version']
            })

        dependency_split = dependency.split('[')
        if len(dependency_split) > 1:
            not_specified_version = False
            url = 'https://pypi.org/pypi/' + dependency_split[0] + '/json'
            url_standard = 'https://pypi.org/pypi/' + dependency_split[0].split(']')[0] + '/json'
            req = requests.request(method='GET', url=url)
            req_standard = requests.request(method='GET', url=url_standard)
            req_json = req.json()
            req_json_standard = req_standard.json()

            dependencies_json.append({
                "packageName": dependency_split[0],
                "currentVersion": req_json_standard['info']['version'],
                "latestVersion": req_json['info']['version'],
                "outOfDate": req_json_standard['info']['version'] != req_json['info']['version']
            })

        if not_specified_version:
            url = 'https://pypi.org/pypi/' + dependency_split[0] + '/json'
            req = requests.request(method='GET', url=url)
            req_json = req.json()

            dependencies_json.append({
                "packageName": dependency_split[0],
                "currentVersion": req_json['info']['version'],
                "latestVersion": req_json['info']['version'],
                "outOfDate": req_json['info']['version'] != req_json['info']['version']
            })
    with open('dependency_check.json', 'w') as outfile:
        json.dump(dependencies_json, outfile)