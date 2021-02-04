def check68(part: str):
    """
    check whether poem is luc bat and process poem
    :param part:
    :return: True/False, ""/processed_poem
    """
    part = part.strip('\n')
    lines = part.split('\n')
    num_lines = len(lines)
    if num_lines < 4:
        return False, ''

    first_line6 = -1
    # process each of line in poem
    for i in range(num_lines):
        lines[i] = ' '.join([word for word in lines[i].split(' ') if word != ''])

    for i in range(num_lines):
        line = lines[i]
        if len(line.split(' '))==6:
            first_line6 = i
            break

    if first_line6 == -1:
        return False, ''

    end = 0
    flag = False
    for i in range(first_line6, num_lines, 2):
        line1 = ' '.join([word for word in lines[i].split(' ') if word != ''])
        line2 = ' '.join([word for word in lines[min(i+1, num_lines-1)].split(' ') if word != ''])
        if len(line1.split(' ')) == 6 and len(line2.split(' ')) == 8:
            flag = True
            end = min(i+2, num_lines)
        else:
            break


    if flag == True and len(lines[first_line6:end]) >= 4:
        return True, '\n'.join(lines[first_line6:end])
    else:
        return False, ''

def check7(part:str):
    """
    check whether poem is tho 7 chu and process poem
    :param part:
    :return: True/False, ""/processed_poem
    """
    part = part.strip('\n')
    lines = part.split('\n')
    num_lines = len(lines)
    if num_lines < 4:
        return False, ''

    first_line7 = -1
    # process each of line in poem
    for i in range(num_lines):
        lines[i] = ' '.join([word for word in lines[i].split(' ') if word != ''])

    for i in range(num_lines):
        line = lines[i]
        if len(line.split(' '))==7:
            first_line7 = i
            break

    if first_line7 == -1:
        return False, ''

    end = 0
    flag = False
    for i in range(first_line7, num_lines, 2):
        line1 = ' '.join([word for word in lines[i].split(' ') if word != ''])
        line2 = ' '.join([word for word in lines[min(i+1, num_lines-1)].split(' ') if word != ''])
        if len(line1.split(' ')) == 7 and len(line2.split(' ')) == 7:
            flag = True
            end = min(i+2, num_lines)

        else:
            break

    if flag == True and len(lines[first_line7:end]) >= 4:
        return True, '\n'.join(lines[first_line7:end])
    else:
        return False, ''


def check5(part:str):
    """
    check whether poem is tho 5 chu and process poem
    :param part:
    :return: True/False, ""/processed_poem
    """
    part = part.strip('\n')
    lines = part.split('\n')
    num_lines = len(lines)
    if num_lines < 4:
        return False, ''

    first_line5 = -1
    # process each of line in poem
    for i in range(num_lines):
        lines[i] = ' '.join([word for word in lines[i].split(' ') if word != ''])

    for i in range(num_lines):
        line = lines[i]
        if len(line.split(' '))==5:
            first_line5 = i
            break

    if first_line5 == -1:
        return False, ''

    end = 0
    flag = False
    for i in range(first_line5, num_lines, 2):
        line1 = ' '.join([word for word in lines[i].split(' ') if word != ''])
        line2 = ' '.join([word for word in lines[min(i+1, num_lines-1)].split(' ') if word != ''])
        if len(line1.split(' ')) == 5 and len(line2.split(' ')) == 5:
            flag = True
            end = min(i+2, num_lines)
        else:
            break

    if flag == True and len(lines[first_line5:end]) >= 4:
        return True, '\n'.join(lines[first_line5:end])
    else:
        return False, ''


def check8(part:str):
    """
    check whether poem is tho 8 chu and process poem
    :param part:
    :return: True/False, ""/processed_poem
    """
    part = part.strip('\n')
    lines = part.split('\n')
    num_lines = len(lines)
    if num_lines < 4:
        return False, ''

    first_line8 = -1
    # process each of line in poem
    for i in range(num_lines):
        lines[i] = ' '.join([word for word in lines[i].split(' ') if word != ''])

    for i in range(num_lines):
        line = lines[i]
        if len(line.split(' '))==8:
            first_line8 = i
            break

    if first_line8 == -1:
        return False, ''

    end = 0
    flag = False
    for i in range(first_line8, num_lines, 2):
        line1 = ' '.join([word for word in lines[i].split(' ') if word != ''])
        line2 = ' '.join([word for word in lines[min(i+1, num_lines-1)].split(' ') if word != ''])
        if len(line1.split(' ')) == 8 and len(line2.split(' ')) == 8:
            flag = True
            end = min(i+2, num_lines)
        else:
            break

    if flag == True and len(lines[first_line8:end]) >= 4:
        return True, '\n'.join(lines[first_line8:end])
    else:
        return False, ''


def check4(part:str):
    """
    check whether poem is tho 5 chu and process poem
    :param part:
    :return: True/False, ""/processed_poem
    """
    part = part.strip('\n')
    lines = part.split('\n')
    num_lines = len(lines)
    if num_lines < 4:
        return False, ''

    first_line4 = -1
    # process each of line in poem
    for i in range(num_lines):
        lines[i] = ' '.join([word for word in lines[i].split(' ') if word != ''])

    for i in range(num_lines):
        line = lines[i]
        if len(line.split(' '))==4:
            first_line4 = i
            break

    if first_line4 == -1:
        return False, ''

    end = 0
    flag = False
    for i in range(first_line4, num_lines, 2):
        line1 = ' '.join([word for word in lines[i].split(' ') if word != ''])
        line2 = ' '.join([word for word in lines[min(i+1, num_lines-1)].split(' ') if word != ''])
        if len(line1.split(' ')) == 4 and len(line2.split(' ')) == 4:
            flag = True
            end = min(i+2, num_lines)
        else:
            break


    if flag == True and len(lines[first_line4:end]) >= 4:
        return True, '\n'.join(lines[first_line4:end])
    else:
        return False, ''
