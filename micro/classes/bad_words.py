import os


class BadWords():
    def __init__(self,logger):
        self.logger = logger
        self.insults = get_insult_list()

    def is_it_insult(self, msg_lst):
        try:
            msg = ' '.join(msg_lst)

            strict = any(insult in msg for insult in self.insults)
            lenient = any(insult in msg_lst for insult in self.insults)
            
            return strict,lenient

        except Exception as e:
            self.logger.error("Error occured while checking if message is an insult %s"%e)

def get_insult_list():
    with open('static/profanitylist.txt', 'r') as file:
        words = file.read().split('\n')
    return words

