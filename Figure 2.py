import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymannkendall as mk
import seaborn as sns
from sklearn.linear_model import LinearRegression
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import xarray as xr
import warnings
from PIL import Image
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
warnings.filterwarnings('ignore')
lonmin, lonmax = -180, 180
latmin, latmax = -60, 90
extents = [lonmin, lonmax, latmin, latmax]


def Figure2a():
    def draw_picture(slope, p, title):
        proj = ccrs.PlateCarree()
        fig = plt.figure(figsize=(5, 2.5))

        plt.rcParams['xtick.direction'] = 'out'
        plt.rcParams['ytick.direction'] = 'out'
        ax = fig.add_subplot(111, projection=proj)
        ax.grid(zorder=0, ls='--', which='both', alpha=0.25, lw=0.75)
        ax.tick_params(top=False, bottom=True,
                       labeltop=False, labelbottom=True)
        ax.set_global()

        # 设置经纬度刻度.
        ax.axis('off')
        ax.tick_params(labelsize='small')
        plt.xticks(family='serif')
        plt.yticks(family='serif')
        colorK = plt.get_cmap('RdYlBu')(np.linspace(0, 1, 300))
        colorneed = colorK[[i for i in range(120)] + [180 + i for i in range(120)]]
        im = ax.contourf(
            data.lon.data, data.lat.data, slope,
            levels=[-4 + 4 / 120 * i for i in range(240)],
            colors=colorneed,
            extend='both',
            alpha=1,
            zorder=10
        )

        ax.coastlines(resolution='110m', lw=0.3, color='#191970', zorder=10)

        X, Y = [], []
        a1, a2, a3, a4 = 0, 0, 0, 0
        for i in range(len(data.lon.data)):
            for j in range(len(data.lat.data)):
                if p[j, i] < 0.05:
                    X.append(i)
                    Y.append(j)
                    if slope[j, i] <= 0:
                        a1 = a1+1
                    else:
                        a4 = a4+1
                else:
                    if slope[j, i] <= 0:
                        a2 = a2+1
                    else:
                        a3 = a3+1
        ax.scatter(data.lon.data[X], data.lat.data[Y], c='purple', s=0.05, zorder=10, marker='*', linewidths=0.008)

        ax.set_extent(extents, crs=proj)

        ax.text(0.5, 1.00, title, fontfamily='serif', fontsize=15,
                horizontalalignment='center', verticalalignment='bottom', transform=ax.transAxes)
        A = a1+a2+a3+a4

        # 条形图
        plt.rcParams['xtick.direction'] = 'inout'
        plt.rcParams['ytick.direction'] = 'inout'
        ax3 = fig.add_axes([0.1, 0.23, 0.15, 0.35])
        ax3.spines[['right', 'top']].set_visible(False)
        rects = ax3.bar(x=[1, 2, 3, 4], height=[a1/A, a2/A, a3/A, a4/A],
                        color=[colorneed[0], colorneed[59], colorneed[179], colorneed[239]])

        ax3.set_ylim([0, 1])
        ax3.set_xlim([0.4, 4.6])
        plt.yticks([0, 0.2, 0.4, 0.6, 0.8], ['0', '20', '40', '60', '80'], fontfamily='serif', fontsize=8)
        plt.xticks([1, 2, 3, 4], ['SD', 'D', 'I', 'SI'], fontfamily='serif', fontsize=8)
        ax3.patch.set_alpha(0)

        ax_colorbar = fig.add_subplot(15, 10, (141, 149))
        cbar = fig.colorbar(im, cax=ax_colorbar, orientation='horizontal')
        cbar.ax.tick_params(bottom=True, tickdir='in', labelsize=7.5)
        cbar.set_ticks([-4 + 0.5 * i for i in range(17)])
        labels = cbar.ax.get_xticklabels() + cbar.ax.get_yticklabels()
        [label.set_fontname('serif') for label in labels]

        plt.text(1.03, -0.022, '(mm yr$^{-2}$)', fontfamily='serif',
                 transform=ax_colorbar.transAxes, fontsize=8,
                 horizontalalignment='left', verticalalignment='top')

        fig.patch.set_alpha(1.0)
        plt.tight_layout()
        plt.subplots_adjust(
            top=0.98,
            bottom=0.08,
            left=0.045,
            right=0.97,
            hspace=0.2,
            wspace=0.2)
        plt.rcParams['savefig.dpi'] = 3000
        plt.show()

    name = ["BNEMS", "BNMS", "BREMSC", "BRMSC"]
    D = np.zeros((360, 720, 4))
    P = np.zeros((360, 720, 4))
    for i in [0, 1, 2, 3]:
        d = pd.read_csv("dataset\Trend\\"+name[i]+"_OBS.csv")
        D[:, :, i] = np.array(d)[:, 1:]
        d = pd.read_csv("dataset\Trend\\" + name[i] + "_OBS_p_value.csv")
        P[:, :, i] = np.array(d)[:, 1:]
        data = xr.open_dataset("dataset/BNMS_TRENDY_runoff.nc")
    slope = np.median(D, axis=2)
    p = np.median(P, axis=2)
    draw_picture(slope, p, title='Trend pattern')
