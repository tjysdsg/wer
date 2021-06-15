"""
Some of the utility functions copied from or based on
https://github.com/kaldi-asr/kaldi/blob/master/egs/gop_speechocean762/s5/local/utils.py
"""
import argparse
from utils import clean_phones
from metrics import wer_details_for_batch, wer_summary
from typing import Dict, List


def get_args():
    parser = argparse.ArgumentParser(
        description='Calculate ASE correlation between predicted scores and annotated scores')
    parser.add_argument('hyp', metavar='HYP', type=str, help='Hypothesis file')
    parser.add_argument('ref', metavar='REF', type=str, help='Reference file')
    parser.add_argument('--output-path', type=str, default='tmp/results.txt', help='Path to write results')
    args = parser.parse_args()
    return args


def get_wer_align(hyps: Dict[str, List[str]], refs: Dict[str, List[str]]) -> Dict:
    ref_list = []
    hyp_list = []
    utts = []
    for utt, h in hyps.items():
        utts.append(utt)
        hyp_list.append(h)
        ref_list.append(refs[utt])

    details = wer_details_for_batch(utts, ref_list, hyp_list, compute_alignments=True)

    # get utt -> wer alignments
    wer_align = {}
    for d in details:
        wer_align[d['key']] = d['alignment']

    return wer_align


def get_result_str(wer_align: List, hyp: List[str], ref: List[str], pred: List[float], label: List[float]) -> str:
    pred = [str(int(score)) for score in pred]
    label = [str(int(score)) for score in label]

    n = len(wer_align)
    lines = ['' for _ in range(4)]
    indices = [0 for _ in range(3)]
    for i in range(n):
        err = wer_align[i][0]
        if err == 'S' or err == '=':
            lines[0] += '\t' + hyp[indices[0]]
            lines[1] += '\t' + ref[indices[1]]
            lines[2] += '\t' + pred[indices[2]]
            lines[3] += '\t' + label[indices[2]]
            indices[0] += 1
            indices[1] += 1
            indices[2] += 1
        elif err == 'I':
            lines[0] += '\t' + hyp[indices[0]]
            lines[1] += '\t '
            lines[2] += '\t '
            lines[3] += '\t '
            indices[0] += 1
        elif err == 'D':
            lines[0] += '\t '
            lines[1] += '\t' + ref[indices[1]]
            lines[2] += '\t' + pred[indices[2]]
            lines[3] += '\t' + label[indices[2]]
            indices[1] += 1
            indices[2] += 1
        else:
            assert False

    return f'pred_phones:\t{lines[0]}\n' \
           f'true_phones:\t{lines[1]}\n' \
           f'pred_scores:\t{lines[2]}\n' \
           f'true_scores:\t{lines[3]}\n'


def main():
    args = get_args()

    hyp = {}
    with open(args.hyp, encoding='utf-8') as f:
        for line in f:
            tokens = line.strip('\n').split()
            utt = tokens[0]
            phones = tokens[1:]
            hyp[utt] = phones

    ref = {}
    with open(args.ref, encoding='utf-8') as f:
        for line in f:
            tokens = line.strip('\n').split()
            utt = tokens[0]
            phones = tokens[1:]
            if utt in hyp:
                ref[utt] = phones

    ref_list = []
    hyp_list = []
    utts = []
    for utt, h in hyp.items():
        if utt in ref:
            utts.append(utt)
            hyp_list.append(clean_phones(h))
            ref_list.append(clean_phones(ref[utt]))

    details = wer_details_for_batch(utts, ref_list, hyp_list, scoring_mode='present')

    print(wer_summary(details))

    # scores = predict_scores(utts, details)
    # preds, wer_align = get_wer_align(hyps, refs)
    # f = open(args.output_path, 'w')
    # hyp_scores = []
    # true_scores = []
    # for utt, s in preds.items():
    #     hyp_scores += s
    #     if utt in labels:
    #         true_scores += labels[utt]
    #         error_type = wer_align[utt]
    #         f.write(f'utt: {utt}\n')
    #         f.write(get_result_str(error_type, hyps[utt], refs[utt], preds[utt], labels[utt]))
    #     else:
    #         print(f'WARNING: Cannot find annotated score for {utt}')

    # f.close()


if __name__ == '__main__':
    main()
