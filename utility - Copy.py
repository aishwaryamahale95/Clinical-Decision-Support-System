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


def check_primary_deformity(data):
    fore_foot_observations = get_foot_wt_bearing_observation(data, 'forefoot')
    mid_foot_observations = get_foot_wt_bearing_observation(data, 'midfoot')
    hind_foot_observations = get_foot_wt_bearing_observation(data, 'hindfoot')

    FOREFOOT_SYMPTOMS = [SYMPTOMS_DEF[x] for x in
                         ['Abduction', 'Adduction', 'Pronation', 'Supination', 'Valgus', 'Varus', 'Equinus', 'PF',
                          'PF 1st Ray', 'PF 5th Ray']]
    MIDFOOT_SYMPTOMS = [SYMPTOMS_DEF[x] for x in
                        ['Low Arch', 'High Arch', 'Midfoot Break', 'Planovalgus', 'Planus', 'Valgus', 'Pronation',
                         'Rocker Bottom', 'Varus', 'Cavus']]
    HINDFOOT_SYMPTOMS = [SYMPTOMS_DEF[x] for x in ['Valgus', 'Varus', 'Calcaneus', 'Equinus']]
    if any_symptom_present(fore_foot_observations, FOREFOOT_SYMPTOMS) or any_symptom_present(mid_foot_observations,
                                                                                             MIDFOOT_SYMPTOMS) or any_symptom_present(
        hind_foot_observations, HINDFOOT_SYMPTOMS):
        return True
    else:
        return False


def break_down_observation(s): return [x.strip() for x in s.split(';')]


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


def yes_or_no(question, choice='y/n'):
    while "the answer is invalid":
        reply = str(input(f'{question} ({choice}): ')).lower().strip()
        return reply[:1]


def moderate_or_severe_or_else(question, choice='m/s/e'):
    while "the answer is invalid":
        reply = str(input(f'{question} ({choice}): ')).lower().strip()
        return reply[:1]


def mild_or_moderate_or_severe(question, choice='mi/mo/se'):
    while "the answer is invalid":
        reply = str(input(f'{question} ({choice}): ')).lower().strip()
        return reply[:2]


def plus_or_2plus_or_Catch_or_1Beat_or_2Beats(question, choice='p/pp/c/b/bb'):
    while "the answer is invalid":
        reply = str(input(f'{question} ({choice}): ')).lower().strip()
        return reply[:2]
    reply = str(p).lower().strip()
    reply[:2]


def identify_symptoms_observation(observations, symptoms):
    if not isinstance(observations, set):
        observations = set(observations)
    allsymptoms = set()
    for symptom in symptoms:
        allsymptoms.update(symptom.values)
    applicable = set(observations).intersection(allsymptoms)
    return applicable


def get_foot_wt_bearing_observation(data, foottype):
    if foottype not in ['forefoot', 'midfoot', 'hindfoot', 'hallux']:
        raise ValueError('Invalid footype value')
    if foottype == 'forefoot':
        left_foot = 'LeftForefootWtBearing'
        right_foot = 'RightForefootWtBearing'
    elif foottype == 'midfoot':
        left_foot = 'LeftMidfootWtBearing'
        right_foot = 'RightMidfootWtBearing'
    elif foottype == 'hindfoot':
        left_foot = 'LeftHindFootWtBearing'
        right_foot = 'RightHindFootWtBearing'
    elif foottype == 'hallux':
        left_foot = 'LeftHalluxWtBearing'
        right_foot = 'RightHalluxWtBearing'

    observations = break_down_observation(data[left_foot]) + break_down_observation(data[right_foot])
    return observations


