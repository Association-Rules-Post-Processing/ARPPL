import math
from arppl.models import Type1
from arppl.models import Type2
from arppl.models import Type3
from arppl.models import Type4
from arppl.models import Type5
from arppl.models import Type6
from arppl.models import Type7
from arppl.models import Type8


def method_select(item_of_interest, rules, measure, minimal_improvement=0.001, relevance_range=0,
                  allow_empty_items=False):
    if not allow_empty_items:
        rules = remove_rules_with_empty_items(rules)

    rules = remove_irrelevant_rules(rules, measure, relevance_range)

    return group_only_relevant_rules_by_subset(item_of_interest, rules, measure, minimal_improvement)


def remove_rules_with_empty_items(rules):
    return [rule for rule in rules if not rule.has_empty_value()]


def remove_irrelevant_rules(rules, measure, relevance_range):
    if not rules:
        ValueError('Rule list is empty')

    return [rule for rule in rules if rule.measure_value_is_relevant(measure, relevance_range)]


def group_only_relevant_rules_by_subset(item_of_interest, rules, measure, minimal_improvement):
    parents = {rule.get_key(): rule for rule in rules if rule.length == 2}
    three_length_rules = [rule for rule in rules if rule.length == 3 and rule.contain_item(item_of_interest)]

    return (get_groups_for_three_length_rules(item_of_interest, measure, parents, three_length_rules,
                                              minimal_improvement) +
            get_groups_for_two_length_rules(item_of_interest, parents, measure))


def get_groups_for_two_length_rules(item_of_interest, map_of_rules, measure) -> list:
    rules = dict(filter(lambda r: r[1].consequent == item_of_interest, map_of_rules.items()))

    return [Type1(rules=[rule, map_of_rules[rule.get_reverse_key()]], measure=measure)
            for rule in rules.values() if map_of_rules.get(rule.get_reverse_key())]


def get_groups_for_three_length_rules(item_of_interest, measure, parents, three_length_rules,
                                      minimal_improvement) -> list:
    return [group for group in
            map(lambda r: _get_group_for_three_length_rule(r, parents, item_of_interest, measure, minimal_improvement),
                three_length_rules) if group is not None]


def _get_the_gain_of_the_less_general_rule(rule, first_parent, second_parent, measure):
    gain_first = rule.get_gain_in_relation_to(first_parent, measure) if first_parent else None
    gain_second = rule.get_gain_in_relation_to(second_parent, measure) if second_parent else None

    if gain_first is not None and gain_second is not None:
        return gain_first if gain_first < gain_second else gain_second
    elif gain_first is not None:
        return gain_first
    elif gain_second is not None:
        return gain_second
    else:
        return None


def _get_group_for_three_length_rule(rule, parents, item_of_interest, measure, minimal_improvement):
    first_parent = parents.get(rule.get_key())
    second_parent = parents.get(rule.get_key(1))
    gain = _get_the_gain_of_the_less_general_rule(rule, first_parent, second_parent, measure)

    if gain is not None and (math.isnan(gain) or gain < minimal_improvement):
        return None

    group = None
    if rule.consequent == item_of_interest:
        if second_parent and first_parent:
            group = Type6(rules=[first_parent, second_parent, rule], gain=gain)
        elif second_parent or first_parent:
            existing_parent = first_parent if first_parent else second_parent
            group = Type7(rules=[existing_parent, rule], gain=gain)
        else:
            group = Type8(rules=[rule], measure=measure)
    else:
        if first_parent and second_parent:
            group = Type2(rules=[first_parent, second_parent, rule], gain=gain)
        elif second_parent or first_parent:
            existing_parent = first_parent if first_parent else second_parent
            if existing_parent.antecedent[0] != item_of_interest:
                group = Type3(rules=[rule, existing_parent], gain=gain)
            else:
                group = Type4(rules=[rule, existing_parent], gain=gain)
        else:
            group = Type5(rules=[rule], measure=measure)
    return group
