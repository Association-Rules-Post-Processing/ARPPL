class Rule:
    __slots__ = ('antecedent', 'consequent', 'length', 'measures')

    def __init__(self, antecedent, consequent, measures):
        self.antecedent = antecedent
        self.consequent = consequent
        self.length = len(antecedent) + 1
        self.measures = measures

    def __eq__(self, other):
        return len(set(self.antecedent).difference(other.antecedent)) == 0 and self.consequent == other.consequent

    def get_key(self, index=0):
        return self.antecedent[index] + '&' + self.consequent

    def get_reverse_key(self, index=0):
        return self.consequent + '&' + self.antecedent[index]

    def contain_item(self, item):
        return item in self.antecedent or item == self.consequent

    def better_than(self, other, measure):
        return self.measures[measure].better_than(other.measures[measure])

    def to_string(self):
        return ','.join(self.antecedent) + ' => ' + self.consequent


class Measure:
    __slots__ = ('name', 'value')

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def is_relevant(self):
        return self.value > 0

    def better_than(self, other):
        return self.value > other.value

    def diff_value(self, other):
        return self.value - other.value


class Lift(Measure):
    __slots__ = ()

    def __init__(self, value):
        super().__init__('lift', value)

    def is_relevant(self):
        return self.value != 1

    def _values_represent_the_same_type_of_dependency(self, other_value):
        return self.value < 1 and other_value < 1 or self.value > 1 and other_value > 1

    def better_than(self, other):
        if not self._values_represent_the_same_type_of_dependency(other.value):
            ValueError('Values must be both greater than 1 or both smaller than 1.')
        return abs(1 - self.value) > abs(1 - other.value)

    def diff_value(self, other):
        if not self._values_represent_the_same_type_of_dependency(other.value):
            ValueError('Values must be both greater than 1 or both smaller than 1.')
        return abs(self.value - other.value)


class Group:
    __slots__ = ('name', 'rules')

    def __init__(self, name, rules):
        self.name = name
        self.rules = rules

    def contain_rule(self, rule):
        return rule in self.rules

    def to_string(self):
        return '\n'.join([r.to_string() for r in self.rules])