def prescribe_additional_treatment_gmfcs_level12_between5_10(data, treatment, path):
    fore_foot_observations = get_foot_wt_bearing_observation(data, 'forefoot')
    hallux_observations = get_foot_wt_bearing_observation(data, 'hallux')
    forefoot_symptom = SYMPTOMS_DEF['Supination']
    hallux_symptom = [SYMPTOMS_DEF[x] for x in ['Dorsal Bunion', 'Plantarflexed 1st Ray']]
    if any_symptom_present(fore_foot_observations, forefoot_symptom) or any_symptom_present(hallux_observations,
                                                                                            hallux_symptom):
        path += ' -> Foot Position -> True for any -> Treatment Recommended'
        treatment += ' + Tibialis Anterior Transfer and Osteotomy or Naviculocuneiform fusion'
    else:
        path += ' -> Foot Position -> Else -> No Treatment Recommended'
    return path, treatment


def prescribe_additional_treatment_gmfcs_level12_morethan10(data, treatment, path):
    hallux_observations = get_foot_wt_bearing_observation(data, 'hallux')
    hallux_symptom = SYMPTOMS_DEF['HalVal']
    if any_symptom_present(hallux_observations, hallux_symptom):
        path += ' -> Foot Position -> True for Hallux -> Treatment Recommended'
        treatment += ' + Correct Bunion'
    else:
        path += ' -> Foot Position -> Else for Hallux -> Check Thigh Foot Angle > 20?'
        if data['LeftThighFootAngle'] > '20' or data['RightThighFootAngle'] > '20':
            path += ' -> Yes -> Treatment Recommended'
            treatment += ' + Also Correct tibial rotation with Derotation osteotomy'
        else:
            path += ' -> No -> No Treatment Recommended'
    return path, treatment


def prescribe_additional_treatment_gmfcs_level34_morethan10(data, treatment, path):
    hallux_observations = get_foot_wt_bearing_observation(data, 'hallux')
    hallux_symptom = SYMPTOMS_DEF['HalVal']
    if any_symptom_present(hallux_observations, hallux_symptom):
        path += ' -> Foot Position -> True for Hallux -> Treatment Recommended'
        treatment += ' + Correct Bunion with fusion of 1st MTP'
    else:
        path += ' -> Foot Position -> Else for Hallux -> No Treatment Recommended'
    return path, treatment


def investigate_gmfcs_level12_between5_10(data, path):
    resp = None
    path += ' -> Tolerating AFO'
    if data['LeftOrthoticTolerated'] == 'Yes' or data['RightOrthoticTolerated'] == 'Yes':
        path += ' -> Yes -> Treatment Recommended'
        treatment = 'Continue AFO'
        return path, treatment
    else:
        path += ' -> No -> Is Ankle Valgus angle > 10?'
        while resp not in {"y", "n"}:
            resp = yes_or_no('Is Ankle Valgus angle > 10?', 'y - > 10/n - <= 10')
            if resp == 'y':
                path += ' -> Yes -> Treatment Recommended'
                treatment = 'Distal Medial Tibial Ephiphysiodesis'
                return path, treatment
            elif resp == 'n':
                path += ' -> No -> Spasticity'
                if data['LeftToneGastroc'] == 0 or data['RightToneGastroc'] == 0 or data['LeftTonePeroneals'] == 0 or \
                        data[
                            'RightTonePeroneals'] == 0:
                    path += ' -> Any = 0 -> Treatment Recommended'
                    treatment = 'Subtalar Fusion'
                    return prescribe_additional_treatment_gmfcs_level12_between5_10(data, treatment, path)
                elif data['LeftToneGastroc'] >= 2 or data['RightToneGastroc'] >= 2 or data['LeftTonePeroneals'] >= 2 or \
                        data['RightTonePeroneals'] >= 2:
                    path += ' -> Any >= 2 -> HOW SEVERE IS THE FOOT DEFORMITY?'
                    while resp not in {"mi", "mo", "se"}:
                        resp = mild_or_moderate_or_severe('HOW SEVERE IS THE FOOT DEFORMITY?',
                                                          'mi - Mild/mo - Moderate/se - Severe')
                        if resp == 'mi':
                            path += ' -> Mild -> Treatment Recommended'
                            treatment = 'Lateral Column Lengthening'
                            return prescribe_additional_treatment_gmfcs_level12_between5_10(data, treatment, path)
                        elif resp == 'mo' or resp == 'se':
                            path += ' -> Moderate or Severe -> Perineal Clonus'
                            resp = plus_or_2plus_or_Catch_or_1Beat_or_2Beats('IS PERINEAL CLONUS?',
                                                                             'p - +/pp - ++/c - Catch/b - 1 Beat/ bb - 2Beats')
                            if resp == 'p' or resp == 'pp' or resp == 'c' or resp == 'b' or resp == 'bb':
                                path += ' -> +, ++, Catch, 1 beat, or 2 beats -> Treatment Recommended'
                                treatment = 'Myofascial Lenthening of Perineus Brevis ONLY with Lateral Column ' \
                                            'Lengthening or Subtalar Fusion '
                                return prescribe_additional_treatment_gmfcs_level12_between5_10(data, treatment, path)
                            else:
                                path += ' -> Else -> Treatment Recommended'
                                treatment = 'Subtalar Fusion'
                                return prescribe_additional_treatment_gmfcs_level12_between5_10(data, treatment, path)
                        else:
                            print("Choose Input Wisely")
                else:
                    path += ' -> Else -> No Treatment Recommended'
                    treatment = 'No Treatment Recommendation'
                    return path, treatment
            else:
                print("Choose Input Wisely")


