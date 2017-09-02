import json
import os
from datetime import datetime

from libs.GitLog import GitLog
from libs.ServiceApi import ServiceApi

if __name__ == "__main__":
    giturl = "https://github.com/modoojunko/git-log-service.git" #use http instead of git
    branch = "master"
    user = ""
    passwd = ""
    path = ""
    repo = GitLog(giturl=giturl,branch=branch,path=path)
    #utils.remove_tmp()
    #repo.git_clone()
    datetime = datetime.now()
    body = json.dumps({
            "domain": giturl.split("/")[2],
            "group": giturl.split("/")[3],
            "project": giturl.split("/")[4].split(".")[0],
            "path": path,
            "last_update": datetime.strftime('%Y%m%d%H%M%S')
        })
    params = {"domain": giturl.split("/")[2],
              "group": giturl.split("/")[3],
              "project": giturl.split("/")[4].split(".")[0]
              }
    os.chdir("tmp")
    service = ServiceApi("http://localhost:5000/repo")
    if service.check_data_exist(params):
        repo_id = service.query_id(params)
    else:
        result = service.post_data(body)
        #print(result)
        repo_id = int(eval(result)["data"]["id"])
    print(repo_id)
    for commit in repo.git_log():
        commit["last_update"] = datetime.strftime('%Y%m%d%H%M%S')
        #print(commit)
        commit_api = ServiceApi("http://localhost:5000/repo/" + str(repo_id) + "/commit")
        print(commit_api.post_data(json.dumps(commit)))
