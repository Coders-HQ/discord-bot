import os
import pandas as pd
from discord import embeds

class QuestionQuery:

    def __init__(self,filename, logger):
        self.data = self._excel_to_dict(os.path.abspath(filename))
        self.logger = logger
    
    def _excel_to_dict(self, path):
        try:
            data = pd.read_excel(path)
            data.set_index('Command',inplace=True)
            return data.to_dict()
        except Exception as e:
            self.logger.error('Error in fetching the questions: %s'%e)

    def question(self, command):
        title, msg = self.data['Title']['who'], self.data['Answer']['who']
        if command in self.data['Answer'].keys():
            title, msg = self.data['Title'][command], self.data['Answer'][command]
        return self._toEmbed(title, msg)

    def _toEmbed(self, title, msg):
        try:
            return embeds.Embed.from_dict(
                {
                    'type'          :   'rich',
                    'title'         :   f'{title}',
                    'description'   :   f'{msg}',
                    'color'         :   0x00afb1,
                    'thumbnail'     : {
                        'url': 'https://www.arsal.xyz/CHQLogo.png'
                    }
                }
            )
        except Exception as e:
            self.logger.error("Error in creating Embed: %s"%e)