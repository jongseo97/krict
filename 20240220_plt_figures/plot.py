# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 14:43:46 2024

@author: user
"""


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#%%
# 그림 2-a

plt.rcParams['font.family'] ='Malgun Gothic'

colors = ['olivedrab', 'darkseagreen']
colors = ['#809fff', '#ccd9ff']
ratio = [4, 96]
labels = ['혼합', '단일']

fig = plt.figure(figsize=(7,7))
fig.set_facecolor('white')
ax = fig.add_subplot()

pie = ax.pie(ratio, startangle = 90, counterclock=True, colors=colors)

total = np.sum(ratio)

threshold = 5
sum_pct = 0

bbox_props = dict(boxstyle='square', fc='w', ec='w', alpha=0)

#annonation
config = dict(arrowprops=dict(arrowstyle='-'), bbox=bbox_props, va='center')

for i,l in enumerate(labels):
    ang1, ang2 = ax.patches[i].theta1, ax.patches[i].theta2
    center, r = ax.patches[i].center, ax.patches[i].r

    sum_pct += float(f'{ratio[i]:.0f}')
    text = (
        f'{labels[i]}\n '
        f'{ratio[i]:.0f}%'
        )

        
    if ratio[i]/total*100 < threshold:
        ang = (ang1 + ang2)/2
        x = np.cos(np.deg2rad(ang))
        y = np.sin(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        config["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(text, xy=(x, y), xytext=(1.5*x, 1.2*y), horizontalalignment=horizontalalignment, **config, fontsize=18)
    
    else:
        x = (r/2)*np.cos(np.pi/180*((ang1+ang2)/2)) + center[0]
        y = (r/2)*np.sin(np.pi/180*((ang1+ang2)/2)) + center[0]
        ax.text(x,y,text,ha='center',va='center',fontsize=18, color='black', weight='bold')

plt.legend(pie[0], labels, loc='upper right')
plt.show()
plt.savefig('figure2.png', dpi=600, bbox_inches = 'tight')

#%%
# 그림 2-b
plt.rcParams['font.family'] ='Arial'
name = ['MIE', 'KE', 'AO']
ratio = [72, 20, 8]
colors = ['#4d79ff', 'orange', 'tomato']
#colors = ['#809fff','#4d79ff','#ccd9ff']
#colors = ['deepskyblue']
#colors = ['c']
x_pos = [1.0, 1.5, 2]
width = 0.7

fig, ax = plt.subplots(figsize = (10, 5))
y_pos = np.arange(len(name))

hbars = ax.barh(y_pos, ratio, width, align = 'center', zorder=3, color = colors)
ax.invert_yaxis()

plt.grid(True, axis='x')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['right'].set_edgecolor('darkgrey')

ax.tick_params(labelleft = False, left=False)
plt.xticks(np.arange(0, 81, 20),fontsize=20, weight='bold')

labels = [f' {name[i]}, {ratio[i]}%' for i in range(len(name))]

ax.bar_label(hbars, labels, fontsize= 20, weight= 'bold')
plt.ylim(3, -1)

plt.savefig('figure2.png', dpi=600, bbox_inches = 'tight')
plt.show()

    
#%%
# 그림 2-c
import matplotlib.colors
plt.rcParams['font.family'] ='Arial'
# plt.rcParams['font.family'] ='Arial'
ratio = [41, 14, 12, 5, 5, 5, 2, 2, 2, 2, 2, 2, 3, 3]
ratio = [35, 12.5, 12.5, 5, 2.5, 2.5, 2.5, 2.5, 2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,5]
labels = ['Toxcast/Tox21', 'Inhouse DB', 'ChEMBL', 'PubChem DB', 'PDB', 'AOP-DB',
          'UniProt', 'UK BioBank', 'etc', 'OECD eChemPortal', 'NTP', 'EFSA DB', 'DNT-DIVER', 'AlphaFold Protein Structure Database']
labels = ['Toxcast / Tox21', 'Inhouse DB', 'ChEMBL', 'PubChem DB', 'PDB', 'AOP-DB',
          'UniProt', 'UK BioBank', 'CTD', 
          'OECD eChemPortal', 'AOPwiki', 'PRIDE', 'NTP', 'EFSA DB', 'DNT-DIVER', 'AlphaFold Protein Structure Database', 'etc']

np.random.seed(12)
cc = plt.cm.tab20c(np.linspace(0.05, 0.7, len(ratio)))
colors = cc
colors[0] = np.array(matplotlib.colors.to_rgba('#ccd9ff'))
colors[2] = colors[1]
colors[1] = np.array(matplotlib.colors.to_rgba('#409fff'))
# colors[5] = np.array(matplotlib.colors.to_rgba('#D17300'))
colors[6] = np.array(matplotlib.colors.to_rgba('#ffe6ff'))
colors[9] = np.array(matplotlib.colors.to_rgba('#FDFF9C'))
colors[10] = np.array(matplotlib.colors.to_rgba('#e6fffa'))
colors[13] = np.array(matplotlib.colors.to_rgba('#A4EEF5'))
# #colors[1] = np.array(matplotlib.colors.to_rgba('#AAFF'))


fig = plt.figure(figsize=(7,7))
fig.set_facecolor('white')
ax = fig.add_subplot()

pie = ax.pie(ratio, startangle = 90, counterclock=True, colors=colors)

total = np.sum(ratio)

threshold = 10
sum_pct = 0

bbox_props = dict(boxstyle='square', fc='w', ec='w', alpha=0)

#annonation
config = dict(arrowprops=dict(arrowstyle='-'), bbox=bbox_props, va='center')

for i,l in enumerate(labels):
    ang1, ang2 = ax.patches[i].theta1, ax.patches[i].theta2
    center, r = ax.patches[i].center, ax.patches[i].r

    sum_pct += float(f'{ratio[i]:.0f}')
    text = (
        f'{labels[i]}\n '
        f'{ratio[i]:.1f}%'
        )

        
    if ratio[i]/total*100 < threshold:
        ang = (ang1 + ang2)/2
        x = np.cos(np.deg2rad(ang))
        y = np.sin(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        config["arrowprops"].update({"connectionstyle": connectionstyle})
        if len(l) > 9:
            ax.annotate(text, xy=(x, y), xytext=(1.3*x, 1.3*y), horizontalalignment=horizontalalignment, **config, fontsize=10, weight='bold')
        elif len(l)>8:
            ax.annotate(text, xy=(x, y), xytext=(1.25*x, 1.25*y), horizontalalignment=horizontalalignment, **config, fontsize=10, weight='bold')
        else:
            ax.annotate(text, xy=(x, y), xytext=(1.2*x, 1.2*y), horizontalalignment=horizontalalignment, **config, fontsize=10, weight='bold')
    
    else:
        x = (r/2)*np.cos(np.pi/180*((ang1+ang2)/2)) + center[0]
        y = (r/2)*np.sin(np.pi/180*((ang1+ang2)/2)) + center[0] -0.05
        if l == 'ChEMBL':
            x += 0.02
        if l == 'Inhouse DB':
            x -= 0.055
            y -= 0.03
        print(l, x, y)
        ax.text(x,y,text,ha='center',va='center', fontsize=12, color='black', weight='bold')

#plt.legend(pie[0], labels, loc='upper right')
plt.savefig('figure3.png', dpi=600, bbox_inches = 'tight')
plt.show()


#%%
# 그림 2-d

plt.rcParams['font.family'] ='Arial'


ratio = [10.5, 10.5, 5, 21, 16, 16, 21]
labels = ['Neurotoxicity', 'Developmental\ntoxicity     ', 'Thyroid  \n     endocrine\ntoxicity  ', 
          'Reproductive toxicity', 'Skin sensitization', 'Respiratory\n   toxicity', 'Multi-endpoints']
colors = plt.cm.tab20c(np.linspace(0, 1, len(ratio)))
colors[0] = np.array(matplotlib.colors.to_rgba('#ccd9ff'))
colors[5] = np.array(matplotlib.colors.to_rgba('#809fff'))
explode = (0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02)

fig = plt.figure(figsize=(7,7))
fig.set_facecolor('white')
ax = fig.add_subplot()

textprops = {'fontsize':15, 'weight':'bold'}

def autopct_format(pct):
    if round(pct,1) == 10.5:
        return '%.1f%%' % pct
    else:
        return '%.0f%%' % pct

pie = ax.pie(ratio, startangle = 90, counterclock=True, colors=colors, 
       pctdistance =0.78, explode = explode, autopct = autopct_format, labels = labels, textprops=textprops)

centre_circle = plt.Circle((0,0), 0.60, fc='white')
fig = plt.gcf()

fig.gca().add_artist(centre_circle)
plt.savefig('figure4.png', dpi=600, bbox_inches = 'tight')
plt.show()




#%%
# 그림 3-a

plt.rcParams['font.family'] ='Arial'
N = 5

grey = (12, 12, 12, 12, 12)
yellow = (0, 28, 28, 28, 28)
blue = (0,0,16, 16, 16)
green = (0,0,0,32,32)
nam = (0,0,0,0,12)

ind = np.arange(N) 
width = 0.45

fig = plt.subplots(figsize =(10, 7))
p1 = plt.bar(ind, grey, width, color='darkgray')
p2 = plt.bar(ind, yellow, width, bottom = grey, color = 'orange')
p3 = plt.bar(ind, blue, width, bottom = [grey[i] + yellow[i] for i in range(N)], color= 'dodgerblue')
p4 = plt.bar(ind, green, width, bottom = [grey[i] + yellow[i] + blue[i] for i in range(N)], color = 'yellowgreen')
p5 = plt.bar(ind, nam, width, bottom = [grey[i] + yellow[i] + blue[i]+ green[i] for i in range(N)], color = 'midnightblue')

pp1 = plt.plot(ind, [6.896552,10.34483,13.7931,17.24138,20.68966], linewidth=3, color = 'tab:blue')
pp2 = plt.plot(ind, [6.896552,27.58621,41.37931,62.06897,68.96552], linewidth=3, color='tab:red')

plt.grid(True, axis='y')
plt.gca().spines['top'].set_visible(False)
#plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.ylabel('percentage', fontsize=20, weight='bold')
#plt.title('<연간 문헌 수 및 예측 기법 (%)>', fontsize = 25, weight='bold')
plt.xticks(ind, ('2019', '2020', '2021', '2022', '2023'), fontsize=20, weight='bold')
plt.yticks(np.arange(0, 101, 20),fontsize=20, weight='bold')
#plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0]), ('2019', '2020', '2021', '2022', '2023'), fontsize=13)
plt.legend((pp1[0], pp2[0]), ('Deep Learning', 'Machine Learning'), prop={'size':18, 'weight':'bold'},  loc='upper left')#,bbox_to_anchor=(0,0.99))
plt.savefig('figure5.png', dpi=600, bbox_inches = 'tight')
plt.show()

#%%
# 그림 3-b
import matplotlib.colors
plt.rcParams['font.family'] ='Arial'

fig2 = plt.subplots(figsize = (7,7))
ratio = [69, 10, 21]

labels = ['Machine learning', 'Molecular simulation', 'DL']
fake_labels = ['', 'Molecular simulation', 'Deep learning']

colors = plt.cm.turbo(np.linspace(0.3, 0.7, len(ratio)))
colors[1] = np.array(matplotlib.colors.to_rgba('#ff944d'))
#colors[0] = np.array(matplotlib.colors.to_rgba('#809fff'))
colors[0] = np.array(matplotlib.colors.to_rgba('#99bbff'))
colors[2] = np.array(matplotlib.colors.to_rgba('#66ff66'))
#plt.title('<예측 기법>', fontsize = 25, weight = 'bold')

def func(pct, ratio, labels):
    pct = round(pct)
    for i in range(3):
        if ratio[i] == pct:
            break
    if pct>25:
        print(f"{labels[i]:s}\n{pct:.0f}%")
        return f"{labels[i]:s}\n{pct:.0f}%"
    else:
        print(f"{pct:.0f}%")
        return f"{pct:.0f}%"

plt.pie(ratio, labels = fake_labels, autopct=lambda pct:func(pct,ratio,labels), startangle=90, counterclock=True, textprops = {'fontsize':18, 'weight':'bold'}, colors= colors,pctdistance=0.5)
plt.savefig('figure6.png', dpi=600, bbox_inches = 'tight')
plt.show()

#%%
# 그림 3-c

fig3 = plt.subplots(figsize = (7,7))
ratio = [19, 27, 54]
labels = ['모두 사용', '정량', '정성']
fake_labels = ['','','']
colors = plt.cm.tab20c(np.linspace(0.3, 0.7, len(ratio)))
colors[2] = np.array(matplotlib.colors.to_rgba('#d9d9d9'))
# colors[2] = np.array(matplotlib.colors.to_rgba('#809fff'))
# colors[2] = np.array(matplotlib.colors.to_rgba('#ccd9ff'))
# colors[0] = np.array(matplotlib.colors.to_rgba('#FFA500'))
# colors[1] = np.array(matplotlib.colors.to_rgba('#9ACD32'))
def func(pct, ratio, labels):
    pct = round(pct)
    for i in range(6):
        if ratio[i] == pct:
            break
    if i==0:
        return f"{labels[i]:s}   \n{pct:.0f}%  "
    if i==2:
        return f"{labels[i]:s}   \n{pct:.0f}%  "
    return f"{labels[i]:s}\n{pct:.0f}%"
   

#plt.title('<예측 결과 타입>', fontsize = 25, weight = 'bold')
plt.pie(ratio, labels = fake_labels, autopct=lambda pct:func(pct,ratio,labels), startangle=90, counterclock=True, textprops = {'fontsize':18, 'weight':'bold'}, colors=colors,pctdistance=0.55)
plt.show()