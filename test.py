import os
import psycopg2
import json


def process_raw(record):

    def process_to_list(record):
        content = record[0][1].split("<br/>")
        lines = list()
        for l in content:
            l = l.strip('["], ')
            l = l.strip("'")
            l = l.replace("\\r\\n", "")
            l = l.strip('- .,?!:')

            lines.append(l)

        return lines

    def remove_noise(poem):
        avg = 0
        res = list()
        for kho in poem:
            for line in kho:
                avg += len(line.split())

            try:
                avg = avg / len(kho)

                for line in kho:
                    if len(line.split()) < avg - 2:
                        continue
                    res.append(line)

            except Exception as e:
                continue

        return res

    def find_kho(lines):
        poem = []
        start = 0
        end = 0
        print(lines)
        for i in range(len(lines)):

            if lines[i] == '':
                end = i

                if (end - start) > 1 :
                    poem.append(lines[start:end])

                if start == end:
                    poem.append([line for line in lines if line != ''])
                    break

                start = end + 1

        return poem

    lines = process_to_list(record)
    poem = find_kho(lines)
    return remove_noise(poem)

if __name__ == '__main__':
    db_infor = {
        'user': 'pvhanh',
        'password': 'pvhanh',
        'host': '127.0.0.1',
        'port': '5432',
        'database': 'poem'
    }

    conn = psycopg2.connect(user=db_infor['user'], password=db_infor['password'],
                                           host=db_infor['host'], port=db_infor['port'],
                                           database=db_infor['database'])
    cursor = conn.cursor()
    sql = """SELECT * FROM poems2"""
    cursor.execute(sql)

    count = 0
    i = 0
    while i< 1000:
        record = cursor.fetchmany(1)
        if record == []:
            break
        res = process_raw(record)
        i +=1
        for line in res:
            # out= "\n".join(r)
            print(line)

            count = count + 1  if line != '\n' else count

        print("-"*10)

    print("Totol sentences: {}".format(count))

    cursor.close()
    conn.close()