def investigate_gmfcs_level12_morethan10(data, path):
    fore_foot_observations = get_foot_wt_bearing_observation(data, 'forefoot')
    mid_foot_observations = get_foot_wt_bearing_observation(data, 'midfoot')
    hind_foot_observations = get_foot_wt_bearing_observation(data, 'hindfoot')
    hallux_observations = get_foot_wt_bearing_observation(data, 'hallux')

    mild_forefoot_symptom = [SYMPTOMS_DEF[x] for x in
                             ['Mild Abduction', 'Mild Equinus', 'Mild Supination', 'Mild Valgus']]
    mild_midfoot_symptom = [SYMPTOMS_DEF[x] for x in ['Mild Planus', 'Mild Valgus']]
    mild_hindfoot_symptom = [SYMPTOMS_DEF[x] for x in ['Mild Equinus', 'Mild Valgus']]

    moderate_forefoot_symptom = [SYMPTOMS_DEF[x] for x in ['Abd', 'Equinus', 'Pronation', 'Valgus']]
    moderate_midfoot_symptom = [SYMPTOMS_DEF[x] for x in
                                ['Equinus', 'Low Med Arch', 'Midfoot Break', 'Planovalgus', 'Planus', 'Valgus',
                                 'Pronation', 'Rocker Bottom']]
    moderate_hindfoot_symptom = [SYMPTOMS_DEF[x] for x in ['Equinus', 'Valgus']]

    severe_hallux_symptoms = [SYMPTOMS_DEF[x] for x in ['1st Ray', 'Elevation', 'HalVal']]
    severe_forefoot_symptom = [SYMPTOMS_DEF[x] for x in ['Abduction', 'Pronation', 'Valgus']]
    severe_midfoot_symptom = [SYMPTOMS_DEF[x] for x in
                              ['Low Med Arch', 'Midfoot Break', 'Planovalgus', 'Planus', 'Valgus', 'Pronation',
                               'Rocker Bottom']]
    severe_hindfoot_symptom = [SYMPTOMS_DEF[x] for x in ['Equinus', 'Valgus']]

    resp = None
    path += ' -> Foot Position -> HOW SEVERE IS THE VALGUS?'
    while resp not in {"mi", "mo", "se"}:
        resp = mild_or_moderate_or_severe('HOW SEVERE IS THE VALGUS?',
                                          'mi - Mild Valgus/mo - Moderate Valgus/se - Severe Valgus')
        if resp == 'mi':
            if any_symptom_present(fore_foot_observations, mild_forefoot_symptom) or any_symptom_present(
                    mid_foot_observations, mild_midfoot_symptom) or any_symptom_present(hind_foot_observations,
                                                                                        mild_hindfoot_symptom):
                path += ' -> Mild -> True for any -> Treatment Recommended'
                treatment = 'Lateral Column Lengthening Through the Calcaneus'
                return prescribe_additional_treatment_gmfcs_level12_morethan10(data, treatment, path)
            else:
                path += ' -> Mild -> Else -> No Treatment Recommended'
                treatment = 'No Treatment Recommendation'
                return path, treatment
        elif resp == 'mo':
            if any_symptom_present(fore_foot_observations, moderate_forefoot_symptom) or any_symptom_present(
                    mid_foot_observations, moderate_midfoot_symptom) or any_symptom_present(hind_foot_observations,
                                                                                            moderate_hindfoot_symptom):
                path += ' -> Moderate -> True for any -> Treatment Recommended'
                treatment = 'Subtalar Fusion'
                return prescribe_additional_treatment_gmfcs_level12_morethan10(data, treatment, path)
            else:
                path += ' -> Moderate -> Else -> No Treatment Recommended'
                treatment = 'No Treatment Recommendation'
                return path, treatment
        elif resp == 'se':
            path += ' -> Severe'
            if any_symptom_present(hallux_observations, severe_hallux_symptoms) or any_symptom_present(
                    fore_foot_observations, severe_forefoot_symptom) or any_symptom_present(mid_foot_observations,
                                                                                            severe_midfoot_symptom) or any_symptom_present(
                hind_foot_observations, severe_hindfoot_symptom):
                path += ' -> True for any -> Ankle Eversion > 10?'
                if data['LeftAnkleRomEver'] > 10 or data['RightAnkleRomEver'] > 10:
                    while resp not in {"y", "n"}:
                        path += ' -> Yes -> IS THE GROWTH PLATE OPEN?'
                        resp = yes_or_no('IS THE GROWTH PLATE OPEN?', 'y - OPEN/n - OFF')
                        if resp == 'y':
                            path += ' -> Yes -> Treatment Recommended'
                            treatment = 'Epiphysiodesis'
                            return prescribe_additional_treatment_gmfcs_level12_morethan10(data, treatment, path)
                        elif resp == 'n':
                            path += ' -> No -> Treatment Recommended'
                            treatment = 'Tibia Osteotomy'
                            return prescribe_additional_treatment_gmfcs_level12_morethan10(data, treatment, path)
                        else:
                            print("Choose Input Wisely")
                else:
                    path += ' -> Else -> No Treatment Recommended'
                    treatment = 'No Treatment Recommendation'
                    return path, treatment
            else:
                path += ' -> Foot Position values are wrong -> Unable to determine treatment'
                print("Foot Position values is wrong, so unable to reach conclusion")
                treatment = 'Unable to determine treatment'
                return path, treatment
        else:
            print("Choose Input Wisely")


