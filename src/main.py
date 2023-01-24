import json
import requests
from os import path

if __name__ == '__main__':
    try:
        with open(path.join(path.dirname(path.abspath(__file__)), 'data/settings.json')) as f:
            config = json.load(f)
    except IOError:
        print('File read error')
        exit(1)

    try:
        response = requests.post(config['url'], data=config['payload'])
        status = response.status_code
        if status == 201:
            msg = 'Smoke-test запущен'
            body = json.loads(response.content)
        else:
            msg = 'Ошибка выполнения'
            body = ''
        print(msg + "\n" + str(body['web_url']))
    except requests.exceptions.HTTPError as httpError:
        print("Http Error:", httpError)
    except requests.exceptions.ConnectionError as connectionError:
        print("Error Connecting:", connectionError)
    except requests.exceptions.Timeout as timeoutError:
        print("Timeout Error:", timeoutError)
    except requests.exceptions.RequestException as err:
        print("OOps: unexpected", err)


