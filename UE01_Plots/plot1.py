import matplotlib.pyplot as plt
import math

__author__ = "Luka Pacar"
__version__ = "1.0.0"

PI = math.pi
CNT = 1024
min_value = -PI
max_value = +PI
X = [ min_value + (2 * max_value * i) / (CNT-1)  for i in range(CNT)]
C = [ math.cos(x) for x in X ]
S = [ math.sin(x) for x in X ]


plt.figure(figsize=(10,6), dpi=80)
plt.plot(X, C, color="blue", linewidth=2.5, linestyle="-", label="cosine")
plt.plot(X, S, color="red", linewidth=2.5, linestyle="-", label="sine")


# X und Y Achsen Limits
plt.xlim(min(X)*1.1, max(X)*1.1)
plt.ylim(-1, 1)

# Ticks
plt.xticks([-PI, -PI/2, 0, PI/2, PI], [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
plt.yticks([0, 0.5, 1, -0.5, -1])

# Legende
plt.legend(loc='upper left', frameon=False)

# Achsen
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

# Markierungen
t = 2*PI/3
plt.plot([t,t],[0,math.cos(t)], color ='blue', linewidth=2.5, linestyle="--") # Linie zur cosinus Kurve
plt.scatter([t,],[math.cos(t),], 50, color ='blue') # Punkt auf der Kurve

# Coole Beschriftung für einen Punkt auf der Sinus Kurve
plt.annotate(r'$\sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$',
             xy=(t, math.sin(t)), xycoords='data',
             xytext=(+10, +30), textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

# Ticks größer
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(16)
    label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.65 ))

    # bei neueren matplot versionen
    ax.set_axisbelow(True)

plt.savefig("plot1_pacar.png",dpi=72) # muss vor plt.show() sein, sonst ist das Bild weiß!
plt.show() # Anzeigen: Danach kann man die Grafik nicht mehr ändern!