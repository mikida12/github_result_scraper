
class ResultObject:
    def __init__(self, title, link, description, tags, time, lang, stars):
        self.title = title
        self.link = link
        self.description = description
        self.tags = tags
        self.datetime = time
        self.language = lang
        self.stars = stars

    def print(self):
        print("--------------------------------")
        print("title: {}".format(self.title))
        print("link: {}".format(self.link))
        print("description: {}".format(self.description))
        print("tags: {}".format(self.tags))
        print("datetime: {}".format(self.datetime))
        print("language: {}".format(self.language))
        print("stars: {}".format(self.stars))

