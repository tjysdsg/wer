INITIALS = ['b', 'c', 'ch', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 'sh', 't', 'w', 'x', 'y',
            'z', 'zh']

utt2trans = {}
f = open('data/aishell3.txt', encoding='utf-8')
with open('data/ref.txt', 'w') as of:
    for line in f:
        tokens = line.strip('\n').split()
        utt = tokens[0].split('.')[0]
        phones = tokens[2::2]
        # separate initials and finals
        utt2trans[utt] = []
        for p in phones:
            if p[:2] in INITIALS:
                utt2trans[utt].append(p[:2])
                final = p[2:]
            elif p[:1] in INITIALS:
                utt2trans[utt].append(p[:1])
                final = p[1:]
            else:
                final = p

            tone = final[-1]
            if tone == 'r':  # 儿化
                tone = 0
            else:
                tone = int(tone)
                final = final[:-1]

            if tone == 5:  # 轻声 5 -> 0
                tone = 0

            # 分离儿化
            if 'er' not in final and final[-1] == 'r':
                final = final[:-1]
                utt2trans[utt].append(f'{final}_{tone}')
                utt2trans[utt].append('er_0')
            else:
                utt2trans[utt].append(f'{final}_{tone}')

        s = ' '.join(utt2trans[utt])
        of.write(f'{utt}\t{s}\n')
