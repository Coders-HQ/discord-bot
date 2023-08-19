import os, requests, discord

from typing import Iterable
from math import ceil
from github import Github, Issue, PaginatedList
from github.GithubException import UnknownObjectException, BadCredentialsException


class GitHub:
    """Class to handle all github issue queries"""

    def __init__(self):
        self.URL = "https://raw.githubusercontent.com/{}"

        self.authenticate()

    def validate_link(self, url: str) -> bool:
        """Checks if the link is a valid github link"""
        return "github.com" in url

    def get_code_block(self, url: str) -> tuple[list, str]:
        """Function to return the code from the requested github url"""
        code_lst = []

        line = url.split("#L")[1:]
        parts = url.replace("/blob", "")
        data = parts.split("github.com/")[-1]
        code_url = self.URL.format(data)
        info_str = self.get_repo_info(code_url)

        if len(line) > 1:
            n1, n2 = int(line[0].replace("-", "")), int(line[1]) + 1

            if n1 < n2:
                num_range = range(n1, n2)
            else:
                num_range = range(n2 - 1, n1 + 1)

            looper = num_range
        else:
            looper = line

        for i in looper:  # IMPROVE EFFICIENCY
            code = (
                requests.get(code_url).content.decode("utf-8").split("\n")[int(i) - 1]
            )  # NOT FOUND ERROR
            code_lst.append(code)

        return code_lst, info_str

    def get_repo_info(self, url: str) -> tuple[str, str]:
        """Returns info about the github code block"""
        url = url.replace("https://raw.githubusercontent.com/", "")
        parts = url.split("/")[3:]
        file_data = "/".join(parts).split("#")
        file_path = file_data[0]
        lang = file_path.split(".")[-1]
        line = file_data[1:]

        if len(line) > 1:
            line_count = "lines"
        else:
            line_count = "line"

        line_info = f"{line_count} {''.join(''.join(line).split('L'))}"
        data_string = f"`{file_path}` {line_info}"

        return data_string, lang

    def get_issue(self, num: int) -> Issue.Issue | None:
        """Returns `Issue`, if exists, else returns `None`"""
        if not self.repo:
            return
        try:
            issue = self.repo.get_issue(num)
        except UnknownObjectException:
            return False
        return issue

    def list_issues(
        self
    ) -> PaginatedList.PaginatedList | list[list] | None:
        """Returns the list of issues of the repo, or the paginated list of issue"""
        if not self.repo:
            return
        issues = self.repo.get_issues()
        return issues

    def create_issue(
        self, labels: list[str], title: str, body: str = ""
    ) -> Issue.Issue | None:
        """Creates an issue with the given options and returns it"""
        if not self.repo:
            return

        if labels:
            try:
                lbls = []
                for label in labels:
                    lbls.append(self.repo.get_label(label))
            except UnknownObjectException:
                return False
            issue = self.repo.create_issue(title=title, labels=lbls, body=body)
        else:
            issue = self.repo.create_issue(title=title, body=body)

        return issue

    def update_issue(
        self, num: int, title: str, body: str = "", labels: str = None
    ) -> Issue.Issue | None:
        """Updates the issue with the given option"""
        if not self.repo:
            return
        try:
            issue = self.repo.get_issue(num)
            issue.edit(title, body, labels=labels)

            return issue
        except UnknownObjectException:
            return False

    def close_issue(self, num: int) -> Issue.Issue | None:
        """Closes the given issue"""
        if not self.repo:
            return
        
        issue = self.repo.get_issue(num)
        issue.edit(state="closed")
        return issue

    def get_all_labels(self) -> list[str]:
        """Gets all the label names within the repo"""
        if not self.repo:
            return
        return [label for label in [each.name for each in self.repo.get_labels()]]

    def get_details(self, num: int) -> Issue.Issue | None:
        """Returns title, body and labels from `Issue`, if exists, else returns `None`"""
        if not self.repo:
            return
        try:
            issue = self.repo.get_issue(num)
        except UnknownObjectException:
            return False

        return issue.title, issue.body, [label.name for label in issue.labels]

    def prepare_pagination(self, to_paginate: Iterable) -> list[list]:
        """Takes in a set of data and creates a list of list like content in a page"""
        total_items = to_paginate.totalCount
        r_count = ceil(total_items / 5)
        c_count = 5
        main = []
        for i in range(r_count):
            lst = []
            for j in range(c_count):
                idx = c_count * i + j
                if idx >= total_items:
                    break
                lst.append(to_paginate[idx])
            main.append(lst)

        return main

    def authenticate(self):
        GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)
        GITHUB_REPO = os.getenv("GITHUB_REPO", None)

        try:
            if not GITHUB_REPO or not GITHUB_TOKEN:
                self.repo = None
                return False
            self.GHApi = Github(GITHUB_TOKEN)
            self.repo = self.GHApi.get_repo(GITHUB_REPO)
            return True
        except (requests.exceptions.ConnectTimeout, BadCredentialsException):
            self.repo = None
            return False
        