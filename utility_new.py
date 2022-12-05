class Symptom(object):
    def __init__(self, symptom, values):
        self.symptom = symptom
        self.values = values

    @staticmethod
    def initialize_symptoms(symptoms):
        result = {}
        for symptom, values in symptoms.items():
            result[symptom] = (Symptom(symptom, values))
        return result

    def __contains__(self, key):
        # print(key)
        return key.casefold() in (value.casefold() for value in self.values)

    def __repr__(self):
        return f'{self.symptom}:{self.values}'


SYMPTOMS = {
    'Abduction': ['abduction'],
    'Mild Abduction': ['mild abduction'],
    'Abd': ['abd'],
    'Mild Abd': ['mild abd'],
    'Adduction': ['adduction'],
    'Mild Adduction': ['mild adduction'],
    'Add': ['add'],
    'Mild Add': ['mild add'],
    'Pronation': ['pronation'],
    'Mild Pronation': ['mild pronation'],
    'Supination': ['supination'],
    'Mild Supination': ['mild supination'],
    'Valgus': ['valgus'],
    'Mild Valgus': ['mild valgus'],
    'Varus': ['varus'],
    'Mild Varus': ['mild varus'],
    'Equinus': ['equinus'],
    'Mild Equinus': ['mild equinus'],
    'PF': ['pf'],
    'PF 1st Ray': ['pf 1st ray'],
    '1st Ray': ['1st ray'],
    'PF 5th Ray': ['pf 5th ray'],
    'Low Arch': ['low arch'],
    'Low Med Arch': ['low med arch'],
    'High Arch': ['high arch'],
    'High Med Arch': ['high med arch'],
    'Midfoot Break': ['midfoot break'],
    'Planovalgus': ['planovalgus'],
    'Mild Planovalgus': ['mild planovalgus'],
    'Planus': ['planus'],
    'Mild Planus': ['mild planus'],
    'Rocker Bottom': ['rocker bottom'],
    'Cavus': ['cavus'],
    'Mild Cavus': ['mild cavus'],
    'Calcaneus': ['calcaneus'],
    'Mild Calcaneus': ['mild calcaneus'],
    'Dorsal Bunion': ['dorsal bunion'],
    'HalVal': ['halval'],
    'Elevation': ['elevation'],
    'Plantarflexed 1st Ray': ['plantarflexed 1st ray']
}
SYMPTOMS_DEF = Symptom.initialize_symptoms(SYMPTOMS)

def break_down_observation(s): return [x.strip() for x in s.split(';')]

def get_left_foot_wt_bearing_observation(data, foottype):
    if foottype not in ['forefoot', 'midfoot', 'hindfoot']:
        raise ValueError('Invalid footype value')
    if foottype == 'forefoot':
        left_foot = 'LeftForefootWtBearing'
    elif foottype == 'midfoot':
        left_foot = 'LeftMidfootWtBearing'
    elif foottype == 'hindfoot':
        left_foot = 'LeftHindfootWtBearing'
    observations = break_down_observation(data[left_foot])
    return observations

def get_right_foot_wt_bearing_observation(data, foottype):
    if foottype not in ['forefoot', 'midfoot', 'hindfoot']:
        raise ValueError('Invalid footype value')
    if foottype == 'forefoot':
        right_foot = 'RightForefootWtBearing'
    elif foottype == 'midfoot':
        right_foot = 'RightMidfootWtBearing'
    elif foottype == 'hindfoot':
        right_foot = 'RightHindfootWtBearing'
    observations = break_down_observation(data[right_foot])
    return observations

def is_symptom_present(observation, symptoms):
    if isinstance(observation, list):
        print(observation)

    for symptom in symptoms:
        if observation in symptom:
            return True
    return False

def any_symptom_present(observations, symptoms):
    # print(observations)
    if isinstance(symptoms, Symptom):
        symptoms = [symptoms]
    for observation in observations:
        # print(observation)
        if is_symptom_present(observation, symptoms):
            return True
    return False

