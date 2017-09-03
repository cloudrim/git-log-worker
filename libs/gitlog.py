import os
from datetime import datetime


class GitLog():
    def __init__(self, giturl, branch, path):
        self.giturl = giturl
        self.branch = branch
        self.path = path
        self.domain = self.giturl.split("/")[2]
        self.group = self.giturl.split("/")[3]
        self.project = self.giturl.split("/")[4].split(".")[0]

    def git_clone(self):
        print os.popen("git clone " + self.giturl + " tmp").readlines()

    def git_log(self):
        log_stream = os.popen('git log --no-merges --pretty=format:%H,%an,%ae,%at,%cn,%ce,%ct','r')
        key = ["revision","author","author_email", "author_date", "committer", "committer_email", "committer_date"]
        git_log_data = []
        for item in log_stream.readlines():
            revision_data = item.split(",")
            revision_data[3] = datetime.utcfromtimestamp(int(revision_data[3])).strftime('%Y%m%d%H%M%S')
            revision_data[6] = datetime.utcfromtimestamp(int(revision_data[6])).strftime('%Y%m%d%H%M%S')
            insert_data = dict(zip(key, revision_data))
            git_log_data.append(insert_data)
        return git_log_data

    def git_show(self, revision):
        git_show_data = []
        git_show_stream = os.popen("git show " + revision + " --pretty=tformat: --numstat")
        return git_show_stream


if __name__ == "__main":
    git_url = "https://github.com/modoojunko/git-log-service.git" #use http instead of git
    branch = "master"
    user = ""
    passwd = ""
    path = ""
    repo = GitLog(git_url,branch,path)
    #repo.remove_tmp()
    #repo.git_clone()
    #repo.generate_post_body()
    #os.chdir("tmp")


# commit diff