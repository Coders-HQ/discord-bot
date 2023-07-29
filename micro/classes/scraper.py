import requests


class Scraper:
    def __init__(self, title):
        site = f"https://raw.githubusercontent.com/Coders-HQ/CodersHQ/main/docs/src/{title}.md"

        self.body = requests.get(site).text
        self.titles = None
        self.content_dict = None
        self.description = None
        self.init()

    def init(self):
        raw_content = self.body.strip().splitlines()

        content_title = ""
        content_list = []
        content_dict = {}
        take_title = True
        description = []

        for i in raw_content:
            if i != "":
                if i.startswith("### ") and take_title:
                    content_title = i[4:].split(" ")[0].lower()
                    take_title = False
                elif i.startswith("### ") and not take_title:
                    content_dict[content_title] = content_list

                    content_title = i[4:].split(" ")[0].lower()
                    content_list = []
                elif content_title == "":
                    description.append(i)
                else:
                    content_list.append(i)

        self.content_dict = content_dict
        self.titles = [i for i in content_dict]


if __name__ == "__main__":

    scraper = Scraper("features")
    for k in scraper.titles:
        print(scraper.content_dict[k])
