# confmat.py
class BinaryConfusionMatrix:
    def __init__(self, pos_tag, neg_tag):
        self.pos_tag = pos_tag
        self.neg_tag = neg_tag
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0

    def as_dict(self):
        return {'tp': self.tp, 'tn': self.tn, 'fp': self.fp, 'fn': self.fn}

    def update(self, truth, prediction):
        if truth not in [self.pos_tag, self.neg_tag] or prediction not in [self.pos_tag, self.neg_tag]:
            raise ValueError("Invalid truth or prediction value.")
        
        if truth == self.pos_tag and prediction == self.pos_tag:
            self.tp += 1
        elif truth == self.neg_tag and prediction == self.neg_tag:
            self.tn += 1
        elif truth == self.neg_tag and prediction == self.pos_tag:
            self.fp += 1
        elif truth == self.pos_tag and prediction == self.neg_tag:
            self.fn += 1

    def compute_from_dicts(self, truth_dict, pred_dict):
        for key in truth_dict.keys():
            truth = truth_dict[key]
            prediction = pred_dict[key]
            self.update(truth, prediction)