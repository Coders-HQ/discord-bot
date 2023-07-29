import json

class Resources:
   def __init__(self, path='static/resources.json'):
      with open(path) as file:
         self.data = json.load(file)

   def get_all_langs(self):
      return [k for k in self.data]
      
   def get_all_kw(self):
      return {k:v['Keywords'] for k,v in self.data.items()}
   
   def get_kw_lang_map(self):
      kws = self.get_all_kw()
      langs = self.get_all_langs()
      return {x:y for x,y in zip(langs,kws.values())}

   def get_details(self, name):
      return self.data[name]

   def reload_resource(self,path='static/dummy2.json'):
      with open(path) as file:
         self.data = json.load(file)
