import json
from sys import argv
import requests


if __name__ == '__main__':
    # url, token, ref, run_type, suite_name
    if argv.__len__() != 6:
        print('Incorrect number of parameters, smoke-test will not run')
        exit(0)

    script, url, token, ref, run_type, suite_name = argv

    msg = ""
    body = ""
    try:
        payload = {
            'token': token,  # токен триггера пайплайна
            'ref': ref,
            'variables[RUN_TYPE]': run_type,
            'variables[SUITE_NAME]': suite_name
        }
        response = requests.post(url, data=payload)
        status = response.status_code
        if status == 201:
            msg = 'Smoke-test запущен'
            body = json.loads(response.content)
        else:
            msg = 'Ошибка выполнения'
        print(msg + "\n" + body)
    except requests.exceptions.HTTPError as httpError:
        print("Http Error:", httpError)
    except requests.exceptions.ConnectionError as connectionError:
        print("Error Connecting:", connectionError)
    except requests.exceptions.Timeout as timeoutError:
        print("Timeout Error:", timeoutError)
    except requests.exceptions.RequestException as err:
        print("OOps: unexpected", err)


