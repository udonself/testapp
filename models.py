import sqlite3


class TrustDB:
    def __init__(self, path: str) -> None:
        self.path = path
        for query in [
            'CREATE TABLE IF NOT EXISTS Article(article_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, base64image TEXT, telegraphUrl TEXT)'    
        ]: self.executeNonQuery(query)

    def executeNonQuery(self, query: str, args: tuple = None) -> None:
        self.conn = sqlite3.connect(self.path)
        cur = self.conn.cursor()
        if args:
            cur.execute(query, args)
        else:
            cur.execute(query)
        self.conn.commit()
        cur.close()
        self.conn.close()

    def isArticleExists(self, telegraphUrl: str) -> bool:
        self.conn = sqlite3.connect(self.path)
        cur = self.conn.cursor()
        result = cur.execute('SELECT COUNT(article_id) FROM Article WHERE telegraphUrl=?', (telegraphUrl,))
        articleExist = result.fetchone()[0] > 0
        cur.close()
        self.conn.close()
        return articleExist

    def addArticle(self, title: str, base64image: str, telegraphUrl: str) -> bool:
        telegraphUrl = telegraphUrl.split('/')[-1] if '/' in telegraphUrl else telegraphUrl
        if self.isArticleExists(telegraphUrl):
            return False
        self.executeNonQuery('INSERT INTO Article (title, base64image, telegraphUrl) VALUES (?, ?, ?)', (title, base64image, telegraphUrl))
        return True

    def getTopArticles(self, limit=3) -> list:
        self.conn = sqlite3.connect(self.path)
        cur = self.conn.cursor()
        result = cur.execute('SELECT title, base64image, telegraphUrl FROM Article LIMIT 3')
        topArticles = result.fetchall()
        cur.close()
        self.conn.close()
        return topArticles