Figure2a()

def Figure2b():
    k = 6
    trendy_name = ['CABLE_POP', 'CLASSIC', 'CLM5', 'DLEM', 'IBIS', 'ISAM',
                   'ISBA_CTRIP', 'JSBACH', 'JULES', 'LPJ_GUESS', 'LPX_Bern', 'ORCHIDEE',
                   'SDGVM', 'VISIT_NIES']
    name = ["BNEMS", "BNMS", "BREMSC", "BRMSC"]
    fig = plt.figure(figsize=(5, 2.5))
    # colors = ['#9D0048', '#F39700', '#3D7D53', '#4A4B9D', '#E7242E', '#808000', '#1f77b4']
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
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.spines[['right', 'top']].set_visible(False)
    plt.yticks(fontfamily='serif')
    plt.xticks([-1, 9, 19, 29, 39], ['1980', '1990', '2000', '2010', '2020'],
               fontfamily='serif')
    plt.xlim([-3, 41])
    plt.ylim([-38, 30])
    plt.rcParams['xtick.direction'] = 'inout'
    plt.rcParams['ytick.direction'] = 'inout'
    ax1.set_ylabel('Runoff anomaly (mm yr$^{-1}$)', fontfamily='serif', fontsize=11)
    ax1.set_xlabel('Year (yr)', fontfamily='serif', fontsize=11)
    ax1.set_title("Time series and trend", loc='center', fontweight='normal', fontsize=15, fontfamily='serif')
    s = 4
    rotation = 0
    # if k in [2, 4, 5]:
    #     rotation = -45
    STREAMFLOW = np.zeros((4, 40))
    colors2 = ['#BAD5E8', '#FFD9B5', '#B9D6B3', '#F1BDBF', '#DED1EC']
    for i in range(4):
        streamflow = pd.read_excel(r"dataset\OB TRENDY runoff\\" + name[i] + "_trendy_runoff.xlsx", sheet_name='S3')
        streamflow = np.array(streamflow)[:, 1:].T
        d = streamflow[k, :] - np.mean(streamflow[k, :])
        STREAMFLOW[i, :] = d
        slope = mk.original_test(d).slope
        print(slope)
        p = mk.original_test(d).p
        x = [i for i in range(40)]
        ly = np.ravel([i * slope for i in x])
        width = 0.75
    ax1.fill_between(x, np.mean(STREAMFLOW, axis=0) + np.std(STREAMFLOW, axis=0),
                     np.mean(STREAMFLOW, axis=0) - np.std(STREAMFLOW, axis=0),
                     facecolor=colors[0], alpha=0.4)
    ax1.plot(x, np.mean(STREAMFLOW, axis=0), lw=1.0, c=colors[0], ls='-')
    plt.text(1.0, 0.04, 'Trend$=$0.09$±$0.05 (mm yr$^{-2}$) $[\mathrm{p_{min}>0.05}]$', fontfamily='serif',
             transform=ax1.transAxes, fontsize=12,
             horizontalalignment='right', verticalalignment='bottom')
    d = np.mean(STREAMFLOW, axis=0)
    slope = mk.original_test(d).slope
    print(slope)
    ly = np.ravel([i * slope for i in x])
    ax1.plot(x, ly - np.mean(ly), lw=0.75, c=colors[0], ls='--')
    ax1.patch.set_alpha(0.3)
    fig.patch.set_alpha(1.0)
    plt.tight_layout()
    plt.subplots_adjust(
        top=0.89,
        bottom=0.18,
        left=0.143,
        right=0.97,
        hspace=0.2,
        wspace=0.2
    )
    plt.rcParams['savefig.dpi'] = 2000
    plt.show()
Figure2b()

