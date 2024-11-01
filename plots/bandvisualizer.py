import matplotlib.pyplot as mpl

def saveFigure(tm_freqs, te_freqs, tm_gaps, te_gaps):
    fig, ax = mpl.subplots()
    x = range(len(tm_freqs))
    # Plot bands
    # Scatter plot for multiple y values, see https://stackoverflow.com/a/34280815/2261298
    # for xz, tmz, tez in zip(x, tm_freqs, te_freqs):
    #     ax.scatter([xz]*len(tmz), tmz, color='blue')
    #     ax.scatter([xz]*len(tez), tez, color='red', facecolors='none')
    ax.plot(tm_freqs, color='blue')
    ax.plot(te_freqs, color='red')
    ax.set_ylim([400, 600]) #Height
    ax.set_xlim([x[0], x[-1]])

    # Plot gaps
    # for gap in tm_gaps:
    #     if gap[0] > 1:
    #         ax.fill_between(x, gap[1], gap[2], color='blue', alpha=0.2)

    # for gap in te_gaps:
    #     if gap[0] > 1:
    #         ax.fill_between(x, gap[1], gap[2], color='red', alpha=0.2)


    # Plot labels
    #ax.text(12, 0.04, 'TM bands', color='blue', size=15)
    ax.text(13.05, 0.235, 'TE bands', color='red', size=15)

    points_in_between = (len(tm_freqs) - 3) / 2
    tick_locs = [i*points_in_between+i for i in range(3)]
    tick_labs = ['K', 'Γ', 'M']
    ax.set_xticks(tick_locs)
    ax.set_xticklabels(tick_labs, size=16)
    ax.set_ylabel('Wavelength (nm)', size=16)
    ax.grid(True)

    fig.savefig("band_structure.png", dpi=150, bbox_inches="tight")