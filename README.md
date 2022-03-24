# checkMerge
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/EddDoubleD/checkMerge)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/EddDoubleD/checkMerge/python-gitlab) <br/>

This script is designed to parse merge requests in gitlab <br/>

## How to use 
* Create an image based on python:3.8-slim-buster
* Run the script on the generated image
* Generate a token as [instructed](https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html) 
* Run script
<br/>

```python
python /code/main.py $GL_URL $TOKEN $MERGE_ID
```

## helpfulness
[How to use pipenv](https://webdevblog.ru/pipenv-rukovodstvo-po-novomu-instrumentu-python/) 