def investigate_gmfcs_level34_between5_10(data, path):
    fore_foot_observations = get_foot_wt_bearing_observation(data, 'forefoot')
    mid_foot_observations = get_foot_wt_bearing_observation(data, 'midfoot')
    hind_foot_observations = get_foot_wt_bearing_observation(data, 'hindfoot')
    hallux_observations = get_foot_wt_bearing_observation(data, 'hallux')

    hallux_symptoms = [SYMPTOMS_DEF[x] for x in ['PF 1st Ray', '1st Ray', 'Elevation']]
    forefoot_symptom = [SYMPTOMS_DEF[x] for x in ['Abduction', 'Pronation', 'Valgus']]
    midfoot_symptom = [SYMPTOMS_DEF[x] for x in
                       ['Low Med Arch', 'Midfoot Break', 'Planovalgus', 'Planus', 'Valgus', 'Pronation',
                        'Rocker Bottom']]
    hindfoot_symptom = SYMPTOMS_DEF['Valgus']

    path += ' -> Foot Position'
    if any_symptom_present(hind_foot_observations, hindfoot_symptom):
        if any_symptom_present(mid_foot_observations, midfoot_symptom):
            if any_symptom_present(fore_foot_observations, forefoot_symptom) or any_symptom_present(hallux_observations,
                                                                                                    hallux_symptoms):
                path += ' -> True for Hindfoot and any Midfoot and any Forefoot or Hallux -> Treatment Recommended'
                treatment = 'Subtalar Fusion and calcaneocuboid lenghening fusion with Tibialis Anterior Transfer & ' \
                            'Fusion or Naviculocuneiform Osteotomy '
                return path, treatment
            else:
                path += ' -> True for Hindfoot and any Midfoot -> Treatment Recommended'
                treatment = 'Calcaneocubiod lenghtening fusion and Subtalar fusion'
                return path, treatment
        else:
            path += ' -> True for only Hindfoot -> Treatment Recommended'
            treatment = 'Subtalar Fusion'
            return path, treatment
    else:
        path += ' -> Else -> No Treatment Recommended'
        treatment = 'No Treatment Recommendation'
        return path, treatment


