import requests
import pprint


class Telegraph:
    
    @staticmethod
    def getArticleContent(articleName) -> dict:
        articleName = articleName.split('/')[-1] if '/' in articleName else articleName
        r = requests.get(f'https://api.telegra.ph/getPage/{articleName}?return_content=true').json()
        if 'result' not in r:
            return None
        content_dict = {
            'article_name': r['result']['title'],
            'tags': []
        }
        for tag in r['result']['content']:
            for child in tag['children']:
                if type(child) == str:
                    content_dict['tags'].append({'p': child})
                elif type(child) == dict and child['tag'] == 'img':
                    content_dict['tags'].append({'img': child['attrs']['src']})
                elif type(child) == dict and child['tag'] == 'a':
                    content_dict['tags'].append({'a': child['attrs']['href']})
                elif type(child) == dict and child['tag'] == 'strong':
                    content_dict['tags'].append({'b': child['children'][0]})
        return content_dict


#pprint.pprint(Telegraph.getArticleContent('https://telegra.ph/hello-world-05-30'))


    