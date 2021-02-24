import json
import os
import numpy as np


def split_poem(poem:str, poem_size:int):
    result = list()
    poem = poem.strip(' ')
    poem = poem.strip('\n')
    poem = poem.strip(' ')
    lines = poem.split('\n')
    lines = [l.strip('\n') for l in lines]
    lines = [(l.strip(' ')).strip('\n') for l in lines if l!='\n']
    num_lines = len(lines)
    start_range = range(0, num_lines, poem_size)

    if len(start_range) > 1:
        for i in start_range[:-1]:
            result.append('\n'.join(lines[i:i+poem_size]))

        res = lines[start_range[-1]: ]
        if len(res) >= 4:
            result.append('\n'.join(res))
    else:
        result.append('\n'.join(lines))

    return result

if __name__ == '__main__':
    file = open(os.path.join('../dataset', 'dataset_lucbat_v2.txt'), 'r')
    context = file.read()
    poems = context.split('\n\n')
    print (poems)

    num_poems = len(poems)
    valid_idxs = list(np.random.randint(0, num_poems, size=int(num_poems * 0.1)))
    train_idxs = [i for i in range(num_poems) if i not in valid_idxs]

    # Split one poem to some poems and write to json file
    f = open('../dataset/train_lucbat_v2.txt', 'w')
    train_dataset = list()
    count = 1
    for idx in train_idxs:
        splited_poems = split_poem(poems[idx], 8)

        for poem in splited_poems:
            data = poem
            data = data.replace("“", "")
            data = data.replace('"', "")
            data = data.replace(':', "")
            data = data.replace("”", "")
            data = data.replace(";", "")
            data = data.replace("’", "")
            data = data.replace("‘", "")
            data = data.replace("*", "")
            data = data.replace("(", "")
            data = data.replace(")", "")
            data = data.strip(' ')
            data = data.strip('\n')
            data = data.strip(' ')
            lines = data.split('\n')
            p = [line for line in lines if line != '\n']
            if len(p) >= 4:

                train_dataset.append({'id': count, 'content': '\n'.join(p), 'length': len(p)})
                count += 1
                f.write('\n'.join(p))
                f.write('\n\n')


    f.close()

    valid_dataset = list()
    count = 1
    f = open('../dataset/valid_lucbat_v2.txt', 'w')
    for idx in valid_idxs:
        splited_poems = split_poem(poems[idx], 8)

        for poem in splited_poems:
            data = poem
            data = data.replace("“", "")
            data = data.replace('"', "")
            data = data.replace(':', "")
            data = data.replace("”", "")
            data = data.replace(";", "")
            data = data.replace("’", "")
            data = data.replace("‘", "")
            data = data.replace("*", "")
            data = data.replace("(", "")
            data = data.replace(")", "")
            data = data.strip(' ')
            data = data.strip('\n')
            data = data.strip(' ')
            lines = data.split('\n')
            p = [line for line in lines if line != '\n']
            if len(p) >= 4:
                valid_dataset.append({'id': count, 'content': '\n'.join(p), 'length': len(p)})
                count += 1
                f.write('\n'.join(p))
                f.write('\n\n')


    f.close()

    with open('../dataset/train_lucbat_v2.json', 'w') as jfile:
        json_obj = json.dumps(train_dataset)
        jfile.write(json_obj)

    with open('../dataset/valid_lucbat_v2.json', 'w') as jfile:
        json_obj = json.dumps(valid_dataset)
        jfile.write(json_obj)