def investigate_gmfcs_level34_morethan10(data, path):
    fore_foot_observations = get_foot_wt_bearing_observation(data, 'forefoot')
    mid_foot_observations = get_foot_wt_bearing_observation(data, 'midfoot')
    hind_foot_observations = get_foot_wt_bearing_observation(data, 'hindfoot')
    hallux_observations = get_foot_wt_bearing_observation(data, 'hallux')

    hallux_symptoms = [SYMPTOMS_DEF[x] for x in ['PF 1st Ray', 'Elevation']]
    forefoot_symptom = [SYMPTOMS_DEF[x] for x in ['Abduction', 'Pronation', 'Valgus']]
    midfoot_symptom = [SYMPTOMS_DEF[x] for x in
                       ['Low Arch', 'Midfoot Break', 'Planovalgus', 'Planus', 'Valgus', 'Pronation', 'Rocker Bottom']]
    hindfoot_symptom = SYMPTOMS_DEF['Valgus']

    path += ' -> Foot Position'
    if any_symptom_present(hind_foot_observations, hindfoot_symptom):
        if any_symptom_present(mid_foot_observations, midfoot_symptom):
            if any_symptom_present(fore_foot_observations, forefoot_symptom) or any_symptom_present(hallux_observations,
                                                                                                    hallux_symptoms):
                path += ' -> True for Hindfoot and any Midfoot and any Forefoot or Hallux -> Treatment Recommended'
                treatment = 'Subtalar Fusion & Fusion of Naviculocuneiform or whole medial column'
                return prescribe_additional_treatment_gmfcs_level34_morethan10(data, treatment, path)
            else:
                path += ' -> True for Hindfoot and any Midfoot -> Treatment Recommended'
                treatment = 'Calcaneocubiod lenghtening fusion and Subtalar fusion'
                return prescribe_additional_treatment_gmfcs_level34_morethan10(data, treatment, path)
        else:
            path += ' -> True for Hindfoot -> Treatment Recommended'
            treatment = 'Subtalar Fusion'
            return prescribe_additional_treatment_gmfcs_level34_morethan10(data, treatment, path)
    else:
        path += ' -> Else -> No Treatment Recommended'
        treatment = 'No Treatment Recommendation'
        return path, treatment


def investigate_valgus(data, path):
    gmfcs = int(data['GmfcsNew'])
    if gmfcs == 1 or gmfcs == 2:
        path += ' -> GMFCS LEVEL 1 or 2'
        return investigate_gmfcs_level12_between5_10(data, path)
    elif gmfcs == 3 or gmfcs == 4:
        path += ' -> GMFCS LEVEL 3 or 4'
        return investigate_gmfcs_level34_between5_10(data, path)
    else:
        path = ' -> GMFCS level is wrong -> Unable to determine treatment'
        print("GMFCS value is wrong, so unable to reach conclusion")
        treatment = 'Unable to determine treatment'
        return path, treatment


