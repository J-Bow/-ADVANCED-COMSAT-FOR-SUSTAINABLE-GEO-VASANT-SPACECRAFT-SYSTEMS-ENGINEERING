from Solar_panel import solar_panel, cart_to_pol, pol_to_cart
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation 
def polar_plot(r, theta):
    x_data = [0 for i in range(len(r))]
    y_data = [0 for i in range(len(theta))]
    for i in range(len(r)):
        x_data[i], y_data[i] = pol_to_cart(r[i], theta[i]*(2*np.pi/360))
    return x_data,y_data
# Coordinates are taken from middle of VASANT, when it's vertically orientated

# Case 1
panel_1 = solar_panel(0, 56)
panel_2 = solar_panel(0, 31)
panel_3 = solar_panel(0, 6)
panel_4 = solar_panel(0, -6)
panel_5 = solar_panel(0, -31)
panel_6 = solar_panel(0, -56)
panel_7 = solar_panel(0, 25)
panel_8 = solar_panel(0, 0)
panel_9 = solar_panel(0, -25)
"""
#Case 2
panel_1 = solar_panel(11, 56)
panel_2 = solar_panel(-11, 31)
panel_3 = solar_panel(0, 6)
panel_4 = solar_panel(0, -6)
panel_5 = solar_panel(-11, -31)
panel_6 = solar_panel(11, -56)
panel_7 = solar_panel(11, 0)
panel_8 = solar_panel(0, 0)
panel_9 = solar_panel(-11, 0)
"""
list_of_panels_1 = [panel_1, panel_2, panel_3, panel_4, panel_5, panel_6 ]
list_of_panels_2 = [panel_7, panel_8, panel_9]
increment = 1
step_size = increment *(2*np.pi/360)        # conversion to radians
angles = [i for i in range(int(0/increment),int(360/increment))]  # theta
SA_size = []
position = [[] for i in range(len(list_of_panels_1)) ]
j=-1
top = [] # stores the area of the top panel
bot = [] # stores area of the bottom panels

#used to check the positions
for i in list_of_panels_1:
    j+=1
    for theta in angles:
        i.update(step_size)
        position[j].append([pol_to_cart(i.r, i.theta)])
        if abs(((pol_to_cart(i.r, i.theta)[0]**2 +pol_to_cart(i.r, i.theta)[1]**2)**0.5)-i.r) > 0.001:
            print()
index = -1

#used to find the area
for theta in angles:
    index += 1
    SA_size =[]
    for panel in list_of_panels_1:
        panel.update(step_size)    
        x,y = pol_to_cart(panel.r, panel.theta)
        print(x,y)
        SA_size.append([x, [y, y-5,y+5]]) #[x, [y, bottom of panel, top of panel]
    for i in SA_size:       # i is the array that shadows the array j
        for j in SA_size:
            if i[0] > j[0]:
                if j[1][1] <= i[1][2] and j[1][1] >= i[1][1]:     #checks if the bottom of back panel is inbetween the edges of the front panel
                    if j[1][2] < i[1][2]:
                        j[1][1] = j[1][2]
                    else:
                        j[1][1] = i[1][2]
                elif j[1][2] <= i[1][2] and j[1][2] >= i[1][1]:     #checks if the top of back panel is inbetween the edges of the front panel
                    if j[1][1] > i[1][1]:
                        j[1][2] = j[1][1]
                    else:
                        j[1][2] = i[1][1]
    Areas = [(((SA_size[i][1][1]-SA_size[i][1][2])**2)**0.5) for i in range(len(SA_size))] # makes an array of each arrays area
    top.append(Areas)

    SA_size = []
    for panel in list_of_panels_2:
        panel.update(step_size)
        x,y = pol_to_cart(panel.r, panel.theta)
        SA_size.append([x, [y, y-5,y+5]]) #[x, [y, bottom of panel, top of panel]
    temp_sort = []
    for i in SA_size:       # i is the array that shadows the array j
        for j in SA_size:
            if i[0] > j[0]:
                if j[1][1] <= i[1][2] and j[1][1] >= i[1][1]:     #checks if the bottom of back panel is inbetween the edges of the front panel
                    if j[1][2] < i[1][2]:
                        j[1][1] = j[1][2]
                    else:
                        j[1][1] = i[1][2]
                elif j[1][2] <= i[1][2] and j[1][2] >= i[1][1]:     #checks if the top of back panel is inbetween the edges of the front panel
                    if j[1][1] > i[1][1]:
                        j[1][2] = j[1][1]
                    else:
                        j[1][2] = i[1][1]
    Areas = [(((SA_size[i][1][1]-SA_size[i][1][2])**2)**0.5) for i in range(len(SA_size))] # makes an array of each arrays area
    bot.append(Areas)


