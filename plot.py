import string
import seaborn as sns
import matplotlib.pyplot as plt


def plot(solution):

    l = len(solution)

    Ly = list(range(1, l + 1))[::-1]
    ly = [str(i) for i in Ly]

    Lx = list(string.ascii_uppercase)
    lx = Lx[:l]

    plt.close("all")
    plt.figure(figsize=(5, 5))

    ax = plt.gca()
    ax.set_aspect(1)

    sns.set(font_scale=1)
    sns.heatmap(
        solution,
        linewidths=0.4,
        cbar=False,
        linecolor="white",
        cmap="Reds",
        center=0.4,
        xticklabels=lx,
        yticklabels=ly,
    )
