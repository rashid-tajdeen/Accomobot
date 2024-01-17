import pyAgrum
import numpy

from constants import *


class MyBayesian:
    def __init__(self, input_rent, input_size, input_type, input_univ):
        self.input_rent = input_rent
        self.input_size = input_size
        self.input_type = input_type
        self.input_univ = input_univ
        self.bn = pyAgrum.BayesNet('Student Dorm')
        self.dorm_posterior = None
        self.match_posterior = None
        self.vacancy_posterior = None

    def run(self):
        self._init_dorm_step()
        self._get_dorm_posterior()
        self._init_match_step()
        self._get_match_posterior()
        self._init_vacancy_step()
        self._get_vacancy_posterior()
        self.print_result()

    def _add_to_bn(self, name, items):
        return self.bn.add(pyAgrum.LabelizedVariable(name, name + '?', items))

    def _init_dorm_step(self):
        bn_rent_range = self._add_to_bn('rent_range', rent_range)
        bn_room_size = self._add_to_bn('room_size', room_size)
        bn_property_type = self._add_to_bn('property_type', property_type)
        bn_dorm = self._add_to_bn('dorm', dorm)

        self.bn.addArc(bn_rent_range, bn_dorm)
        self.bn.addArc(bn_room_size, bn_dorm)
        self.bn.addArc(bn_property_type, bn_dorm)

        self.bn.cpt(bn_rent_range).fillWith([0.5, 0.3, 0.2])
        self.bn.cpt(bn_room_size).fillWith([0.8, 0.2])
        self.bn.cpt(bn_rent_range).fillWith([0.65, 0.30, 0.05])

        self.bn.cpt(bn_dorm)[0, 0, 0, :] = [0.28, 0.20, 0.16, 0.12, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01]
        self.bn.cpt(bn_dorm)[0, 0, 1, :] = [0.16, 0.12, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01, 0.28, 0.20]
        self.bn.cpt(bn_dorm)[0, 0, 2, :] = [0.08, 0.06, 0.04, 0.03, 0.02, 0.01, 0.28, 0.20, 0.16, 0.12]
        self.bn.cpt(bn_dorm)[0, 1, 0, :] = [0.04, 0.03, 0.02, 0.01, 0.28, 0.20, 0.16, 0.12, 0.08, 0.06]
        self.bn.cpt(bn_dorm)[0, 1, 1, :] = [0.02, 0.01, 0.28, 0.20, 0.16, 0.12, 0.08, 0.06, 0.04, 0.03]
        self.bn.cpt(bn_dorm)[0, 1, 2, :] = [0.20, 0.16, 0.12, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01, 0.28]

        self.bn.cpt(bn_dorm)[1, 0, 0, :] = [0.12, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01, 0.28, 0.20, 0.16]
        self.bn.cpt(bn_dorm)[1, 0, 1, :] = [0.06, 0.04, 0.03, 0.02, 0.01, 0.28, 0.20, 0.16, 0.12, 0.08]
        self.bn.cpt(bn_dorm)[1, 0, 2, :] = [0.03, 0.02, 0.01, 0.28, 0.20, 0.16, 0.12, 0.08, 0.06, 0.04]
        self.bn.cpt(bn_dorm)[1, 1, 0, :] = [0.01, 0.28, 0.20, 0.16, 0.12, 0.08, 0.06, 0.04, 0.03, 0.02]
        self.bn.cpt(bn_dorm)[1, 1, 1, :] = [0.28, 0.20, 0.16, 0.12, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01]
        self.bn.cpt(bn_dorm)[1, 1, 2, :] = [0.16, 0.12, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01, 0.28, 0.20]

        self.bn.cpt(bn_dorm)[2, 0, 0, :] = [0.08, 0.06, 0.04, 0.03, 0.02, 0.01, 0.28, 0.20, 0.16, 0.12]
        self.bn.cpt(bn_dorm)[2, 0, 1, :] = [0.04, 0.03, 0.02, 0.01, 0.28, 0.20, 0.16, 0.12, 0.08, 0.06]
        self.bn.cpt(bn_dorm)[2, 0, 2, :] = [0.02, 0.01, 0.28, 0.20, 0.16, 0.12, 0.08, 0.06, 0.04, 0.03]
        self.bn.cpt(bn_dorm)[2, 1, 0, :] = [0.20, 0.16, 0.12, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01, 0.28]
        self.bn.cpt(bn_dorm)[2, 1, 1, :] = [0.12, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01, 0.28, 0.20, 0.16]
        self.bn.cpt(bn_dorm)[2, 1, 2, :] = [0.06, 0.04, 0.03, 0.02, 0.01, 0.28, 0.20, 0.16, 0.12, 0.08]

    def _get_dorm_posterior(self):
        ie = pyAgrum.LazyPropagation(self.bn)
        ie.setEvidence({'rent_range': self.input_rent,
                        'room_size': self.input_size,
                        'property_type': self.input_type})
        ie.makeInference()
        bn_dorm = self.bn.idFromName("dorm")
        self.dorm_posterior = ie.posterior(bn_dorm).tolist()

    def _init_match_step(self):
        bn_university = self._add_to_bn('university', university)
        bn_match = self._add_to_bn('match', match)
        bn_dorm = self.bn.idFromName("dorm")
        self.bn.addArc(bn_dorm, bn_match)
        self.bn.addArc(bn_university, bn_match)
        self.bn.cpt(bn_university).fillWith([0.35, 0.20, 0.45])

        for d in range(len(dorm)):
            for uni in range(len(university)):
                value = self.dorm_posterior[d] * self.bn.cpt(bn_university)[uni]
                self.bn.cpt(bn_match)[uni, d, :] = [value, 1 - value]

    def _get_match_posterior(self):
        bn_match = self.bn.idFromName("match")
        match_posterior = []
        ie = pyAgrum.LazyPropagation(self.bn)
        for d in range(len(dorm)):
            ie.setEvidence({'rent_range': self.input_rent,
                            'room_size': self.input_size,
                            'property_type': self.input_type,
                            'university': self.input_univ,
                            'dorm': d})
            ie.makeInference()
            match_posterior.append(ie.posterior(bn_match).tolist()[0])  # taking only "yes" cases
        self.match_posterior = match_posterior

    def _init_vacancy_step(self):
        bn_vacancy = self._add_to_bn('vacancy', vacancy)
        bn_dorm = self.bn.idFromName("dorm")
        self.bn.addArc(bn_dorm, bn_vacancy)

        vacancy_details = [0.05, 0.10, 0.04, 0.06, 0.05, 0.02, 0.07, 0.06, 0.04, 0.03]
        for d in range(len(dorm)):
            value = vacancy_details[d] * self.match_posterior[d]
            self.bn.cpt(bn_vacancy)[d, :] = [value, 1 - value]

    def _get_vacancy_posterior(self):
        bn_vacancy = self.bn.idFromName("vacancy")
        vacancy_posterior = []
        ie = pyAgrum.LazyPropagation(self.bn)
        for d in range(len(dorm)):
            ie.setEvidence({'rent_range': self.input_rent,
                            'room_size': self.input_size,
                            'property_type': self.input_type,
                            'university': self.input_univ,
                            'dorm': d})
            ie.makeInference()
            vacancy_posterior.append(ie.posterior(bn_vacancy).tolist()[0])  # taking only "vacant" cases

        self.vacancy_posterior = [float(elem)/sum(vacancy_posterior) for elem in vacancy_posterior]

    def print_result(self):
        print("")
        print("###########################################################")
        print("List of Dorms matched and ordered based on your preferences")
        print("###########################################################")
        match_order = numpy.argsort(self.match_posterior)[::-1]
        for count, idx in enumerate(match_order):
            percent = numpy.round(self.match_posterior[idx] * 100, 2)
            print(f'   {count+1}. {dorm[idx]} ({percent} %)')

        print("")
        print("#############################################################")
        print("Chances available to receive and appointment based on vacancy")
        print("#############################################################")
        vacancy_order = numpy.argsort(self.vacancy_posterior)[::-1]
        for count, idx in enumerate(vacancy_order):
            percent = numpy.round(self.vacancy_posterior[idx] * 100, 2)
            print(f'   {count+1}. {dorm[idx]} ({percent} %)')


if __name__ == "__main__":
    myBayesian = MyBayesian(0, 0, 0, 0)
    myBayesian.run()