def investigate_hemiplegia(data, path):
    resp = None
    path += ' -> IS TIB ANT OUT OF PHASE OR ALWAYS ON?'
    while resp not in {"y", "n"}:
        resp = yes_or_no('IS TIB ANT OUT OF PHASE OR ALWAYS ON?', 'y - OUT OF PHASE/n - ALWAYS ON')
        if resp == 'y':
            path += ' -> Yes -> Treatment Recommended'
            treatment = 'Split Transfer Tibialis Anterior(SPLATT)'
            return path, treatment
        elif resp == 'n':
            path += ' -> No -> IS POST TIB OUT OF PHASE OR ALWAYS ON?'
            resp = yes_or_no('IS POST TIB OUT OF PHASE OR ALWAYS ON?', 'y - OUT OF PHASE/n - ALWAYS ON')
            if resp == 'y':
                path += ' -> Yes -> Treatment Recommended'
                treatment = 'Split Transfer Tibialis Posterior (SPOTT)'
                return path, treatment
            elif resp == 'n':
                path += ' -> No -> No Treatment Recommended'
                treatment = 'No Treatment Recommendation'
                return path, treatment
            else:
                print("Choose Input Wisely")
        else:
            print("Choose Input Wisely")


def investigate_diplegia(data, path):
    fore_foot_observations = get_foot_wt_bearing_observation(data, 'forefoot')
    mid_foot_observations = get_foot_wt_bearing_observation(data, 'midfoot')
    hind_foot_observations = get_foot_wt_bearing_observation(data, 'hindfoot')

    forefoot_symptom = [SYMPTOMS_DEF[x] for x in
                        ['Adduction', 'Mild Adduction', 'Supination', 'Mild Supination', 'Varus', 'Mild Varus']]
    hindfoot_symptom = [SYMPTOMS_DEF[x] for x in ['Varus', 'Mild Varus']]
    midfoot_symptom = [SYMPTOMS_DEF[x] for x in ['Cavus', 'Mild Cavus']]

    resp = None
    path += ' -> Foot Position'
    if any_symptom_present(fore_foot_observations, forefoot_symptom):
        path += ' -> True for Forefoot -> IS TIB ANT ALWAYS ON?'
        while resp not in {"y", "n"}:
            resp = yes_or_no('IS TIB ANT ALWAYS ON?')
            if resp == 'y':
                path += ' -> Yes -> Treatment Recommended'
                treatment = 'Transfer the Tib Ant to the Lateral Cuneiform'
                return path, treatment
            elif resp == 'n':
                path += ' -> No -> No Treatment Recommended'
                treatment = 'No Treatment Recommendation'
                return path, treatment
            else:
                print("Choose Input Wisely")
    elif (any_symptom_present(hind_foot_observations, hindfoot_symptom) and (
            any_symptom_present(mid_foot_observations, midfoot_symptom))):
        path += ' -> True for Hindfoot and Midfoot -> IS POST TIB ALWAYS ON?'
        resp = yes_or_no('IS POST TIB ALWAYS ON?')
        if resp == 'y':
            path += ' -> Yes -> Treatment Recommended'
            treatment = 'Z-Lengthening of Post Tib'
            return path, treatment
        elif resp == 'n':
            path += ' -> No -> No Treatment Recommended'
            treatment = 'No Treatment Recommendation'
            return path, treatment
        else:
            print("Choose Input Wisely")
    elif any_symptom_present(hind_foot_observations, hindfoot_symptom):
        path += ' -> True for Hindfoot -> IS POST TIB OUT OF PHASE?'
        resp = yes_or_no('IS POST TIB OUT OF PHASE?')
        if resp == 'y':
            path += ' -> Yes -> Treatment Recommended'
            treatment = 'Myofascial Lengthening of Post Tib'
            return path, treatment
        elif resp == 'n':
            path += ' -> No -> No Treatment Recommended'
            treatment = 'No Treatment Recommendation'
            return path, treatment
        else:
            print("Choose Input Wisely")
    elif any_symptom_present(hind_foot_observations, hindfoot_symptom):
        path += ' -> True for Hindfoot -> Foot Supple'
        if data['LeftFootSupple'] == 'N' or data['RightFootSupple'] == 'N':
            path += ' -> No -> Treatment Recommended'
            treatment = 'Lateral Column Shortening and Z-Lenghtening of Post Tib'
            return path, treatment
        elif data['LeftFootSupple'] == 'Y' or data['RightFootSupple'] == 'Y':
            path += ' -> Yes -> No Treatment Recommended'
            treatment = 'No Treatment Recommendation'
            return path, treatment
        else:
            print("Choose Input Wisely")
    else:
        path += ' -> Else -> No Treatment Recommended'
        treatment = 'No Treatment Recommendation'
        return path, treatment


