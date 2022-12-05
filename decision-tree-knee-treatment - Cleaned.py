from utility_new import case_between_5_10, case_lessthan_5, case_morethan_10
import pandas as pd
import argparse


def decision_tree(data):
    path = 'Cerebral Palsy -> Age Encounter'
    encounter_age = int(data["EncountersAge"])
    if encounter_age < 5:
        path += ' -> Age < 5'
        print("encounter_age < 5")
        return case_lessthan_5(data, path)
    elif encounter_age > 10:
        path += ' -> Age > 10'
        print("encounter_age > 10")
        return case_morethan_10(data, path)
    else:
        path += ' -> 5 <= Age <= 10'
        print("encounter_age between 5 & 10")
        return case_between_5_10(data, path)


def process_data(filename):
    df = pd.read_csv(filename)
    path = []
    treatment = []
    for index, row in df.iterrows():
        caseid = row['RRN']
        print(f'***Analysing CASE: {caseid}***')
        p, t = decision_tree(row)
        print('Path = ' + p)
        print('Treatment = ' + t)
        path.append(p)
        treatment.append(t)
        print(f'***Finished with CASE: {caseid}***')
        print('=======================================================================================================')
    df['Treatment'] = treatment
    df['Path'] = path
    df.to_excel("output.xlsx")


if __name__ == "__main__":
    print('Starting processing')
    process_data('cleaned_qry_KneeTreatmentDecisionTree.csv')
    print('Finished processing')
