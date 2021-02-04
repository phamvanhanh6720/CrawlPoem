import psycopg2
import os
from psycopg2 import Error
import re
import check_type

class Connection:
    def __init__(self):
        self.db_infor = {
            'user': 'pvhanh',
            'password': 'pvhanh',
            'host': '127.0.0.1',
            'port': '5432',
            'database': 'poem'
        }

        try:
            self.connection = psycopg2.connect(user=self.db_infor['user'], password=self.db_infor['password'],
                                           host=self.db_infor['host'], port=self.db_infor['port'],
                                           database=self.db_infor['database'])
        except (Exception, Error) as error:
            print("Error while connecting to PostGreSql", error)

    def insert(self, sql, values:tuple):
        """
        Insert to processed_poems table
        :param sql: query
        :param values:tuple of (content, url)
        :return: None
        """
        c = self.connection.cursor()
        c.execute(sql, values)
        self.connection.commit()
        c.close()
        print("Store content")


def remove_speical_character(text: str):
    lines = text.split('<br/>')
    poems = list()

    for l in lines:
        s = l.replace("\\r", "")
        s = s.replace("\\n", "")
        s = s.replace("[", "")
        s = s.replace("]", "")
        s = re.sub('[;:!/",*)@#%(&$_?.^\>]', '', s)
        s = re.sub('[-]', ' ', s)
        s = s.replace('…', ' ')
        s = s.replace("'", "")
        s = s.strip()
        s = ' '.join([word for word in s.split(' ') if word != ''])
        s= s.lower()
        poems.append(s)

    return '\n'.join(poems)


def concatnate(parts:list):
    poems = list()
    flag = False
    for part in parts:
        part = part.strip('\n')
        part = ' '.join([word for word in part.split(' ') if word != ''])
        num_words = len(part)

        if num_words in [4,5,6,7,8]:
            poems.append(part)
            flag = True

    return ['\n'.join(poems)] if flag else ''


if __name__ == '__main__':
    conector = Connection()
    cursor = conector.connection.cursor()

    table = 'poems2'
    query = "SELECT * FROM {}".format(table)

    cursor.execute(query)
    record = cursor.fetchmany(1)
    while record != []:
    # for i in range(100):

        data = remove_speical_character(record[0][1])
        parts = data.split('\n\n')

        if concatnate(parts) != '':
            poem = concatnate(parts)
        else:
            poem = parts

        processed_poem = list()
        for p in parts:
            # check 7
            check, content = check_type.check7(p)
            if check == True:
                processed_poem.append(content)
                continue

            # check 68
            check, content = check_type.check68(p)
            if check == True:
                processed_poem.append(content)
                continue

            # check 8
            check, content = check_type.check8(p)
            if check == True:
                processed_poem.append(content)
                continue

            # check 5
            check, content = check_type.check5(p)
            if check == True:
                processed_poem.append(content)
                continue

            # check 4
            check, content = check_type.check4(p)
            if check == True:
                processed_poem.append(content)
                continue

        if len(processed_poem) != 0:
            url = record[0][2]
            content = '\n\n'.join(processed_poem)

            sql = """INSERT INTO processed_poems(content, url) VALUES(%s, %s) """

            conector.insert(sql, values=(content, url))

        record = cursor.fetchmany(1)

    cursor.close()
    conector.connection.close()




