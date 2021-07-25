import re

from arppl import models

_DEFAULT_RULE_SEPARATOR = ' => '
_COMPILED_PATTERN = re.compile('^(.*=.*),(.*=.*)$|^(.*=.*)$')


def convert_data_frame_to_rule_list(data_frame, rule_separator=_DEFAULT_RULE_SEPARATOR):
    data_frame.rules = data_frame.rules.str.replace('}', '', regex=False)
    data_frame.rules = data_frame.rules.str.replace('{', '', regex=False)

    data_frame[['antecedent', 'consequent']] = data_frame.rules.str.split(rule_separator, expand=True)

    return [create_rules_from_row(row) for _, row in data_frame.iterrows()]


def split_antecedent(antecedent):
    items = _COMPILED_PATTERN.search(antecedent)

    if items.group(2):
        return [items.group(1), items.group(2)]

    return [antecedent]


def create_rules_from_row(row):
    measures = {'support': models.Measure('support', row.support),
                'confidence': models.Measure('confidence', row.confidence),
                'lift': models.Lift(row.lift)}

    antecedent = split_antecedent(row.antecedent)

    return models.Rule(antecedent, row.consequent, measures)
