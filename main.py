import json
import requests
import pandas as pd
import matplotlib


st = 0
# Open and read the JSON file
with open('gh3.json', 'rb') as file:
    st = file.read()

langs = []
watchers = []
dict = {}
y = json.loads(st)
headers = {'User-Agent': 'request', 'Authorization': 'token ' + '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'}
for i in zip(range(0, 50), y):
    req = requests.get(i[1]['repo'], headers=headers)
    if req.status_code == 200:
        req_j = json.loads(req.text)
        print(f"{req} type{type(req.status_code)} lang {req_j['language']}")
        lang = req_j['language'] 
        val = dict.get(lang)
        if val == None:
            #print('none')
            dict.update({lang: {'count': 1}})
        else:
            #print('has it')
            dict[lang]['count'] += 1
            

        #dict[req_j['language']].watchers = 1;
        #langs.append(req_j['language'])
        #watchers.append(req_j['watchers'])

#df = pd.DataFrame(data={'javascript': {'count': 10}, 'python':2})
df = pd.DataFrame(data=dict)
print(df)
fig = df.plot(kind='bar', figsize=(20, 16), fontsize=26).get_figure()
fig.savefig('test.png')
#print(watchers)

#for i in zip(range(0, 10), y):
    #print(i[1]['repo'])
# Print the data
