
import numpy as np
import matplotlib.pyplot as plt
 
# set width of bar
barWidth = 0.2
fig = plt.subplots(figsize =(12, 8))
 
# set height of bar
ratio  = [2.6,1.58,1.45,1.29, 1.09]
# num_turns = [475,76,142,108,50]
# avg_turn = [1.55,21.48,21.12,51.09,22.55]
energy = [19486,11361,10797,9590,7600]

for i in range(len(ratio)):
    ratio[i] *= (1/2.6)

# for i in range(len(num_turns)):
#     num_turns[i] *= (1/475)

# for i in range(len(avg_turn)):
#     avg_turn[i] *= (1/51.09)

for i in range(len(energy)):
    energy[i] *= (1/19486)
 
# Set position of bar on X axis
br1 = np.arange(len(ratio))
# br2 = [x + barWidth for x in br1]
# br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br1]
 
# Make the plot
plt.bar(br1, ratio, color ='c', width = barWidth,
        edgecolor ='grey', label ='Distance Ratio')
# plt.bar(br2, num_turns, color ='g', width = barWidth,
#         edgecolor ='grey', label ='Number of Turns')
# plt.bar(br3, avg_turn, color ='m', width = barWidth,
#         edgecolor ='grey', label ='Average Turn Angle')
plt.bar(br4, energy, color ='orange', width = barWidth,
        edgecolor ='grey', label ='Energy Used (mAh)')
 
# Adding Xticks
plt.xlabel('Algorithm', fontweight ='bold', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(ratio))],
        ['Circles', 'Circles w/ Waypts', 'Follow Edge', 'Greedy', 'A*'])
 
plt.legend()
plt.show()