def left_additional_treatment(data, treatment, path):
    if data['KneeFlexionAtIC'] >= 25:
        path += ' -> KneeFlexionAtIC -> greater than or equal to 25'
        if data['LeftKneeRomPopAngle'] >= 50:
            path += ' -> LeftKneeRomPopAngle -> greater than or equal to 50'
            if data['LeftKneeRomExt'] >= -10:
                path += ' -> LeftKneeRomExt -> greater than or equal to -10 -> Treatment Recommended'
                treatment += 'Hamstring Lengthening & Correct Crouch Causes'
                return path, treatment
            elif -30 <= data['LeftKneeRomExt'] < -10:
                path += ' -> LeftKneeRomExt -> greater than or equal to -30 or less than -10 -> Treatment Recommended'
                treatment +='Posterior Knee Capsulotomy & Correct all Crouch Causes'
                return path, treatment
            else:
                path += ' -> LeftKneeRomExt -> less than -30 -> Treatment Recommended'
                treatment += 'Knee Extension Osteotomy & Correct All Crouch Causes'
                return path, treatment
        else:
            path += ' -> LeftKneeRomPopAngle -> less than 50 -> No Treatment Recommended'
            treatment += 'No Treatment Recommendation'
            return path, treatment
    else:
        path += ' -> KneeFlexionAtIC -> less than 25 -> No Treatment Recommended'
        treatment += 'No Treatment Recommendation'
        return path, treatment

def right_additional_treatment(data, treatment, path):
    if data['KneeFlexionAtIC'] >= 25:
        path += ' -> KneeFlexionAtIC -> greater than or equal to 25'
        if data['RightKneeRomPopAngle'] >= 50:
            path += ' -> RightKneeRomPopAngle -> greater than or equal to 50'
            if data['RightKneeRomExt'] >= -10:
                path += ' -> RightKneeRomExt -> greater than or equal to -10 -> Treatment Recommended'
                treatment += 'Hamstring Lengthening & Correct Crouch Causes'
                return path, treatment
            elif -30 <= data['RightKneeRomExt'] < -10:
                path += ' -> RightKneeRomExt -> greater than or equal to -30 or less than -10 -> Treatment Recommended'
                treatment +='Posterior Knee Capsulotomy & Correct all Crouch Causes'
                return path, treatment
            else:
                path += ' -> RightKneeRomExt -> less than -30 -> Treatment Recommended'
                treatment += 'Knee Extension Osteotomy & Correct All Crouch Causes'
                return path, treatment
        else:
            path += ' -> RightKneeRomPopAngle -> less than 50 -> No Treatment Recommended'
            treatment += 'No Treatment Recommendation'
            return path, treatment
    else:
        path += ' -> KneeFlexionAtIC -> less than 25 -> No Treatment Recommended'
        treatment += 'No Treatment Recommendation'
        return path, treatment

def case_lessthan_5(data, path):
    if data['Side'] == "Left":
        path += ' -> Side -> Left'
        if data['LeftKneeRomPopAngle'] < 60:
            path += ' -> LeftKneeRomPopAngle -> less than 60'
            if data['AnkleDorsiPlantarMeanStanceDF'] <= 2:
                path += ' -> AnkleDorsiPlantarMeanStanceDF -> less than or equal to 2 -> Treatment Recommended'
                treatment = 'Botox Injection & Knee Splinting'
                return path, treatment
            else:
                path += ' -> AnkleDorsiPlantarMeanStanceDF -> greater than 2 -> No Treatment Recommended'
                treatment = 'No Treatment Recommendation'
                return path, treatment
        else:
            path += ' -> LeftKneeRomPopAngle -> greater than or equal to 60'
            if data['LeftKneeRomExt'] <= -10:
                path += ' -> LeftKneeRomExt -> less than or equal to -10 -> Treatment Recommended'
                treatment = 'Hamstring Lengthening'
                return path, treatment
            else:
                path += ' -> LeftKneeRomExt -> greater than -10 -> No Treatment Recommended'
                treatment = 'No Treatment Recommendation'
                return path, treatment
    else:
        path += ' -> Side -> Right'
        if data['RightKneeRomPopAngle'] < 60:
            path += ' -> RightKneeRomPopAngle -> less than 60'
            if data['AnkleDorsiPlantarMeanStanceDF'] <= 2:
                path += ' -> AnkleDorsiPlantarMeanStanceDF -> less than or equal to 2 -> Treatment Recommended'
                treatment = 'Botox Injection & Knee Splinting'
                return path, treatment
            else:
                path += ' -> AnkleDorsiPlantarMeanStanceDF -> greater than 2 -> No Treatment Recommended'
                treatment = 'No Treatment Recommendation'
                return path, treatment
        else:
            path += ' -> RightKneeRomPopAngle -> greater than or equal to 60'
            if data['RightKneeRomExt'] <= -10:
                path += ' -> RightKneeRomExt -> less than or equal to -10 -> Treatment Recommended'
                treatment = 'Hamstring Lengthening'
                return path, treatment
            else:
                path += ' -> RightKneeRomExt -> greater than -10 -> No Treatment Recommended'
                treatment = 'No Treatment Recommendation'
                return path, treatment

