import re
import xlsxwriter
from itertools import groupby
import math
import string

from arppl import models

_DEFAULT_RULE_SEPARATOR = ' => '
_COMPILED_PATTERN = re.compile('^(.*=.*),(.*=.*)$|^(.*=.*)$')
_COMPILED_BOOLEAN_PATTERN = re.compile('^(.*),(.*)$|^(.*)$')
_MEASURE_DESCRIPTION = {
    'support': 'Support',
    'confidence': 'Confidence',
    'lift': 'Lift',
    'conviction': 'Conviction',
    'hyper_confidence': 'Hyper-Confidence',
    'cosine': 'Cosine',
    'chi_square': 'Chi-Square',
    'coverage': 'Coverage',
    'doc': 'Doc',
    'gini': 'Gini',
    'hyper_lift': 'Hyper-Lift',
    'odds_ratio': 'Odds Ratio',
    'kappa': 'Kappa',
}


def convert_data_frame_to_rule_list(data_frame, rule_separator=_DEFAULT_RULE_SEPARATOR):
    data_frame.rules = data_frame.rules.str.replace('}', '', regex=False)
    data_frame.rules = data_frame.rules.str.replace('{', '', regex=False)

    data_frame[['antecedent', 'consequent']] = data_frame.rules.str.split(rule_separator, expand=True)

    return [create_rules_from_row(row) for _, row in data_frame.iterrows()]


def split_antecedent(antecedent):
    items = _COMPILED_PATTERN.search(antecedent)

    if not items:
        items = _COMPILED_BOOLEAN_PATTERN.search(antecedent)

    if items.group(2):
        return [items.group(1), items.group(2)]

    return [antecedent]


def create_rules_from_row(row):
    antecedent = split_antecedent(row.antecedent)

    return models.Rule(
        antecedent=antecedent,
        consequent=row.consequent,
        support=_get_treated_measure_value_from_row(row=row, column='support', is_probability=True,
                                                    measure_class=models.Measure),
        confidence=_get_treated_measure_value_from_row(row=row, column='confidence', is_probability=True,
                                                       measure_class=models.Measure),
        lift=_get_treated_measure_value_from_row(row=row, column='lift', is_probability=False,
                                                 measure_class=models.MeasureIndependentlyAtOne),
        conviction=_get_treated_measure_value_from_row(row=row, column='conviction', is_probability=False,
                                                       measure_class=models.MeasureIndependentlyAtOne),
        hyper_confidence=_get_treated_measure_value_from_row(row=row, column='hyperConfidence', is_probability=True,
                                                             measure_class=models.Measure),
        cosine=_get_treated_measure_value_from_row(row=row, column='cosine', is_probability=False,
                                                   measure_class=models.MeasureIndependentlyAtHalf),
        chi_square=_get_treated_measure_value_from_row(row=row, column='chiSquare', is_probability=False,
                                                       measure_class=models.Measure),
        coverage=_get_treated_measure_value_from_row(row=row, column='coverage', is_probability=False,
                                                     measure_class=models.Measure),
        doc=_get_treated_measure_value_from_row(row=row, column='doc', is_probability=False,
                                                measure_class=models.Measure),
        gini=_get_treated_measure_value_from_row(row=row, column='gini', is_probability=False,
                                                 measure_class=models.Measure),
        hyper_lift=_get_treated_measure_value_from_row(row=row, column='hyperLift', is_probability=False,
                                                       measure_class=models.MeasureIndependentlyAtOne),
        odds_ratio=_get_treated_measure_value_from_row(row=row, column='oddsRatio', is_probability=False,
                                                       measure_class=models.MeasureIndependentlyAtOne),
        kappa=_get_treated_measure_value_from_row(row=row, column='kappa', is_probability=False,
                                                  measure_class=models.Measure)
    )


def _get_treated_measure_value_from_row(row, column, is_probability, measure_class):
    value = None
    if column in row:
        value = row[column]

    if not value or math.isnan(value):
        return None
    elif math.isinf(value):
        return measure_class(math.inf, is_probability)
    else:
        return measure_class(value, is_probability)


def export_groups_to_xlsx(directory, filename, groups, measures, interest_measure):
    workbook = xlsxwriter.Workbook(directory + filename)

    sorted_groups = sorted(groups, key=lambda x: x.name)
    groups_by_name = groupby(sorted_groups, key=lambda x: x.name)

    for key, gps in groups_by_name:
        groups_as_list = list(gps)
        sorted_gps = sorted(groups_as_list)

        worksheet = workbook.add_worksheet('Grupo ' + key)
        # Total
        worksheet.write('A1', 'Total')
        worksheet.write('B1', len(groups_as_list))

        # Headers
        headers = _get_headers(measures=measures, interest_measure=interest_measure, group=key)
        prefixes = string.ascii_uppercase[:len(headers)]
        _write_headers(headers=headers, prefixes=prefixes, worksheet=worksheet)

        i = 3
        for g in sorted_gps:
            for r in g.rules:
                _write_values_in_xlsx(row=str(i), rule=r, sorted_fields=list(headers.keys()), group=g,
                                      prefixes=prefixes, worksheet=worksheet)
                i += 1
            i += 1
    workbook.close()


def _get_headers(measures, interest_measure, group):
    headers = {'rule': 'Rule'}

    if group in ['2', '3', '4', '6', '7']:
        headers['gain'] = 'Gain'

    headers[interest_measure] = _MEASURE_DESCRIPTION[interest_measure]

    for m in measures:
        if m != interest_measure:
            headers[m] = _MEASURE_DESCRIPTION[m]

    return headers


def _write_headers(headers, prefixes, worksheet):
    headers_values = list(headers.values())
    for i, prefix in enumerate(prefixes):
        worksheet.write(prefix + '2', headers_values[i])


def _write_values_in_xlsx(row, group, rule, sorted_fields, prefixes, worksheet):
    for i, prefix in enumerate(prefixes):
        cell = prefix + row
        field = sorted_fields[i]
        if field == 'rule':
            worksheet.write(cell, rule.to_string())
        elif field == 'gain':
            value = getattr(group, field)
            _write_value_in_xlsx(cell=cell, value=value, worksheet=worksheet, is_probability=True)
        else:
            measure = getattr(rule, field)
            _write_measure_value_in_xlsx(cell=cell, measure=measure, worksheet=worksheet,
                                         is_probability=measure.is_probability)


def _write_measure_value_in_xlsx(cell, measure, worksheet, is_probability=False):
    if measure:
        _write_value_in_xlsx(cell=cell, value=measure.value, worksheet=worksheet, is_probability=is_probability)
    else:
        worksheet.write(cell, '')


def _write_value_in_xlsx(cell, value, worksheet, is_probability=False):
    if value:
        worksheet.write(cell, _get_value_for_xlsx(value, is_probability))
    else:
        worksheet.write(cell, '')


def _get_value_for_xlsx(value, is_probability):
    if math.isinf(value):
        return 'Inf'
    elif math.isnan(value):
        return 'NaN'
    elif is_probability:
        return str(round((value * 100), 2)) + '%'
    else:
        return round(value, 3)
