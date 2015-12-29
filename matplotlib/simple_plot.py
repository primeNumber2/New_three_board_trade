import numpy as np
import matplotlib.pyplot as plt

def simple_plot():
    X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    C, S = np.cos(X), np.sin(X)
    plt.plot(X, C, X, S)
    plt.show()


# 上面是一个最简单的图形，但是实际上使用了很多的默认值，下面把这些默认值手工定义出来
def initial_defaults():
    plt.figure(num=1, figsize=(8, 6), dpi=80)
    plt.subplot(111)
    X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    C, S = np.cos(X), np.sin(X)
    plt.plot(X, C, color="green", linewidth=1.0, linestyle="-")
    plt.plot(X, S, color="red", linewidth=1.0, linestyle="-")
    plt.xlim(-4.0, 4.0)
    plt.xticks(np.linspace(-4, 4, 9, endpoint=True))
    plt.ylim(-1.0, 1.0)
    plt.yticks(np.linspace(-1, 1, 5, endpoint=True))
    plt.show()

# initial_defaults()
# 下面改变默认的坐标值，并使用LaTex排版显示数学符号
def set_labels():
    plt.figure(num=1, figsize=(8, 6), dpi=80)
    plt.subplot(111)
    X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    C, S = np.cos(X), np.sin(X)
    plt.plot(X, C, color="green", linewidth=1.0, linestyle="-", label='cosine')
    plt.plot(X, S, color="red", linewidth=1.0, linestyle="-", label='sine')
    # plt.xlim(-4.0, 4.0)
    plt.xlim(X.min()*1.1, X.max()*1.1)
    # plt.xticks(np.linspace(-4, 4, 9, endpoint=True))
    plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi], [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$\pi/2$', r'$\pi$'])
    # plt.ylim(-1.0, 1.0)
    plt.ylim(C.min()*1.1, C.max()*1.1)
    plt.yticks(np.linspace(-1, 1, 5, endpoint=True))

    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))

    plt.legend(loc='upper left', frameon=True)

    t = 2*np.pi/3
    plt.plot([t, t], [0, np.cos(t)], color='green', linewidth=2.5, linestyle="--")
    plt.plot([t, t], [0, np.sin(t)], 'r--', linewidth=2.5)
    plt.scatter([t,], [np.cos(t)], s=50, color='green')
    plt.scatter([t,], [np.sin(t)], s=50, color='red')
    plt.annotate(r'$sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$', xy=(t, np.sin(t)), xycoords='data',
                 xytext=(+10, +30), textcoords='offset points', fontsize=16,
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=.2'))
    plt.annotate(s=r'$cos(\frac{2\pi}{3})=-\frac{1}{2}$', xy=(t, np.cos(t)), xycoords='data', xytext=(-90, -50),
                 textcoords='offset points', fontsize=16, arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=.2'))
    plt.show()
set_labels()