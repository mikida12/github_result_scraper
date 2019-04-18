import logging

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

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
        logging.INFO("--------------------------------")
        logging.INFO("title: {}".format(self.title))
        logging.INFO("link: {}".format(self.link))
        logging.INFO("description: {}".format(self.description))
        logging.INFO("tags: {}".format(self.tags))
        logging.INFO("datetime: {}".format(self.datetime))
        logging.INFO("language: {}".format(self.language))
        logging.INFO("stars: {}".format(self.stars))

