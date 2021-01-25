import os


if __name__ == '__main__':
    file = open('tho_lucbat_clean (1).txt', 'r')

    lines = file.readlines()
    poems = []

    keywords = ['tết', 'mùa xuân', 'hoa đào', 'hoa mai', 'bánh chưng', 'bánh giò', 'hoa nở', 'mừng xuân'
                'sang xuân', 'xuân sang','câu đối', 'an khang', 'thịnh vượng', 'mừng thọ', 'cầu chúc','cung kính',
                'chúc mừng', 'phát tài', 'phát lộc', 'công danh', 'bình an', 'tài lộc', 'giao thừa', 'mưa xuân', 'cây quất'
                ,'tết nguyên đán','năm mới', 'đâm chồi', 'nảy lộc']

    keywords_tet =['tết','mùa xuân' 'hoa đào', 'hoa mai', 'bánh chưng', 'bánh giò', 'mừng xuân'
                'sang xuân', 'xuân sang','câu đối', 'an khang', 'thịnh vượng', 'mừng thọ', 'cầu chúc','cung kính',
                'chúc mừng năm', 'phát tài', 'phát lộc', 'công danh', 'bình an', 'tài lộc', 'giao thừa', 'mưa xuân', 'cây quất'
                ,'tết nguyên đán','năm mới', 'đâm chồi', 'nảy lộc']

    start = 0
    end = 0
    for i in range(len(lines)):

        if lines[i] == '\n':
            end = i
            poems.append(lines[start:end])
            start = i+1

    with open('./tho_lucbat_tet_xuan_v3.txt', 'w') as f:
        for p in poems:
            str = "".join(p)
            count = 0
            for key in keywords:
                if str.find(key) != -1:
                    count+=1

            if count >= 1:
                f.write(str)
                f.write("\n")