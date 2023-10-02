import random as rd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os
import glob
import matplotlib.cm as cm
import scipy.special as ss
plt.rcParams['text.usetex'] = True
mpl.use('Agg')


N = 15                  #nombre de pendules
theta = np.radians(30)  #angle initial
T0 = 40                 #nombre de périodes du plus grand pendule L0 avant 1er période d'ensemble
L0 = 2                #plus grande tige
g = 9.81
R = 0.1

L = [L0]
for i in range(1, N):
    L.append(L0 * (T0/(T0+i))**2 )  #longueur des tiges

L =np.array(L)
dt = 0.01       #pas
tf = 75        #temps

d = 1.5

pas_img = 2
digit = 4

def name(i,digit):

    i = str(i)

    while len(i)<digit:
        i = '0'+i

    i = 'img/'+i+'.png'

    return(i)

def init(t):

    vec = []
    for i in range(N):
        vec.append(np.zeros((2, t.shape[0])))
        vec[i][0, 0] = theta

    return vec

def a(vec_k, k):
    return np.array([vec_k[1], - g/L[k] * np.sin(vec_k[0])])

def rk4(derivee, step, fin):

    t = np.arange(0,fin,step)
    N_g = []

    vec = np.array(init(t))
    l_t = t.shape[0] - 1

    k = 0
    color_array_tot = []

    for i in range(l_t):

        for k in range(N):

            d1 = derivee(vec[k, :, i], k)
            d2 = derivee(vec[k, :, i] + d1 * step / 2, k)
            d3 = derivee(vec[k, :, i] + d2 * step / 2, k)
            d4 = derivee(vec[k, :, i] + d3 * step, k)
            vec[k,:, i + 1] = vec[k,:, i] + step / 6 * (d1 + 2 * d2 + 2 * d3 + d4)

    return vec, t

#initialisation des coefficients

vec, t = rk4(a, dt, tf)

print("RK4 sucessed")

extension="img/*.png"
for f in glob.glob(extension):
  os.remove(f)

arr = np.linspace(-d, d, N)
for i in range(0, t.shape[0] - 1, pas_img):
#for i in range(0, 1):

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    ax.set_xlim( -d, d)        #limite x
    ax.set_ylim( -d, d)       #limite y
    ax.set_zlim(-2*d, 0)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.view_init(-2, 0)
    ax.set_ylabel("Pendulum wave by @maximev1314", labelpad=0)

    X = L * np.sin(vec[:, 0, i])
    Y = - L * np.cos(vec[:, 0, i])

    #ax.scatter(arr, X , Y, s = 200, c = L, cmap = cm.jet, alpha = 1)
    for k in range(N):
        ax.plot([arr[k], arr[k]], [0, X[k]], [0, Y[k]], color = 'black', zorder = 0)

        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = R * np.cos(u)*np.sin(v) + arr[k]
        y = R * np.sin(u)*np.sin(v) + X[k]
        z = R * np.cos(v) + Y[k]
        ax.plot_surface(x, y, z, color = cm.jet( 1 - k/N))


    ax2 = fig.add_subplot(4, 4, 8)
    ax2.set_xlim( - 3, 3)        #limite x
    ax2.set_ylim( - 3, 3)       #limite y
    ax2.set_aspect('equal', adjustable='box')
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])
    ax2.set_title(r'$\theta$')
    ax2.set_ylabel(r'$\dot{\theta}$', labelpad=0)
    ax2.grid()

    ax2.scatter(vec[:, 0, i], vec[:, 1, i], s = 10, c = L, cmap = cm.jet, zorder = 2)

    ax3 = fig.add_subplot(4, 4, 12)
    ax3.set_xlim( - 3, 3)        #limite x
    ax3.set_ylim( - 4, 2)       #limite y
    ax3.set_aspect('equal', adjustable='box')
    ax3.set_xticklabels([])
    ax3.set_yticklabels([])
    ax3.set_xlabel(r'$x$', labelpad=0)
    ax3.set_ylabel(r'$z$', labelpad=0)
    ax3.grid()

    ax3.scatter(arr, Y, c = L, cmap = cm.jet, zorder = 2)

    name_pic = name(int(i/pas_img), digit)
    plt.savefig(name_pic, bbox_inches='tight', dpi=300)

    ax.clear()
    ax2.clear()
    ax3.clear()
    plt.close(fig)

    print(i/t.shape[0])

print("img sucessed")

# ffmpeg -i img/%04d.png -r 30 -pix_fmt yuv420p hexagon.mp4
# ffmpeg -r 50 -i img/%04d.png -vcodec libx264 -y -an test.mp4 -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" (if 'width not divisible by two' error)
# ffmpeg -r 10 -i img/%04d.png -vcodec libx264 -y -an test.mp4 -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" (if 'width not divisible by two' error)
