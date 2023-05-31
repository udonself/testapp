from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from telegraph import Telegraph
from models import TrustDB


db = TrustDB('db.db')


class Article(Resource):
    def get(self, url: str):
        article = Telegraph.getArticleContent(url)
        if article:
            return article, 200
        return "article not found", 404

db.getTopArticles()


class TopArticles(Resource):
    def get(self):
        articles = {
            "articles": []
        }
        for article in db.getTopArticles():
            articles['articles'].append(
                {
                    'title': article[0],     
                    'image': article[1],
                    'telegraphUrl': article[2]
                }
            )
        return articles, 200


class AddArticle(Resource):
    def post(self, title: str, base64image: str, telegraphUrl: str):
        succesful_add = db.addArticle(title, base64image, telegraphUrl)
        if succesful_add:
            return 'Article was succesfully added', 200
        return 'Article with such telegraph url already exist', 400
        

def main() -> None:
    app = Flask(__name__)
    CORS(app)
    api = Api(app)
    api.add_resource(Article, '/article/<url>')
    api.add_resource(TopArticles, '/top_articles')
    api.add_resource(AddArticle, '/add_article/<title>/<base64image>/<telegraphUrl>')
    app.run(host='0.0.0.0')
    

if __name__ == '__main__':
    main()