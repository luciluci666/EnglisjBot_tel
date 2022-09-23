import requests
from bs4 import BeautifulSoup

from models import connect_db, Topic, Word, Phrase


class Parse:

    def create_topic(self, session, name, desc=""):
        if session.query(Topic).filter(Topic.name == name).first() is None:
            topic = Topic(
            name = name,
            desc = desc
            )
            session.add(topic)
            session.commit()

            return session.query(Topic).filter(Topic.name == name).one_or_none().id

        else:
            print(f'Words with "{name}" topic were already dumped.')
            return False

    def dump_db(self, session, data, type='word', topic_id=1):
        if type == 'word':
            row = Word(
                word = data['word'],
                translation = data['trans'],
                topic_id = topic_id
            )
        elif type == 'phrase':
            row = Phrase(
                word = data['phrase'],
                translation = data['trans'],
                topic_id = topic_id
            )
        else:
            return print('Data type is invalid!')

        session.add(row)
        session.commit()

        

   
    def words_5000(self):
        request = requests.get('https://studynow.ru/dicta/allwords')

        if request.status_code == 200:
            soap = BeautifulSoup(request.content, 'html.parser')
            word_list = soap.find(id="wordlist").find_all('td')

            i = 0    
            database = connect_db()     
            topic_id = self.create_topic(database, '5000 must have words', 'Here are collected a lot of useful English words for every day.') 
            if not topic_id:
                return
            for word_data in word_list:
                i += 1
                if i == 1:
                    pass
                if i == 2:
                    word = word_data.text
                if i == 3:
                    trans = word_data.text
                    i = 0

                    data ={
                        'word' : word,
                        'trans' : trans,
                    }

                    self.dump_db(database, data, topic_id=topic_id)
        else:
            return print('This url is invalid!')

        database.close()

        return print('Data dump success! (5000 common words)')


    def theme_words(self):
        request = requests.get('https://reallanguage.club/anglijskie-slova-po-temam/')

        if request.status_code == 200:
            soap = BeautifulSoup(request.content, 'html.parser')
            theme_list = soap.find(class_="text__main").find('table').find_all('a', href=True)
            themes = []
            for a in theme_list:
                themes.append({
                    "name" : a.text,
                    "href" : a["href"]
                })

            for theme in themes:
                database = connect_db()     

                topic_id = self.create_topic(database, theme['name'], desc='Небольшие тематические коллекции слов.')
                if not topic_id:
                    continue

                request = requests.get(theme['href'])
                soap = BeautifulSoup(request.content, 'html.parser')
                tables = soap.find(class_="text__main").find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    words = []
                    for row in rows:
                        i = 0
                        tds = row.find_all('td')
                        for td in tds:
                            i += 1
                            if i == 1:
                                word = td.find('strong').text
                            if i == 3:
                                trans = td.find('span').text
                                i = 0

                        data ={
                            'word' : word,
                            'trans' : trans,
                        }
                        self.dump_db(database, data, topic_id=topic_id)
                print(f"Words with '{theme['name']}' topic were dumped!")

        else:
            return print('This url is invalid!')

        return print('Data dump success!')



    def main(self):
        self.words_5000()
        self.theme_words()


if __name__ == '__main__':
    Parse().main()