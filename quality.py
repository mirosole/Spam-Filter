# quality.py
import os
from confmat import BinaryConfusionMatrix
from utils import read_classification_from_file

def quality_score(tp, tn, fp, fn):
    accuracy = (tp + tn) / (tp + tn + (10 * fp) + fn)
    return accuracy

def compute_quality_for_corpus(corpus_dir):
    truth_path = os.path.join(corpus_dir, '!truth.txt')
    pred_path = os.path.join(corpus_dir, '!prediction.txt')

    truth_dict = read_classification_from_file(truth_path)
    pred_dict = read_classification_from_file(pred_path)

    matrix = BinaryConfusionMatrix(pos_tag='SPAM', neg_tag='OK')
    matrix.compute_from_dicts(truth_dict, pred_dict)

    return quality_score(matrix.tp, matrix.tn, matrix.fp, matrix.fn)