def case_between_5_10(data, path):
    if data['Side'] == "Left":
        path += ' -> Side -> Left'
        if -40 <= data['LeftKneeRomExt'] < -20:
            path += ' -> LeftKneeRomExt -> greater than or equal to -40 or less than -20 -> Treatment Recommended'
            treatment = 'Knee Capsulotomy & Hamstring Lengthening'
            return path, treatment
        elif -20 <= data['LeftKneeRomExt'] <= 0:
            path += ' -> LeftKneeRomExt -> greater than or equal to -20 or less than or equal to 0'
            if data['KneeFlexionAtIC'] >= 25:
                path += ' -> KneeFlexionAtIC -> greater than or equal to 25'
                if data['LeftKneeRomPopAngle'] >= 50:
                    path += ' -> LeftKneeRomPopAngle -> greater than or equal to 50'
                    if data['KneeFlexionMin'] >= 25:
                        path += ' -> KneeFlexionMin -> greater than or equal to 25 -> Treatment Recommended'
                        treatment = 'Knee Capsulotomy & Hamstring Lengthening'
                        return path, treatment
                    else:
                        path += ' -> KneeFlexionMin -> less than 25 -> No Treatment Recommended'
                        treatment = 'No Treatment Recommendation'
                        return path, treatment
                else:
                    path += ' -> LeftKneeRomPopAngle -> less than 50 -> No Treatment Recommended'
                    treatment = 'No Treatment Recommendation'
                    return path, treatment
            else:
                path += ' -> KneeFlexionAtIC -> less than 25 -> No Treatment Recommended'
                treatment = 'No Treatment Recommendation'
                return path, treatment
        else:
            path += ' -> LeftKneeRomExt -> greater than 0 or less than -40 -> No Treatment Recommended'
            treatment = 'No Treatment Recommendation'
            return path, treatment
    else:
        path += ' -> Side -> Right'
        if -40 <= data['RightKneeRomExt'] < -20:
            path += ' -> RightKneeRomExt -> greater than or equal to -40 or less than -20 -> Treatment Recommended'
            treatment = 'Knee Capsulotomy & Hamstring Lengthening'
            return path, treatment
        elif -20 <= data['RightKneeRomExt'] <= 0:
            path += ' -> RightKneeRomExt -> greater than or equal to -20 or less than or equal to 0'
            if data['KneeFlexionAtIC'] >= 25:
                path += ' -> KneeFlexionAtIC -> greater than or equal to 25'
                if data['RightKneeRomPopAngle'] >= 50:
                    path += ' -> RightKneeRomPopAngle -> greater than or equal to 50'
                    if data['KneeFlexionMin'] >= 25:
                        path += ' -> KneeFlexionMin -> greater than or equal to 25 -> Treatment Recommended'
                        treatment = 'Knee Capsulotomy & Hamstring Lengthening'
                        return path, treatment
                    else:
                        path += ' -> KneeFlexionMin -> less than 25 -> No Treatment Recommended'
                        treatment = 'No Treatment Recommendation'
                        return path, treatment
                else:
                    path += ' -> RightKneeRomPopAngle -> less than 50 -> No Treatment Recommended'
                    treatment = 'No Treatment Recommendation'
                    return path, treatment
            else:
                path += ' -> KneeFlexionAtIC -> less than 25 -> No Treatment Recommended'
                treatment = 'No Treatment Recommendation'
                return path, treatment
        else:
            path += ' -> RightKneeRomExt -> greater than 0 or less than -40 -> No Treatment Recommended'
            treatment = 'No Treatment Recommendation'
            return path, treatment

