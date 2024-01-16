import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymannkendall as mk
from PIL import Image

def Figure3a():
    k = -1
    name = ["BNEMS", "BNMS", "BREMSC", "BRMSC"]
    trendy_name = ['CABLE_POP', 'CLASSIC', 'CLM5', 'DLEM', 'IBIS', 'ISAM',
                   'ISBA_CTRIP', 'JSBACH', 'JULES', 'LPJ_GUESS', 'LPX_Bern', 'ORCHIDEE',
                   'SDGVM', 'VISIT_NIES']
    fig = plt.figure(figsize=(4, 4))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    SLOPE, P = [], []
    RUNOFF = np.zeros((len(trendy_name), 40))
    for i in range(len(trendy_name)):
        s = pd.read_excel(r"dataset\TRENDY\\" + trendy_name[i] + "_runoff.xlsx", sheet_name='S3')
        s = np.array(s)[:, 1:].T
        d = s[k, :]
        RUNOFF[i, :] = d - np.mean(d)
        slope = mk.original_test(d).slope
        p = mk.original_test(d).p
        SLOPE.append(slope)
        P.append(p)
    plt.rcParams['xtick.direction'] = 'inout'
    plt.rcParams['ytick.direction'] = 'inout'
    ax = fig.add_subplot(111)
    ax.spines[['right', 'top']].set_visible(False)
    STREAMFLOW = np.zeros((4, 40))
    colors2 = ['#BAD5E8', '#FFD9B5', '#B9D6B3', '#F1BDBF', '#DED1EC']
    SLOPE2 = []
    for i in range(4):
        streamflow = pd.read_excel(r"dataset\OB TRENDY runoff\\" + name[i] + "_trendy_runoff.xlsx", sheet_name='S3')
        streamflow = np.array(streamflow)[:, 1:].T
        d = streamflow[k, :] - np.mean(streamflow[k, :])
        STREAMFLOW[i, :] = d
        slope = mk.original_test(d).slope
        p = mk.original_test(d).p
        SLOPE2.append(slope)
    width = 0.5
    pr = ax.bar(0, np.mean(SLOPE2),
                  width=width,
                  yerr=[[np.std(SLOPE2)], [np.std(SLOPE2)]],
                  facecolor=colors2[0], edgecolor=colors[0], linewidth=1.5,
                  alpha=1, error_kw={'linewidth': 1.5, 'ecolor': colors[0]})
    d = np.mean(STREAMFLOW, axis=0)
    pr = ax.bar(1, np.mean(SLOPE),
                  width=width,
                  yerr=[[np.std(SLOPE)], [np.std(SLOPE)]],
                  facecolor=colors2[1], edgecolor=colors[1], alpha=1, linewidth=1.5,
                  error_kw={'linewidth': 1.5, 'ecolor': colors[1]})
    plt.xlim([-0.7, 1.7])
    plt.ylim([-0.01, 0.31])
    plt.xticks([0, 1], ['Observation\nconstrained', 'Unconstrained'], fontfamily='serif', fontsize=12)
    plt.yticks([0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.30], fontfamily='serif', fontsize=10)
    plt.ylabel("Trend (mm yr$^{-2}$)", fontfamily='serif', fontsize=12)
    plt.title("Annual trend", loc='center', fontfamily='serif', fontsize=15)
    ax.patch.set_alpha(0.3)
    fig.patch.set_alpha(1.0)
    plt.tight_layout()
    plt.subplots_adjust(
        # top=0.89,
        # bottom=0.21,
        # left=0.17,
        # right=0.84,
        # hspace=0.0,
        # wspace=0.0
    )
    plt.rcParams['savefig.dpi'] = 2000
    plt.show()
Figure3a()

def Figure3b():
    labels = ['Best-VAS-EM', 'Best-VAS-SM', 'Best-TAS-EM', 'Best-TAS-SM', 'TRENDYs\n(Mean$±1\sigma$)']
    con_name = ['Asia', 'North America', 'Europe', 'Africa', 'South America', 'Oceania', 'Global']
    data = pd.read_csv(r"dataset\rof_result\\" + con_name[-1] + "_contribution.csv")
    data = np.array(data)[:, 1:] / 300
    d_trendy = data[:, 4:]
    d_trendy = np.float64(d_trendy)
    mean_trendy = np.mean(d_trendy, axis=1)
    std_trendy = np.std(d_trendy, axis=1)
    d_ob = data[:, :4]
    d_ob = np.float64(d_ob)
    mean_ob = np.mean(d_ob, axis=1)
    std_ob = np.std(d_ob, axis=1)

    data_new = np.zeros((6, 2))
    data_new[:, 0] = mean_ob
    data_new[:, 1] = mean_trendy
    std_value = np.zeros((6, 2))
    std_value[:, 0] = std_ob
    std_value[:, 1] = std_trendy
    fig = plt.figure(figsize=(5, 4))
    plt.rcParams['xtick.direction'] = 'inout'
    plt.rcParams['ytick.direction'] = 'inout'
    ax = fig.add_subplot(111)
    ax.spines[['right', 'top']].set_visible(False)
    markersize = 4
    plt.errorbar(y=data_new[:3, 0], x=[1.5, 1.0, 2.0], ls='', marker='o', markersize=markersize, yerr=std_value[:3, 0], color='#1f77b4')
    plt.errorbar(y=data_new[:3, 1], x=[1.6, 1.1, 2.1], ls='', marker='o', markersize=markersize, yerr=std_value[:3, 1], color='#ff7f0e')

    plt.errorbar(y=data_new[3:, 0], x=[3.5, 3.0, 4.0], ls='', marker='o', markersize=markersize, yerr=std_value[3:, 0], color='#1f77b4', label='Observation constrained')
    plt.errorbar(y=data_new[3:, 1], x=[3.6, 3.1, 4.1], ls='', marker='o', markersize=markersize, yerr=std_value[3:, 1], color='#ff7f0e', label='Unconstrained')

    plt.xlim([0.5, 4.6])
    plt.ylim([-0.2, 1.5])
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0], ['0', '20', '40', '60', '80', '100'], fontsize=10, fontfamily='serif')
    plt.xticks([1.05, 1.55, 2.05, 3.05, 3.55, 4.05],
               ['CLI', 'eCO$_2$', 'LUC', 'CLI', 'eCO$_2$', 'LUC'], fontsize=12, fontfamily='serif')
    plt.ylabel('Probability (%)', fontsize=12, fontfamily='serif')
    plt.title("Attribution", loc='center', fontfamily='serif', fontsize=15)
    fig.text(0.76, 0.01, 'Multi factor', fontfamily='serif',
             # transform=ax1.transAxes,
             fontsize=15,
             horizontalalignment='center', verticalalignment='bottom')
    fig.text(0.36, 0.01, 'Single factor', fontfamily='serif',
             # transform=ax1.transAxes,
             fontsize=15,
             horizontalalignment='center', verticalalignment='bottom')

    legend_font = {
        'family': 'serif',
        'style': 'normal',
        'size': 11,
        'weight': "normal",
    }
    plt.legend(prop=legend_font, ncol=1)
    fig.patch.set_alpha(1.0)
    plt.tight_layout()
    plt.subplots_adjust(
        top=0.904,
        bottom=0.144,
        left=0.148,
        right=0.97,
        hspace=0.2,
        wspace=0.2)
    plt.rcParams['savefig.dpi'] = 1500
    plt.show()
# Figure3b()
