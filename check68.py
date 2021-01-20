


if __name__=='__main__':
    f =  open("./Noel_Test_Edited.txt", 'r')
    lines = f.readlines()

    break_idxs =  [i for i in range(len(lines)) if lines[i]=='\n']
    print(break_idxs)

    for idx in range(len(break_idxs)-1):
        break_line = break_idxs[idx]
        result = list()
        flag = True

        kho = lines[break_line+1: break_idxs[idx+1]]

        for even in range(0, len(kho), 2):
            if len(kho[even].split(' ')) !=6:
                flag = False
                break

        for odd in range(1, len(kho), 2):
            if len(kho[odd].split(' ')) !=8:
                flag = False
                break

        if flag:
            with open('./68poem_test.txt', 'a+') as file:
                for l in kho:
                    file.write(l)
                file.write('\n')