def investigate_varus(data, path):
    path += ' -> Pattern Of Involvement'
    if data['PatternOfInvolvement'] == 'Hemiplegia':
        path += ' -> Hemiplegia'
        return investigate_hemiplegia(data, path)
    elif data['PatternOfInvolvement'] == 'Diplegia':
        path += ' -> Diplegia'
        return investigate_diplegia(data, path)
    else:
        path += ' -> Wrong value of Pattern Of Involvement -> Unable to determine treatment'
        print("PatternOfInvolvement value is wrong, so unable to reach conclusion")
        treatment = 'Unable to determine treatment'
        return path, treatment


def case_lessthan_5(data, path):
    path += ' -> Treatment Recommended'
    treatment = 'Prescribe an AFO'
    return path, treatment


def case_between_5_10(data, path):
    path += ' -> Foot Supple and Tolerating AFO'
    if (data['LeftFootSupple'] == 'Y' or data['RightFootSupple'] == 'Y') and (
            data['LeftOrthoticTolerated'] == 'Yes' or data['RightOrthoticTolerated'] == 'Yes'):
        path += ' -> Yes -> Treatment Recommended'
        treatment = 'Continue AFO'
        return path, treatment
    else:
        path += ' -> No -> Foot Position'
        hind_foot_observations = get_foot_wt_bearing_observation(data, 'hindfoot')
        valgus_hindfoot_symptom = [SYMPTOMS_DEF[x] for x in ['Valgus', 'Mild Valgus']]
        varus_hindfoot_symptom = [SYMPTOMS_DEF[x] for x in ['Varus', 'Mild Varus']]
        if any_symptom_present(hind_foot_observations, valgus_hindfoot_symptom):
            path += ' -> Any Valgus'
            return investigate_valgus(data, path)
        elif any_symptom_present(hind_foot_observations, varus_hindfoot_symptom):
            path += ' -> Any Varus'
            return investigate_varus(data, path)
        else:
            path += ' -> Foot Position value is wrong -> Unable to determine treatment'
            print("Foot Position value is wrong, so unable to reach conclusion")
            treatment = 'Unable to determine treatment'
            return path, treatment


