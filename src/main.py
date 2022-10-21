# This script is designed to parse merge requests

import configparser
import logging.config
import re
from os import path
from sys import argv
import requests

import gitlab  # python-gitlab

GIT_LAB = "GitLab"
URL_VAL = "gitlab_url"
PROJECT_VAL = "project_id"
TOKEN_VAL = "private_token"

logging.basicConfig(filename='checkMerge.log', level='DEBUG', filemode='w', format='%(asctime)s %(name)s - %('
                                                                                   'levelname)s:%(message)s')
print('Logger redefined')
log = logging.getLogger(__name__)

# settings init
config = None
try:
    SETTING_CONFIG = path.join(path.dirname(path.abspath(__file__)), 'data/check_merge.ini')
    print(SETTING_CONFIG)
    config = configparser.ConfigParser()
    config.read(SETTING_CONFIG)
except KeyError:
    print('Setting redefined')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    log.debug("--------- check merge request ---------")
    if argv.__len__() < 4:
        log.error("not enough parameters")
        exit(1)
    # get argument's
    script, url, token, projectId, mergeId, mr_url = argv

    regExp = ".*(\.java|pom.xml)"
    # Инициализируем регулярные выражения для отправки запроса на сервер студии
    api = None
    regStudio = None
    # regExp = ".*(\.java|pom.xml)"
    if config is not None:
        api = config.get('studio', 'api')
        regStudio = config.get('studio', 're')

    # init gitlab property and connect
    gl = gitlab.Gitlab(url=url, private_token=token)
    gl.auth()
    logging.debug("gitlab connection success...")
    project = gl.projects.get(projectId, lazy=True)
    mr = project.mergerequests.get(mergeId)
    file = open("result.txt", "w+")
    find = False
    findStudio = False
    for change in mr.changes().get("changes", True):
        filePath = change.get("new_path")
        if not findStudio and api is not None and re.match(regStudio, filePath.lower()) is not None:
            print('Найдены файлы по маске')
            findStudio = True

        if find is False and re.match(regExp, filePath.lower()) is not None:
            log.debug("Файл %s соответствует маске %s", filePath, regExp)
            file.write("Y")
            file.close()
            find = True

    # Если файлы java или pom не найдены запишем N
    if not find:
        file.write("N")
        file.close()

    # Отправим curl запрос если найдены фалы по маске
    if findStudio:
        headers = {'content-type': 'application/json', 'accept': '*/*'}
        print('Выполняет отправка запроса')
        r = requests.post(api, data=mr_url, headers=headers)
