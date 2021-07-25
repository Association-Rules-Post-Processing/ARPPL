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

    def contain_attribute(self, attribute):
        return attribute in self.antecedent or attribute == self.consequent

    def better_than(self, other, measure):
        return self.measures[measure].better_than(other.measures[measure])


class Measure:
    __slots__ = ('name', 'value')

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def is_relevant(self):
        return self.value > 0

    def better_than(self, other):
        return self.value > other.value


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


class Group:
    __slots__ = ('classification', 'name', 'rules')

    def __init__(self, classification, name, rules):
        self.classification = classification
        self.name = name
        self.rules = rules
