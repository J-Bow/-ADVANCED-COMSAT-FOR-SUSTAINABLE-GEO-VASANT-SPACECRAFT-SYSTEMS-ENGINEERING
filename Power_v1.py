import matplotlib.pyplot as plt
import matplotlib.patches
from Solar_Panel_v1 import solar_panel
import numpy as np
import copy
from pandas import DataFrame
import pandas as pd
"""
Variables input from Excel
"""
#maximum capacity of a trip [number of panels]
Max_carry = 6

#period between trips [months]
T_trip = 3

#Numebr of arrasy on VII
SA_VII = 9

#Number of solar panels per array
SP_VII = 10

"""
Other variables
"""
#Maximum number of panels on VII
Max_panels = SA_VII * SP_VII

#Specifc Energy [W/kg] for BoL of panels
Spec_E = 43.3

#The planned lifetime of delivered panels [years]
Life_VII = 10  # why are we saying 10???

#The age of panels when they are received [years]
Age_VII = 15

"""
Initialising the Power needs of the system over time
"""
#VI age at VII operation [years]
T_VII_Op = 15

#VI age at start of upgrade [years]
T_VI_Up = 10


#VI age at VII EoL [years]
T_EoL = 45

#Power demand from VII [kW]
P_VII = 416

#Power demand from VI [kW]
P_VI = P_VII*2/3

"""
Initialising the solar panel properties (VI)
"""
#VI inherent degredation
VI_inherent = 0.77 #0.0172 

#VI lifetime degredation factor
VI_deg = 0.005

#VI total panel area needed [m^2]
VI_total_area = P_VI*1000/(0.92*1418*0.3*VI_inherent*(1-VI_deg)**(T_VII_Op)) #constant inherent degredation, Constant lifetime degredation factor ((1-VI_inherent)**(T_VII_Op))

#Number of solar panels on VI
N_VI_panels = int(Max_panels*2/3)

#Area of each VI panel [m^2]
A_VI = VI_total_area/N_VI_panels

#15 year of life power [W]
VI_BoL_power = 0.92*1418*0.3*VI_inherent*(1-VI_deg)**(T_VII_Op)*A_VI

#VI solar panel mass [kg]
M_VI = VI_BoL_power/Spec_E

"""
Initialisng the solar panel properties (VII)
"""
#VII inherent degredation
VII_inherent =  0.77 #0.0172

#VII lifetime degredation
VII_deg = 0.005 

#Area of each VII panel (set up as 5kW at the end of 10 years)
A_VII = 5000/(0.92*1418*0.3*VII_inherent*(1-VII_deg)**(Age_VII+Life_VII)) #((1-VII_inherent)**(Age_VII+Life_VII))

#15 year of life power [W]
VII_BoL_power =0.92*1418*0.3*VII_inherent*(1-VII_deg)**(Age_VII)*A_VII

#VII solar panel mass [kg]
M_VII = VII_BoL_power/Spec_E

"""
List of panels set up.
"""
#Starting panel list
list_of_panels = [solar_panel(A_VI,0,0,0.3, VI_inherent, VI_deg,0,0, Spec_E) for i in range(0,N_VI_panels)]

"""
Data structure of schedule
[[, Number of new panels, number of panels to be replaced], []]
"""


#schedule set up
end = int(T_EoL*12/T_trip)
schedule = [[T_VI_Up*12+i*T_trip,0,0] for i in range(0, end)]

for i in range(2,16):
    schedule[i][1]=2
"""
Simulation + optimisation
"""
#Array of time steps [months]
T_array = [i for i in range(0,T_EoL *12)]

#Array of powers ouput for each time step [kW]
P_array = [0 for i in range(len(T_array))]
Thermal_array =[0 for i in range(len(T_array))]
Mass_array =[0 for i in range(len(T_array))]

#Array to store the minimum discrete power step at each timestep
min_P = []
temp_Thermal = []
temp_Mass = []