def case_morethan_10(data, path):
    if data['Side'] == "Left":
        path += ' -> Side -> Left'
        if data['KneeFlexionMin'] < 0:
            path += ' -> KneeFlexionMin -> less than 0 -> Treatment Recommended'
            treatment = 'Correct Ankle Equinus for Back Kneeing'
            return path, treatment
        else:
            path += ' -> KneeFlexionMin -> greater than or equal to 0'
            if data['HipFlexionMin'] > -2:
                path += ' -> HipFlexionMin -> greater than -2 (Flexed Hip)'
                fore_foot_observations = get_left_foot_wt_bearing_observation(data, 'forefoot')
                mid_foot_observations = get_left_foot_wt_bearing_observation(data, 'midfoot')
                hind_foot_observations = get_left_foot_wt_bearing_observation(data, 'hindfoot')
                FOREFOOT_SYMPTOMS = [SYMPTOMS_DEF[x] for x in
                                     ['Abduction', 'Pronation', 'Valgus']]
                MIDFOOT_SYMPTOMS = [SYMPTOMS_DEF[x] for x in
                                    ['Low Arch', 'Midfoot Break', 'Planovalgus', 'Planus', 'Valgus', 'Pronation', 'Rocker Bottom']]
                HINDFOOT_SYMPTOMS = [SYMPTOMS_DEF[x] for x in ['Valgus']]
                if any_symptom_present(fore_foot_observations, FOREFOOT_SYMPTOMS) or any_symptom_present(mid_foot_observations, MIDFOOT_SYMPTOMS) or any_symptom_present(hind_foot_observations, HINDFOOT_SYMPTOMS):
                    path += ' -> Foot Position -> True for any'
                    if data['AnkleDorsiPlantarMeanStanceDF'] <= 2:
                        path += ' -> AnkleDorsiPlantarMeanStanceDF -> less than or equal to 2'
                        if data['LeftThighFootAngle'] >= 20:
                            path += ' -> LeftThighFootAngle -> greater than or equal to 20 -> Treatment Recommended'
                            treatment = 'Hip Extension Osteotomy, Planovalgus & Torsional Correction'
                            return path, treatment
                        else:
                            path += ' -> LeftThighFootAngle -> less than 20 -> No Treatment Recommended'
                            treatment = 'No Hip or Foot Treatment Recommendation'
                            return left_additional_treatment(data, treatment, path)
                    else:
                        path += ' -> AnkleDorsiPlantarMeanStanceDF -> greater than 2 -> No Treatment Recommended'
                        treatment = 'No Hip or Foot Treatment Recommendation'
                        return left_additional_treatment(data, treatment, path)
                else:
                    path += ' -> Foot Position -> False for all -> No Treatment Recommended'
                    treatment = 'No Hip or Foot Treatment Recommendation'
                    return left_additional_treatment(data, treatment, path)
            else:
                path += ' -> HipFlexionMin -> less than or equal to -2'
                treatment = ''
                left_additional_treatment(data, treatment, path)
    else:
        path += ' -> Side -> Right'
        if data['KneeFlexionMin'] < 0:
            path += ' -> KneeFlexionMin -> less than 0 -> Treatment Recommended'
            treatment = 'Correct Ankle Equinus for Back Kneeing'
            return path, treatment
        else:
            path += ' -> KneeFlexionMin -> greater than or equal to 0'
            if data['HipFlexionMin'] > -2:
                path += ' -> HipFlexionMin -> greater than -2 (Flexed Hip)'
                fore_foot_observations = get_right_foot_wt_bearing_observation(data, 'forefoot')
                mid_foot_observations = get_right_foot_wt_bearing_observation(data, 'midfoot')
                hind_foot_observations = get_right_foot_wt_bearing_observation(data, 'hindfoot')
                FOREFOOT_SYMPTOMS = [SYMPTOMS_DEF[x] for x in
                                     ['Abduction', 'Pronation', 'Valgus']]
                MIDFOOT_SYMPTOMS = [SYMPTOMS_DEF[x] for x in
                                    ['Low Arch', 'Midfoot Break', 'Planovalgus', 'Planus', 'Valgus', 'Pronation', 'Rocker Bottom']]
                HINDFOOT_SYMPTOMS = [SYMPTOMS_DEF[x] for x in ['Valgus']]
                if any_symptom_present(fore_foot_observations, FOREFOOT_SYMPTOMS) or any_symptom_present(mid_foot_observations, MIDFOOT_SYMPTOMS) or any_symptom_present(hind_foot_observations, HINDFOOT_SYMPTOMS):
                    path += ' -> Foot Position -> True for any'
                    if data['AnkleDorsiPlantarMeanStanceDF'] <= 2:
                        path += ' -> AnkleDorsiPlantarMeanStanceDF -> less than or equal to 2'
                        if data['RightThighFootAngle'] >= 20:
                            path += ' -> RightThighFootAngle -> greater than or equal to 20 -> Treatment Recommended'
                            treatment = 'Hip Extension Osteotomy, Planovalgus & Torsional Correction'
                            return path, treatment
                        else:
                            path += ' -> RightThighFootAngle -> less than 20 -> No Treatment Recommended'
                            treatment = 'No Hip or Foot Treatment Recommendation'
                            return right_additional_treatment(data, treatment, path)
                    else:
                        path += ' -> AnkleDorsiPlantarMeanStanceDF -> greater than 2 -> No Treatment Recommended'
                        treatment = 'No Hip or Foot Treatment Recommendation'
                        return right_additional_treatment(data, treatment, path)
                else:
                    path += ' -> Foot Position -> False for all -> No Treatment Recommended'
                    treatment = 'No Hip or Foot Treatment Recommendation'
                    return right_additional_treatment(data, treatment, path)
            else:
                path += ' -> HipFlexionMin -> less than or equal to -2'
                treatment = ''
                right_additional_treatment(data, treatment, path)