def case_morethan_10(data, path):
    fore_foot_observations = get_foot_wt_bearing_observation(data, 'forefoot')
    mid_foot_observations = get_foot_wt_bearing_observation(data, 'midfoot')
    hind_foot_observations = get_foot_wt_bearing_observation(data, 'hindfoot')

    varus_forefoot_symptom = [SYMPTOMS_DEF[x] for x in
                              ['Add', 'Mild Add', 'Supination', 'Mild Supination', 'Varus', 'Mild Varus']]
    varus_midfoot_symptom = [SYMPTOMS_DEF[x] for x in ['Cavus', 'Varus', 'Supination']]
    varus_hindfoot_symptom = [SYMPTOMS_DEF[x] for x in ['Varus', 'Mild Varus']]

    valgus_forefoot_symptom = [SYMPTOMS_DEF[x] for x in
                               ['Abd', 'Mild Abd', 'Pronation', 'Mild Pronation', 'Valgus', 'Mild Valgus']]
    valgus_midfoot_symptom = [SYMPTOMS_DEF[x] for x in
                              ['Low Arch', 'Midfoot Break', 'Planovalgus', 'Planus', 'Mild Planus', 'Valgus',
                               'Mild Valgus', 'Pronation', 'Rocker Bottom']]
    valgus_hindfoot_symptom = [SYMPTOMS_DEF[x] for x in ['Valgus', 'Mild Valgus', 'Equinus', 'Mild Equinus']]

    resp = None
    path += ' -> Foot Position -> Varus'
    if any_symptom_present(fore_foot_observations, varus_forefoot_symptom) or any_symptom_present(mid_foot_observations,
                                                                                                  varus_midfoot_symptom) or any_symptom_present(
        hind_foot_observations, varus_hindfoot_symptom):
        path += ' -> True for any -> Foot Supple'
        if data['LeftFootSupple'] == 'Y' or data['RightFootSupple'] == 'Y':
            while resp not in {"y", "n"}:
                path += ' -> Yes -> IS TIB ANT OUT OF PHASE OR ALWAYS ON?'
                resp = yes_or_no('IS TIB ANT OUT OF PHASE OR ALWAYS ON?', 'y - OUT OF PHASE/n - ALWAYS ON')
                if resp == 'y':
                    path += ' -> Yes -> Treatment Recommended'
                    treatment = 'Split Transfer of Tibialis Anterior (SPLATT)'
                    return path, treatment
                elif resp == 'n':
                    path += ' -> No -> IS POSTERIOR TIBIALIS OUT OF PHASE OR ALWAYS ON?'
                    resp = yes_or_no('IS POSTERIOR TIBIALIS OUT OF PHASE OR ALWAYS ON?',
                                     'y - OUT OF PHASE/n - ALWAYS ON')
                    if resp == 'y':
                        path += ' -> Yes -> Treatment Recommended'
                        treatment = 'Split Transfer OF Posterior Tibialis (SPOTT)'
                        return path, treatment
                    elif resp == 'n':
                        path += ' -> No -> Ankle Inversion < 15?'
                        if data['LeftAnkleRomInver'] < 15 or data['RightAnkleRomInver'] < 15:
                            path += ' -> Yes -> Treatment Recommended'
                            treatment = 'Posterior Tibialis Z-Lengthening'
                            return path, treatment
                        else:
                            path += ' -> Else -> No Treatment Recommended'
                            treatment = 'No Treatment Recommendation'
                            return path, treatment
                    else:
                        print("Choose Input Wisely")
                else:
                    print("Choose Input Wisely")
        else:
            path += ' -> No, Fixed Deformity -> HOW SEVERE IS THE FOOT DEFORMITY?'
            resp = moderate_or_severe_or_else('HOW SEVERE IS THE FOOT DEFORMITY?',
                                              'm - Moderate/s - Severe/e - Else')
            if resp == 'm':
                path += ' -> Moderate -> Treatment Recommended'
                treatment = 'Calcaneal Osteotomy'
                return path, treatment
            elif resp == 's':
                path += ' -> Severe -> Treatment Recommended'
                treatment = 'Triple Arthrodesis or talectomy'
                return path, treatment
            else:
                path += ' -> Else -> No Treatment Recommended'
                treatment = 'No Treatment Recommendation'
                return path, treatment
    elif any_symptom_present(fore_foot_observations, valgus_forefoot_symptom) or any_symptom_present(
            mid_foot_observations, valgus_midfoot_symptom) or any_symptom_present(hind_foot_observations,
                                                                                  valgus_hindfoot_symptom):
        path += ' -> False for all -> Foot Position -> Valgus -> True for any'
        gmfcs = int(data['GmfcsNew'])
        if gmfcs == 1 or gmfcs == 2:
            path += ' -> GMFCS LEVEL 1 or 2'
            return investigate_gmfcs_level12_morethan10(data, path)
        elif gmfcs == 3 or gmfcs == 4:
            path += ' -> GMFCS LEVEL 3 or 4'
            return investigate_gmfcs_level34_morethan10(data, path)
        else:
            path += ' -> GMFCS LEVEL is wrong -> Unable to determine treatment'
            print("GNFCS value is wrong, so unable to reach conclusion")
            treatment = 'Unable to determine treatment'
            return path, treatment
    else:
        path += ' -> False for all -> Foot Position -> Valgus -> False for all -> No Treatment Recommended'
        treatment = 'No Treatment Recommendation'
        return path, treatment