average = np.mean([((sum(bot[_])+sum(top[_]))*10/9) for _ in range(len(bot))])
plt.figure("lit area", figsize = (10, 6))
plt.plot([angles[_]*increment for _ in range(len(angles))], [((sum(bot[_])+sum(top[_]))*10/9) for _ in range(len(bot))], label = r"Case 1", color = 'green')
#plt.plot([angles[_]*increment for _ in range(len(angles))], [(200/3) for _ in range(len(angles))], color = 'red', linestyle = '--', label = 'Best-worst case')
plt.plot([angles[_]*increment for _ in range(len(angles))], [average for _ in range(len(angles))], color = 'limegreen', linestyle = '--', label = r'Case 1 Average')

#Case 2
panel_1 = solar_panel(11, 56)
panel_2 = solar_panel(-11, 31)
panel_3 = solar_panel(0, 6)
panel_4 = solar_panel(0, -6)
panel_5 = solar_panel(-11, -31)
panel_6 = solar_panel(11, -56)
panel_7 = solar_panel(11, 0)
panel_8 = solar_panel(0, 0)
panel_9 = solar_panel(-11, 0)

list_of_panels_1 = [panel_1, panel_2, panel_3, panel_4, panel_5, panel_6 ]
list_of_panels_2 = [panel_7, panel_8, panel_9]
increment = 1
step_size = increment *(2*np.pi/360)        # conversion to radians
angles = [i for i in range(int(0/increment),int(360/increment))]  # theta
SA_size = []
position = [[] for i in range(len(list_of_panels_1)) ]
j=-1
top = [] # stores the area of the top panel
bot = [] # stores area of the bottom panels

#used to check the positions
for i in list_of_panels_1:
    j+=1
    for theta in angles:
        i.update(step_size)
        position[j].append([pol_to_cart(i.r, i.theta)])
        if abs(((pol_to_cart(i.r, i.theta)[0]**2 +pol_to_cart(i.r, i.theta)[1]**2)**0.5)-i.r) > 0.001:
            print()
index = -1

#used to find the area
for theta in angles:
    index += 1
    SA_size =[]
    for panel in list_of_panels_1:
        panel.update(step_size)    
        x,y = pol_to_cart(panel.r, panel.theta)
        print(x,y)
        SA_size.append([x, [y, y-5,y+5]]) #[x, [y, bottom of panel, top of panel]
    for i in SA_size:       # i is the array that shadows the array j
        for j in SA_size:
            if i[0] > j[0]:
                if j[1][1] <= i[1][2] and j[1][1] >= i[1][1]:     #checks if the bottom of back panel is inbetween the edges of the front panel
                    if j[1][2] < i[1][2]:
                        j[1][1] = j[1][2]
                    else:
                        j[1][1] = i[1][2]
                elif j[1][2] <= i[1][2] and j[1][2] >= i[1][1]:     #checks if the top of back panel is inbetween the edges of the front panel
                    if j[1][1] > i[1][1]:
                        j[1][2] = j[1][1]
                    else:
                        j[1][2] = i[1][1]
    Areas = [(((SA_size[i][1][1]-SA_size[i][1][2])**2)**0.5) for i in range(len(SA_size))] # makes an array of each arrays area
    top.append(Areas)

    SA_size = []
    for panel in list_of_panels_2:
        panel.update(step_size)
        x,y = pol_to_cart(panel.r, panel.theta)
        SA_size.append([x, [y, y-5,y+5]]) #[x, [y, bottom of panel, top of panel]
    temp_sort = []
    for i in SA_size:       # i is the array that shadows the array j
        for j in SA_size:
            if i[0] > j[0]:
                if j[1][1] <= i[1][2] and j[1][1] >= i[1][1]:     #checks if the bottom of back panel is inbetween the edges of the front panel
                    if j[1][2] < i[1][2]:
                        j[1][1] = j[1][2]
                    else:
                        j[1][1] = i[1][2]
                elif j[1][2] <= i[1][2] and j[1][2] >= i[1][1]:     #checks if the top of back panel is inbetween the edges of the front panel
                    if j[1][1] > i[1][1]:
                        j[1][2] = j[1][1]
                    else:
                        j[1][2] = i[1][1]
    Areas = [(((SA_size[i][1][1]-SA_size[i][1][2])**2)**0.5) for i in range(len(SA_size))] # makes an array of each arrays area
    bot.append(Areas)


