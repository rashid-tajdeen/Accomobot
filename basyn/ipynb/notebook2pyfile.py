# Importing Related Libraries

import pyAgrum as gum
import pyAgrum.lib.notebook as gnb

# Creating the network
bn = gum.BayesNet('Student Wohnheim')

# Adding the related nodes and correspondence
University = bn.add(gum.LabelizedVariable('University', 'University',['HBRS_Sankt_Augustin', 'HBRS_Rheinbach', 'University_of_Bonn']))
Location = bn.add(gum.LabelizedVariable('Location', 'Location',['Sankt_Augustin', 'Rheinbach', 'Bonn']))
#'Near', 'Mid-Range', 'Far', 'Very_Far'
Distance = bn.add(gum.LabelizedVariable('Distance', 'Distance',['Near','Far']))
#'Single_Room', 'Dobule_Room', 'Semi-Apartment','Apartment', 'Double_Apartment', 'Differently Abled Friendly Apartment'
Property_Type = bn.add(gum.LabelizedVariable('Property_Type', 'Property_Type',['Single_Room','Apartment']))
#'300', '400', '500', '600', '700', '800', '900'
Max_Rental = bn.add(gum.LabelizedVariable('Max_Rental', 'Max_Rental',['Between_300_600','Between_600_900']))
# Remove_Availability
# Availability = bn.add(gum.LabelizedVariable('Availability', 'Availability',['Yes', 'No']))
# MAke sure always return a statement of your room confiramtion will be sent as a mail within a week.
Student_Dom_List = bn.add(gum.LabelizedVariable('Student_Dom_List', 'Student_Dom_List',['WOHNHEIM_BONN', 'WOHNHEIM_RHEINBACH', 'WOHNHEIM_SANKT_AUGUSTIN']))
# hey 
# Adding the arcs
bn.addArc(University, Distance)
bn.addArc(Location, Distance)

# I feel these are unnecessary arcs as the distance is already given in the location
# bn.addArc(University, Property_Type)
# bn.addArc(University, Max_Rental)

bn.addArc(Property_Type, Student_Dom_List)
bn.addArc(Max_Rental, Student_Dom_List)
# bn.addArc(Distance, Availability)
bn.addArc(Distance,Student_Dom_List)
# bn.addArc(Availability, Student_Dom_List)

gnb.showBN(bn, size="10")

# Trail_2
# Adding CPT's

bn.cpt(Location).fillWith([0.3334,0.3333,0.3333])
bn.cpt(University).fillWith([0.3334,0.3333,0.3333])
bn.cpt(Max_Rental).fillWith([0.6,0.4])
bn.cpt(Property_Type).fillWith([0.5,0.5])

# LHS - Part of the BN Chart
# For Based on the distance the probability is given
bn.cpt(Distance)[{'Location': 'Sankt_Augustin','University':'HBRS_Sankt_Augustin'}] = [0.7,0.3]
bn.cpt(Distance)[{'Location': 'Rheinbach','University': 'HBRS_Sankt_Augustin'}] = [0.6,0.4]
bn.cpt(Distance)[{'Location': 'Bonn','University': 'HBRS_Sankt_Augustin'}] = [0.4,0.6]

bn.cpt(Distance)[{'Location': 'Sankt_Augustin','University': 'HBRS_Rheinbach'}] = [0.6,0.4]
bn.cpt(Distance)[{'Location': 'Rheinbach','University': 'HBRS_Rheinbach'}] = [0.7,0.3]
bn.cpt(Distance)[{'Location': 'Bonn','University': 'HBRS_Rheinbach'}] = [0.4,0.6]

bn.cpt(Distance)[{'Location': 'Sankt_Augustin','University': 'University_of_Bonn'}] = [0.3,0.7]
bn.cpt(Distance)[{'Location': 'Rheinbach','University': 'University_of_Bonn'}] = [0.4,0.6]
bn.cpt(Distance)[{'Location': 'Bonn','University': 'University_of_Bonn'}] = [0.8,0.2]

# RHS - Part of the BN Chart
# For based on the availability the probability is given below
bn.cpt(Availability)[{'Max_Rental': 'Between_300_600','Property_Type': 'Single_Room'}] = [0.7,0.3]
bn.cpt(Availability)[{'Max_Rental': 'Between_300_600','Property_Type': 'Apartment'}] = [0.3,0.7]

bn.cpt(Availability)[{'Max_Rental': 'Between_600_900','Property_Type': 'Single_Room'}] = [0.4,0.6]
bn.cpt(Availability)[{'Max_Rental': 'Between_600_900','Property_Type': 'Apartment'}] = [0.8,0.2]

# Final Node

bn.cpt(Student_Dom_List)[{'Distance': 'Near','Availability': 'Yes'}] =  [0.7,0.15,0.15]
bn.cpt(Student_Dom_List)[{'Distance': 'Near','Availability': 'No'}] = [0.6,0.05,0.35]
bn.cpt(Student_Dom_List)[{'Distance': 'Far','Availability': 'Yes'}] = [0.2,0.4,0.4]
bn.cpt(Student_Dom_List)[{'Distance': 'Far','Availability':'No'}] = [0.8,0.15,0.05]

bn.check()
# Below commented are used to visualize the probability values given
# bn.cpt(Distance)
# bn.cpt(Student_Dom_List)
# bn.cpt(Location)


# Inference With Evidence

ie = gum.LazyPropagation(bn)
ie.makeInference()
ie.setEvidence({'Location':'Sankt_Augustin','University': 'HBRS_Sankt_Augustin','Max_Rental': 'Between_300_600','Property_Type': 'Single_Room','Distance': 'Near', 'Availability': 'Yes'})
ie.makeInference()
ie.posterior(Student_Dom_List)

print(ie.posterior(Student_Dom_List))
gnb.showInference(bn,evs={},size='10')
