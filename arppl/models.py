import math
import re


class Rule:
    # https://www.rdocumentation.org/packages/arules/versions/1.6-8/topics/interestMeasure
    __slots__ = ('id',
                 'antecedent',
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
                 'kappa',
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
                 kappa=None,
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
        self.kappa = kappa
        self.id = 'R' + str(hash(self.to_string()))

    def __eq__(self, other):
        return len(set(self.antecedent).symmetric_difference(other.antecedent)) == 0 and \
               self.consequent == other.consequent

    def get_key(self, index=0):
        return self.antecedent[index] + '&' + self.consequent

    def get_reverse_key(self, index=0):
        return self.consequent + '&' + self.antecedent[index]

    def contain_item(self, item):
        return item in self.antecedent or item == self.consequent

    def get_gain_in_relation_to(self, other, measure):
        measure_ref = getattr(self, measure)
        other_measure_ref = getattr(other, measure)

        if not measure_ref or not other_measure_ref:
            ValueError('Measure not found')

        if math.isinf(other_measure_ref.value):
            return 0

        return (measure_ref.value - other_measure_ref.value) / other_measure_ref.value

    def measure_value_is_relevant(self, measure, relevance_range):
        measure_ref = getattr(self, measure)
        return measure_ref and measure_ref.is_relevant(relevance_range)

    def has_empty_value(self):
        _COMPILED_EMPTY_PATTERN = re.compile('^.*=(.*)$')

        return not _COMPILED_EMPTY_PATTERN.search(self.consequent).group(1) or any(
            [not _COMPILED_EMPTY_PATTERN.search(a).group(1) for a in self.antecedent])

    def get_measure_value(self, measure):
        measure_ref = getattr(self, measure)
        return measure_ref.value if measure_ref else None

    def to_string(self):
        return ','.join(self.antecedent) + ' => ' + self.consequent


class Measure:
    __slots__ = ('value', 'is_probability')

    def __init__(self, value, is_probability):
        self.value = value
        self.is_probability = is_probability

    def is_relevant(self, relevance_range):
        return self.value > 0 + relevance_range


class MeasureIndependentlyAtOne(Measure):
    __slots__ = ()

    def __init__(self, value, is_probability):
        super().__init__(value, is_probability)

    def is_relevant(self, relevance_range):
        return self.value > 1 + relevance_range


class MeasureIndependentlyAtHalf(Measure):
    __slots__ = ()

    def __init__(self, value, is_probability):
        super().__init__(value, is_probability)

    def is_relevant(self, relevance_range):
        return self.value > 0.5 + relevance_range


class Type:
    __slots__ = ('name', 'rules', 'id')

    def __init__(self, rules):
        rules.sort(key=lambda x: x.length)
        self.rules = rules
        self.name = self._get_name()
        self.id = self._generate_id()

    def __eq__(self, other):
        return self.name == other.name and all([self.contain_rule(r) for r in other.rules])

    def _get_name(self):
        return ''

    def _generate_id(self):
        return self._prefix() + str(hash(self.to_string()))

    def _prefix(self):
        return 'G'

    def contain_rule(self, rule):
        return rule in self.rules

    def to_string(self):
        return '\n'.join([r.to_string() for r in self.rules])


class TypeWithoutGain(Type):
    __slots__ = 'max_val'

    def __init__(self, rules, measure):
        super().__init__(rules)
        self.max_val = max([r.get_measure_value(measure) for r in rules])

    def __lt__(self, other):
        return self.max_val < other.max_val

    def __le__(self, other):
        return self.max_val <= other.max_val

    def __gt__(self, other):
        return self.max_val > other.max_val

    def __ge__(self, other):
        return self.max_val >= other.max_val


class TypeWithGain(Type):
    __slots__ = 'gain'

    def __init__(self, rules, gain):
        super().__init__(rules)
        self.gain = gain

    def __lt__(self, other):
        return self.gain < other.gain

    def __le__(self, other):
        return self.gain <= other.gain

    def __gt__(self, other):
        return self.gain > other.gain

    def __ge__(self, other):
        return self.gain >= other.gain


class Type1(TypeWithoutGain):

    def _get_name(self):
        return '1'

    def _prefix(self):
        return 'B'


class Type2(TypeWithGain):

    def _get_name(self):
        return '2'


class Type3(TypeWithGain):

    def _get_name(self):
        return '3'


class Type4(TypeWithGain):

    def _get_name(self):
        return '4'


class Type5(TypeWithoutGain):

    def _get_name(self):
        return '5'


class Type6(TypeWithGain):

    def _get_name(self):
        return '6'


class Type7(TypeWithGain):

    def _get_name(self):
        return '7'


class Type8(TypeWithoutGain):

    def _get_name(self):
        return '8'
