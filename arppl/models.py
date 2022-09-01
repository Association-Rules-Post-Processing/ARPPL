class Rule:
    # https://www.rdocumentation.org/packages/arules/versions/1.6-8/topics/interestMeasure
    __slots__ = ('antecedent',
                 'consequent',
                 'length',
                 'support',
                 'confidence',
                 'lift',
                 'conviction',
                 'hyper_confidence',
                 'cosine',
                 'chi_square',
                 'coverage',
                 'doc',
                 'gini',
                 'hyper_lift',
                 'odds_ratio',
                 )

    def __init__(self,
                 antecedent,
                 consequent,
                 support=None,
                 confidence=None,
                 lift=None,
                 conviction=None,
                 hyper_confidence=None,
                 cosine=None,
                 chi_square=None,
                 coverage=None,
                 doc=None,
                 gini=None,
                 hyper_lift=None,
                 odds_ratio=None,
                 ):
        self.antecedent = antecedent
        self.consequent = consequent
        self.length = len(antecedent) + 1
        self.support = support
        self.confidence = confidence
        self.lift = lift
        self.conviction = conviction
        self.hyper_confidence = hyper_confidence
        self.cosine = cosine
        self.chi_square = chi_square
        self.coverage = coverage
        self.doc = doc
        self.gini = gini
        self.hyper_lift = hyper_lift
        self.odds_ratio = odds_ratio

    def __eq__(self, other):
        return len(set(self.antecedent).symmetric_difference(other.antecedent)) == 0 and \
               self.consequent == other.consequent

    def get_key(self, index=0):
        return self.antecedent[index] + '&' + self.consequent

    def get_reverse_key(self, index=0):
        return self.consequent + '&' + self.antecedent[index]

    def contain_item(self, item):
        return item in self.antecedent or item == self.consequent

    def better_than(self, other, measure, minimal_improvement):
        measure_ref = getattr(self, measure)
        other_measure_ref = getattr(other, measure)
        return measure_ref and other_measure_ref and measure_ref.better_than(other_measure_ref, minimal_improvement)

    def measure_value_is_relevant(self, measure, relevance_range):
        measure_ref = getattr(self, measure)
        return measure_ref and measure_ref.is_relevant(relevance_range)

    def to_string(self):
        return ','.join(self.antecedent) + ' => ' + self.consequent


class Measure:
    __slots__ = 'value'

    def __init__(self, value):
        self.value = value

    def is_relevant(self, relevance_range):
        return self.value > 0 + relevance_range

    def better_than(self, other, minimal_improvement):
        return (self.value - other.value)/other.value >= minimal_improvement


class MeasureIndependentlyAtOne(Measure):
    __slots__ = ()

    def __init__(self, value):
        super().__init__(value)

    def is_relevant(self, relevance_range):
        return self.value > 1 + relevance_range


class Group:
    __slots__ = ('name', 'rules')

    def __init__(self, name, rules):
        self.name = name
        self.rules = rules

    def __eq__(self, other):
        return self.name == other.name and all([self.contain_rule(r) for r in other.rules])

    def contain_rule(self, rule):
        return rule in self.rules

    def to_string(self):
        return '\n'.join([r.to_string() for r in self.rules])