for t in T_array:
    temp_P = []
    temp_Mass = []
    for panel in list_of_panels:
        panel.update()
        temp_P.append(panel.P_out)
        temp_Thermal.append(1418*panel.Area-panel.P_out)
        temp_Mass.append(panel.mass)
    P_array[t] = sum(temp_P)
    Thermal_array[t] = sum(temp_Thermal)
    min_P.append(min(temp_P))
    Mass_array[t] = (sum(temp_Mass))
    temp_P = []

    #if t >= T_VI_Up*12 and t < T_VII_Op*12:
        

    if t >= T_VII_Op*12:
        toggle = False
        for i in range(len(schedule)):
            if t == schedule[i][0]:
                while toggle == False:
                    temp_P = []
                    temp_LoP = copy.deepcopy(list_of_panels)
                    for j in [solar_panel(A_VII, Age_VII, 0, 0.3, VII_inherent, VII_deg,0,0, Spec_E) for h in range(0, schedule[i][1])]:
                        temp_LoP.append(j) 
                    for j in range(0,schedule[i][2]):
                        del temp_LoP[j]
                    for j in [solar_panel(A_VII, Age_VII, 0, 0.3, VII_inherent, VII_deg,0,0, Spec_E) for h in range(0,schedule[i][2])]:
                        temp_LoP.append(j)  
                    for a in range(0,T_trip):
                        for panel in temp_LoP:
                            panel.update()
                    for panel in temp_LoP:    
                        temp_P.append(panel.P_out)
                    if sum(temp_P)-min(temp_P) < P_VII:    
                        if len(temp_LoP) < Max_panels:
                            schedule[i][1] = schedule[i][1] + 1
                        elif len(temp_LoP) >= Max_panels:
                            schedule[i][2] = schedule[i][2] + 1
                    if schedule[i][1]+schedule[i][2] >= Max_carry:
                        toggle = True
                    if sum(temp_P)-min(temp_P) >= P_VII: 
                        toggle = True
        
    for i in range(len(schedule)):
        if t == schedule[i][0]:    
            for j in [solar_panel(A_VII, Age_VII, 0, 0.3, VII_inherent, VII_deg,0,0, Spec_E) for h in range(0, schedule[i][1])]:
                list_of_panels.append(j) 
            for j in range(0,schedule[i][2]):
                del list_of_panels[j]
            for j in [solar_panel(A_VII, Age_VII, 0, 0.3, VII_inherent, VII_deg,0,0, Spec_E) for h in range(0,schedule[i][2])]:
                list_of_panels.append(j) 



df = pd.DataFrame(data = schedule, columns= ['Time', 'Add', 'Replace'])
pd.DataFrame(df).to_csv("trip_index.csv")

plt.figure("VASANT Power over time", figsize= (15,6))        
plt.plot([T_array[x]/12 for x in range(len(T_array))], [P_VI for i in range(len(T_array))], color = 'grey', linestyle='-', alpha = 0.5, label = 'V-I power demand ' )
plt.plot([T_array[x]/12 for x in range(len(T_array))], [min_P[i]+(P_VI) for i in range(len(min_P))], color = 'grey', linestyle = '--', label = 'V-I power demand and margin')
plt.plot([T_array[x]/12 for x in range(len(T_array))], [P_VII for i in range(len(T_array))], color = 'black', linestyle='-', alpha = 0.5, label = 'V-II power demand ')
plt.plot([T_array[x]/12 for x in range(len(T_array))], [min_P[i]+(P_VII) for i in range(len(min_P))], color = 'black', linestyle = '--', label = 'V-II power demand and margin')
plt.axis([0, T_EoL , 250, 450])
plt.grid(axis = 'x', linestyle = ':')
rect = plt.Rectangle([10,0], 5, 1000, alpha = 0.5, color = 'lightgrey')
plt.gca().add_patch(rect)
plt.text(12,275, "VASANT I - VASANT II",fontsize = 20, rotation = 90, alpha = 0.7)
Text = 270
#plt.text(30, Text, r'Variables', fontsize=10)
#plt.text(30, Text - 10,  'trip time = {0} months'.format(T_trip))
#plt.text(30, Text - 20,  'trip time = {0} months'.format(T_trip))

