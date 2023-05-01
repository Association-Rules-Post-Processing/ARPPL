import re
import xlsxwriter
from itertools import groupby
import math

from arppl import models

_DEFAULT_RULE_SEPARATOR = ' => '
_COMPILED_PATTERN = re.compile('^(.*=.*),(.*=.*)$|^(.*=.*)$')
_COMPILED_BOOLEAN_PATTERN = re.compile('^(.*),(.*)$|^(.*)$')


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
        antecedent,
        row.consequent,
        _get_treated_measure_value_from_row(row.support, models.Measure),
        _get_treated_measure_value_from_row(row.confidence, models.Measure),
        _get_treated_measure_value_from_row(row.lift, models.MeasureIndependentlyAtOne),
        _get_treated_measure_value_from_row(row.conviction, models.MeasureIndependentlyAtOne),
        _get_treated_measure_value_from_row(row.hyperConfidence, models.Measure),
        _get_treated_measure_value_from_row(row.cosine, models.MeasureIndependentlyAtHalf),
        _get_treated_measure_value_from_row(row.chiSquare, models.Measure),
        _get_treated_measure_value_from_row(row.coverage, models.Measure),
        _get_treated_measure_value_from_row(row.doc, models.Measure),
        _get_treated_measure_value_from_row(row.gini, models.Measure),
        _get_treated_measure_value_from_row(row.hyperLift, models.MeasureIndependentlyAtOne),
        _get_treated_measure_value_from_row(row.oddsRatio, models.MeasureIndependentlyAtOne),
        _get_treated_measure_value_from_row(row.kappa, models.Measure)
    )


def _get_treated_measure_value_from_row(value, measure_class):
    if math.isnan(value):
        return None
    elif math.isinf(value):
        return measure_class(math.inf)
    else:
        return measure_class(value)


def export_groups_to_xlsx(directory, filename, groups):
    workbook = xlsxwriter.Workbook(directory + filename)

    sorted_groups = sorted(groups, key=lambda x: x.name)
    groups_by_name = groupby(sorted_groups, key=lambda x: x.name)

    for key, gps in groups_by_name:
        worksheet = workbook.add_worksheet('Grupo ' + key)
        worksheet.write('A1', 'Regras')
        worksheet.write('B1', 'Suporte')
        worksheet.write('C1', 'Confiança')
        worksheet.write('D1', 'Lift')
        worksheet.write('E1', 'Convicção')
        worksheet.write('F1', 'Hiper Confiança')
        worksheet.write('G1', 'Cosseno')
        worksheet.write('H1', 'X²')
        worksheet.write('I1', 'Cobertura')
        worksheet.write('J1', 'Doc')
        worksheet.write('K1', 'Gini')
        worksheet.write('L1', 'Hiper Lift')
        worksheet.write('M1', 'Odds Ratio')
        worksheet.write('N1', 'Kappa')

        i = 2
        for group in gps:
            for r in group.rules:
                worksheet.write('A' + str(i), r.to_string())
                _write_value_in_xlsx('B' + str(i), r.support.value, worksheet)
                _write_value_in_xlsx('C' + str(i), r.confidence.value, worksheet)
                _write_value_in_xlsx('D' + str(i), r.lift.value, worksheet)
                _write_value_in_xlsx('E' + str(i), r.conviction.value, worksheet)
                _write_value_in_xlsx('F' + str(i), r.hyper_confidence.value, worksheet)
                _write_value_in_xlsx('G' + str(i), r.cosine.value, worksheet)
                _write_value_in_xlsx('H' + str(i), r.chi_square.value, worksheet)
                _write_value_in_xlsx('I' + str(i), r.coverage.value, worksheet)
                _write_value_in_xlsx('J' + str(i), r.doc.value, worksheet)
                _write_value_in_xlsx('K' + str(i), r.gini.value, worksheet)
                _write_value_in_xlsx('L' + str(i), r.hyper_lift.value, worksheet)
                _write_value_in_xlsx('M' + str(i), r.odds_ratio.value, worksheet)
                _write_value_in_xlsx('N' + str(i), r.kappa.value, worksheet)
                i += 1
            i += 1
    workbook.close()


def _write_value_in_xlsx(cell, value, worksheet):
    if value:
        worksheet.write(cell, 'Inf' if math.isinf(value) else value)