def Figure2c():
    name = ["BNEMS", "BNMS", "BREMSC", "BRMSC"]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 'k']
    plt.rcParams['xtick.direction'] = 'inout'
    plt.rcParams['ytick.direction'] = 'inout'
    fig = plt.figure(figsize=(5, 2.5))
    ax = fig.add_subplot(8,1,(2,7))
    ax1 = fig.add_subplot(8,1,1)
    ax2 = fig.add_subplot(8,1,8)
    ax1.spines[['right', 'top', 'bottom']].set_visible(False)
    ax2.spines[['right', 'top']].set_visible(False)
    ax.spines[['right', 'top', 'bottom']].set_visible(False)
    D_single, D_multi = np.zeros((3,3,4)), np.zeros((3,3,4))
    for i in range(4):
        d = pd.read_excel(r"dataset\rof_result\\"+name[i]+r"_one_component\5_years_101.xlsx")
        d_2 = np.array(d)[:3, 1:]
        d = np.copy(d_2)
        d[:, 0] = d_2[:, 1]
        d[:, 1] = d_2[:, 0]
        D_single[:, :, i] = np.copy(d)
        d = pd.read_excel(r"dataset\rof_result\\" + name[i] + r"_three_component\5_years_101.xlsx")
        d_2 = np.array(d)[:3, 1:]
        d = np.copy(d_2)
        d[:, 0] = d_2[:, 1]
        d[:, 1] = d_2[:, 0]
        D_multi[:, :, i] = np.copy(d)

    d = np.median(D_single, axis=2)
    y1 = d[1, :] - d[0, :]
    y2 = d[2, :] - d[1, :]

    x = [-0.1, 0.9, 1.9]
    ax.errorbar(x, d[1, :], color=colors[-1], markersize=3.0,
                yerr=[y1, y2],
                fmt='o', linewidth=1.5, capsize=3, label='Single-factor', zorder=5)
    ax1.errorbar(x, d[1, :], color=colors[-1], markersize=0.0,
                yerr=[y1, y2],
                fmt='o', linewidth=1.5, capsize=3, zorder=5)
    ax2.errorbar(x, d[1, :], color=colors[-1], markersize=0.0,
                yerr=[y1, y2],
                fmt='o', linewidth=1.5, capsize=3, zorder=5)

    d = .2  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=6,
                  linestyle="none", color='k', mec='k', mew=1.3, clip_on=False)
    ax.plot([0, 0], [0, 1], transform=ax.transAxes, **kwargs)
    ax1.plot([0], [0], transform=ax1.transAxes, **kwargs)
    ax2.plot([0], [1], transform=ax2.transAxes, **kwargs)

    d = np.median(D_multi, axis=2)
    x = [0.1, 1.1, 2.1]
    ax.errorbar(x, d[1, :], color=colors[3], markersize=3.0,
                yerr=[d[1, :] - d[0, :], d[2, :] - d[1, :]],
                fmt='o', linewidth=1.5, capsize=3, label='Multi-factor', zorder=5)
    ax1.errorbar(x, d[1, :], color=colors[3], markersize=0.0,
                yerr=[d[1, :] - d[0, :], d[2, :] - d[1, :]],
                fmt='o', linewidth=1.5, capsize=3, zorder=5)
    ax2.errorbar(x, d[1, :], color=colors[3], markersize=0.0,
                yerr=[d[1, :] - d[0, :], d[2, :] - d[1, :]],
                fmt='o', linewidth=1.5, capsize=3, zorder=5)

    ax.plot([-1, 3], [0, 0], lw=1.0, ls='--', c='gray', label='Zero line', alpha=0.6, zorder=0)
    ax.plot([-1, 3], [1, 1], lw=1.0, ls='--', c='r', label='Unit line', alpha=0.6, zorder=0)
    ax.set_xlim([-1, 5.5])
    ax.set_ylim([-2, 6])
    ax.set_xticks([])
    ax.set_yticks([-2, -1, 0, 1, 2, 3, 4, 5, 6], ['', -1, 0, 1, 2, 3, 4, 5, ''], family='serif', fontsize=10)
    ax1.set_xlim([-1, 5.5])
    ax1.set_ylim([6, 20])
    ax1.set_xticks([])
    ax1.set_yticks([6, 20], [6, 20], family='serif', fontsize=10)
    ax2.set_xlim([-1, 5.5])
    ax2.set_ylim([-18, -2])
    ax2.set_yticks([-18, -2], [-18, -2], family='serif', fontsize=10)
    plt.xticks([0, 1, 2], ['CLI', 'eCO$_2$', 'LUC'], family='serif', fontsize=12)
    ax.set_ylabel('Scaling factor', family='serif', fontsize=12)

    ax1.set_title("Attribution", fontfamily='serif', fontsize=15)

    handles, labels = ax.get_legend_handles_labels()
    legend_font = {
        'family': 'serif',
        'style': 'normal',
        'size': 10,
        'weight': "normal",
    }
    fig.legend(handles, labels, ncol=1, prop=legend_font,  loc='center', bbox_to_anchor=[0.82, 0.5])

    fig.patch.set_alpha(1.0)
    plt.tight_layout()
    plt.subplots_adjust(
        top=0.89,
        bottom=0.18,
        left=0.113,
        right=0.97,
        hspace=0.2,
        wspace=0.2
    )
    plt.rcParams['savefig.dpi'] = 2000
    plt.show()
Figure2c()