plt.plot([T_array[x]/12 for x in range(len(T_array))], P_array, color = 'blue', label = 'Max power')
plt.xlabel('time/years', fontsize = 20)
plt.ylabel('Power/kW', fontsize = 20)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
plt.legend(fontsize = 15)

plt.figure("VASANT Power over time - post upgrade", figsize= (15,6))        
#plt.plot([T_array[x]/12 for x in range(len(T_array))], [P_VI for i in range(len(T_array))], color = 'grey', linestyle='-', alpha = 0.5, label = 'V-I power demand' )
#plt.plot([T_array[x]/12 for x in range(len(T_array))], [min_P[i]+(P_VI) for i in range(len(min_P))], color = 'grey', linestyle = '--', label = 'V-I power demand and margin')
plt.plot([T_array[x]/12 for x in range(len(T_array))], [P_VII for i in range(len(T_array))], color = 'black', linestyle='-', alpha = 0.5, label = 'V-II power demand' )
plt.plot([T_array[x]/12 for x in range(len(T_array))], [min_P[i]+(P_VII) for i in range(len(min_P))], color = 'black', linestyle = '--', label = 'V-II power demand and margin')
plt.axis([15, T_EoL , 410, 430])
plt.grid(axis = 'x', linestyle = ':')
rect = plt.Rectangle([10,0], 5, 1000, alpha = 0.5, color = 'lightgrey')
plt.gca().add_patch(rect)
plt.text(12,275, "VASANT I - VASANT II",fontsize = 20, rotation = 90, alpha = 0.7)
Text = 270
#plt.text(30, Text, r'Variables', fontsize=10)
#plt.text(30, Text - 10,  'trip time = {0} months'.format(T_trip))
#plt.text(30, Text - 20,  'trip time = {0} months'.format(T_trip))

plt.plot([T_array[x]/12 for x in range(len(T_array))], P_array, color = 'blue', label = 'Max power')
plt.xlabel('time/years', fontsize = 20)
plt.ylabel('Power/kW', fontsize = 20)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
plt.legend(fontsize = 15)
#plt.figure("thermal")
#plt.plot([T_array[x]/12 for x in range(len(T_array))], Thermal_array)
"""
plt.figure("Solar panels")
plt.axis([0, T_EoL, 0, Max_carry])
plt.bar([schedule[x][0]/12 for x in range(len(schedule))], [schedule[x][1] for x in range(len(schedule))], alpha = 0.5, width =(T_trip)/12, edgecolor = 'black')
plt.bar([schedule[x][0]/12 for x in range(len(schedule))], [schedule[x][2] for x in range(len(schedule))], alpha = 0.5, width =(T_trip)/12, edgecolor = 'black')
plt.xlabel('time/years')
plt.xticks(range(0,T_EoL, 1))
plt.grid(axis = 'x', linestyle = ':')
plt.ylabel('Number of panels')
"""
plt.figure("Solar panels trip index", figsize= (15,6))
#plt.axis([0, T_EoL, 0, Max_carry])
plt.bar([(schedule[x][0]- 10*12)/(T_trip)  for x in range(len(schedule))], [schedule[x][1] for x in range(len(schedule))], alpha = 0.5, width =1, edgecolor = 'black', label = 'Addition')
plt.bar([(schedule[x][0]- 10*12)/(T_trip)  for x in range(len(schedule))], [schedule[x][2] for x in range(len(schedule))], alpha = 0.5, width =1, edgecolor = 'black', label = 'Replacement')
plt.xlabel('trip number', fontsize = 20)
plt.xticks(range(0,len(schedule), 5))
plt.yticks(range(0,3, 1))
#plt.xticks(range(0,100, 1), [])
plt.ylabel('Number of panels', fontsize = 20)
plt.grid(axis = 'x', linestyle = ':')
plt.axis([0, 141, 0, 2])
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 20)
plt.legend(fontsize = 20)
"""
plt.figure("Mass")
plt.plot([T_array[x]/12 for x in range(len(T_array))], Mass_array)
plt.xlabel('time/years')
plt.ylabel('Total solar panel mass/kg')
"""
plt.show()
