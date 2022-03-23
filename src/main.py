# This script is designed to parse merge requests

import configparser
import logging.config
import re
from os import path
from sys import argv

import gitlab  # python-gitlab

GIT_LAB = "GitLab"
URL_VAL = "gitlab_url"
PROJECT_VAL = "project_id"
TOKEN_VAL = "private_token"

# logger init
try:
    LOGGING_CONFIG = path.join(path.dirname(path.abspath(__file__)), 'ini/logging.ini')
    print(LOGGING_CONFIG)
    logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=True)
except KeyError:
    # Creating a default logger
    logging.basicConfig(filename='checkMerge.log', level='DEBUG', filemode='w', format='%(asctime)s %(name)s - %('
                                                                                       'levelname)s:%(message)s')
    print('Logger redefined')

log = logging.getLogger(__name__)

# settings init
try:
    SETTING_CONFIG = path.join(path.dirname(path.abspath(__file__)), 'ini/settings.ini')
    config = configparser.ConfigParser()
    config.read(SETTING_CONFIG)
except KeyError:
    print('Setting redefined')
    exit(2)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    log.debug("--------- desc analysis start ---------")
    if argv.__len__() < 3:
        log.error("not enough parameters")
        exit(1)
    # get argument's
    script, url, token, projectId, mergeId = argv
    regExp = config.get('regExp', 're')
    # init gitlab property and connect
    gl = gitlab.Gitlab(url=url, private_token=token)
    gl.auth()
    logging.debug("gitlab connection success...")
    project = gl.projects.get(projectId, lazy=True)
    mr = project.mergerequests.get(mergeId)
    file = open("result.txt", "w+")
    for change in mr.changes().get("changes", True):
        filePath = change.get("new_path")
        if re.match(regExp, filePath.lower()) is not None:
            log.debug("Файл %s соответствует маске %s", filePath, regExp)
            file.write("Y")
            file.close()
            exit(0)
    file.write("N")
    file.close()