average = np.mean([((sum(bot[_])+sum(top[_]))*10/9) for _ in range(len(bot))])


plt.figure("lit area", figsize = (10, 6))
rect = plt.Rectangle([171,0], 18, 1000, alpha = 0.5, color = 'lightgrey')
plt.gca().add_patch(rect)
plt.text(175,40, "Eclipse",fontsize = 18, rotation = 90, alpha = 0.7)
plt.plot([angles[_]*increment for _ in range(len(angles))], [((sum(bot[_])+sum(top[_]))*10/9) for _ in range(len(bot))], label = r"Case 2", color = 'royalblue')

plt.plot([angles[_]*increment for _ in range(len(angles))], [average for _ in range(len(angles))], color = 'cornflowerblue', linestyle = '--', label = r'Case 2 averaage')
plt.plot([angles[_]*increment for _ in range(len(angles))], [(200/3) for _ in range(len(angles))], color = 'red', linestyle = '--', label = 'Best-worst case')
#plt.plot([angles[_]*increment for _ in range(len(angles))], [297 for _ in range(len(angles))])
plt.axis([0, 360, 20, 100])
plt.xlabel(r"True Anomaly/$^{\circ}$ ", fontsize = 15)
plt.ylabel(r"% Solar arrays illuminated", fontsize = 15)
plt.grid(axis = 'x', linestyle = ':')
#plt.text(250,60, "Worst case = 66.6%",fontsize = 15, rotation = 0)
plt.xticks(range(0,361, 90), fontsize = 15)
plt.yticks(fontsize = 15)
plt.legend()
"""
plt.figure('orbit')
#plt.plot(polar_plot([((sum(bot[_])+sum(top[_]))*10/9)*4.157 for _ in range(len(bot))],  [angles[_]*increment for _ in range(len(angles))]))
#plt.plot(polar_plot([(200/3)*4.157 for _ in range(len(angles))], [angles[_]*increment for _ in range(len(angles))]))
plt.plot(polar_plot([415.7 for _ in range(len(angles))], [angles[_]*increment for _ in range(len(angles))]))
"""

"""
plt.figure("lit area 2")
plt.plot([angles[_]*increment for _ in range(len(angles))], [sum(bot[_]) for _ in range(len(bot))])

plt.figure()
for i in range(len(top[0])):
    #plt.figure(i)

    plt.plot([angles[_]*increment for _ in range(len(angles))], [(top[j][i-1]-top[j][i])*10 for j in range(len(top))], label = i)
"""


"""
plt.figure("traces, y")
plt.plot(angles, [position[0][i][0][1] for i in range(len(position[0]))], color = 'red')
plt.plot(angles, [position[1][i][0][1] for i in range(len(position[1]))], color = 'blue')
plt.plot(angles, [position[2][i][0][1] for i in range(len(position[2]))], color = 'black')

plt.figure("traces, x")
plt.plot(angles, [position[0][i][0][0] for i in range(len(position[0]))], color = 'red')
plt.plot(angles, [position[1][i][0][0] for i in range(len(position[1]))], color = 'blue')
plt.plot(angles, [position[2][i][0][0] for i in range(len(position[2]))], color = 'black')
"""
#plt.figure("x-y")
#for j in range(len(position)):
 #   plt.plot([position[j][i][0][0] for i in range(len(position[0]))], [position[j][i][0][1] for i in range(len(position[0]))])






plt.show()