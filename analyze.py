# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

from libs.GitLog import GitLog
from libs.ServiceApi import ServiceApi

if __name__ == "__main__":
    giturl = "https://github.com/ansible-semaphore/semaphore.git" #use http instead of git
    branch = "master"
    service_ip = "localhost"
    service_port = 5000
    user = ""
    passwd = ""
    path = ""
    repo = GitLog(giturl=giturl, branch=branch, path=path)
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
    repo_api = ServiceApi("http://" + service_ip + ":" + str(service_port) + "/repo")

    # insert repo table
    if repo_api.check_data_exist(params):
        repo_id = repo_api.query_id(params)
    else:
        result = repo_api.post_data(body)
        #print(result)
        repo_id = int(result["data"]["id"])
    #print(repo_id)
    # insert commit table
    for commit in repo.git_log():
        commit["last_update"] = datetime.strftime('%Y%m%d%H%M%S')
        print "add commit data :" + str(commit)
        commit_api = ServiceApi("http://" + service_ip + ":" + str(service_port) + "/repo/" + str(repo_id) + "/commit")
        commit_api.post_data(json.dumps(commit))
        commit_revision = commit["revision"]
        params = {"revision": commit_revision}
        response_data = commit_api.query_data(params)["data"]
        response_data_commit_id = response_data["id"]
        response_data_revision = response_data["revision"]
        # insert commit diff
        commit_diff_api = ServiceApi("http://" + service_ip + ":" + str(service_port) + "/repo/" + str(repo_id) + "/commit/"
                                     + str(response_data_commit_id) + "/commit_diff")
        commit_diff_raw = repo.git_show(response_data_revision).readlines()
        for line in commit_diff_raw:
            if line:
                line_content = line.strip().split("\t")
                if line_content[0].isalnum():
                    add_line = line_content[0]
                else:
                    add_line = 0
                if line_content[1].isalnum():
                    del_line = line_content[1]
                else:
                    del_line = 0
                file_modified = line_content[2]
            commit_diff_post_body = json.dumps({
                "commit_id": response_data_commit_id,
                "last_update": datetime.strftime('%Y%m%d%H%M%S'),
                "change_file": file_modified,
                "add_lines": add_line,
                "del_lines": del_line
            })
            commit_diff_get_params = {
                "commit_id": response_data_commit_id,
                "change_file": file_modified,
                "add_lines": add_line,
                "del_lines": del_line
            }
            query_commit_diff_data = commit_diff_api.query_data(commit_diff_get_params)
            if query_commit_diff_data["data"]:
                print("exists data: " + str(commit_diff_get_params))
            else:
                commit_diff_api.post_data(commit_diff_post_body)
                print("insert data: " + str(commit_diff_post_body))
