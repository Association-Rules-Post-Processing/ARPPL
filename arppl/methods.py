from arppl.models import Group


def method_select(item_of_interest, rules, measure, minimal_improvement=0.001, relevance_range=0):
    rules = remove_irrelevant_rules(rules, measure, relevance_range)

    return group_only_relevant_rules_by_subset(item_of_interest, rules, measure, minimal_improvement)


def remove_irrelevant_rules(rules, measure, relevance_range):
    if not rules:
        ValueError('Rule list is empty')

    return [rule for rule in rules if rule.measure_value_is_relevant(measure, relevance_range)]


def group_only_relevant_rules_by_subset(item_of_interest, rules, measure, minimal_improvement):
    parents = {rule.get_key(): rule for rule in rules if rule.length == 2}
    three_length_rules = [rule for rule in rules if rule.length == 3 and rule.contain_item(item_of_interest)]

    return (get_groups_for_three_length_rules(item_of_interest, measure, parents, three_length_rules,
                                              minimal_improvement) +
            get_groups_for_two_length_rules(item_of_interest, parents))


def get_groups_for_two_length_rules(item_of_interest, map_of_rules):
    rules = dict(filter(lambda r: r[1].consequent == item_of_interest, map_of_rules.items()))

    return [Group('1', [rule, map_of_rules[rule.get_reverse_key()]])
            for rule in rules.values() if map_of_rules.get(rule.get_reverse_key())]


def get_groups_for_three_length_rules(item_of_interest, measure, parents, three_length_rules, minimal_improvement):
    return [_get_group_for_three_length_rule(rule, parents, item_of_interest)
            for rule in three_length_rules if _rule_can_be_in_a_group(rule, parents, measure, minimal_improvement)]


def _rule_can_be_in_a_group(rule, parents, measure, minimal_improvement):
    first_parent = parents.get(rule.get_key())
    second_parent = parents.get(rule.get_key(1))

    return _is_there_any_gain_in_keeping_rule_less_general(
        rule, first_parent, second_parent, measure, minimal_improvement)


def _is_there_any_gain_in_keeping_rule_less_general(rule, first_parent, second_parent, measure, minimal_improvement):
    return ((not first_parent or rule.better_than(first_parent, measure, minimal_improvement)) and
            (not second_parent or rule.better_than(second_parent, measure, minimal_improvement)))


def _get_group_for_three_length_rule(rule, parents, item_of_interest):
    first_parent = parents.get(rule.get_key())
    second_parent = parents.get(rule.get_key(1))
    group = None
    if rule.consequent == item_of_interest:
        if second_parent and first_parent:
            group = Group('6', [first_parent, second_parent, rule])
        elif second_parent or first_parent:
            existing_parent = first_parent if first_parent else second_parent
            group = Group('7', [existing_parent, rule])
        else:
            group = Group('8', [rule])
    else:
        if first_parent and second_parent:
            group = Group('2', [first_parent, second_parent, rule])
        elif second_parent or first_parent:
            existing_parent = first_parent if first_parent else second_parent
            if existing_parent.antecedent[0] != item_of_interest:
                group = Group('3', [rule, existing_parent])
            else:
                group = Group('4', [rule, existing_parent])
        else:
            group = Group('5', [rule])
    return group
