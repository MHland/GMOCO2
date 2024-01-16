import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from matplotlib.pyplot import MultipleLocator
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import xarray as xr
import warnings
from PIL import Image
warnings.filterwarnings('ignore')
lonmin, lonmax = -180, 180
latmin, latmax = -60, 90
extents = [lonmin, lonmax, latmin, latmax]

data = pd.read_csv(r"dataset\observation_based_approach_result.csv")
name = data['Name']
lon, lat = data['Lon'], data['Lat']
index = np.ravel(data['Index'])

# case = 1: 1116 catchments
# case = 2: 550 catchments
case = 1
if case==1:
    P, Ep, CO2 = np.zeros((1116, 4)), np.zeros((1116, 4)), np.zeros((1116, 4))

    P[:, 0] = np.ravel(data['PET_FAO_P_contribution'])
    P[:, 1] = np.ravel(data['PET_FAO_YANG_P_contribution'])
    P[:, 2] = np.ravel(data['PET_PT_P_contribution'])
    P[:, 3] = np.ravel(data['PET_HargreavesSamani_P_contribution'])

    Ep[:, 0] = np.ravel(data['PET_FAO_Ep_contribution'])
    Ep[:, 1] = np.ravel(data['PET_FAO_YANG_Ep_contribution'])
    Ep[:, 2] = np.ravel(data['PET_PT_Ep_contribution'])
    Ep[:, 3] = np.ravel(data['PET_HargreavesSamani_Ep_contribution'])

    CO2[:, 0] = np.ravel(data['PET_FAO_CO2_contribution'])
    CO2[:, 1] = np.ravel(data['PET_FAO_YANG_CO2_contribution'])
    CO2[:, 2] = np.ravel(data['PET_PT_CO2_contribution'])
    CO2[:, 3] = np.ravel(data['PET_HargreavesSamani_CO2_contribution'])

    P_per = np.abs(P)/(np.abs(P)+np.abs(Ep)+np.abs(CO2))
    Ep_per = np.abs(Ep)/(np.abs(P)+np.abs(Ep)+np.abs(CO2))
    CO2_per = np.abs(CO2)/(np.abs(P)+np.abs(Ep)+np.abs(CO2))

    P_per = np.nanmedian(P_per, axis=1)
    Ep_per = np.nanmedian(Ep_per, axis=1)
    CO2_per = np.nanmedian(CO2_per, axis=1)

    AC = np.zeros((1116, 3))
    AC[:, 0] = P_per
    AC[:, 1] = Ep_per
    AC[:, 2] = CO2_per
    AC[np.isnan(AC)] = 0

    P_per = P/(np.abs(P)+np.abs(Ep)+np.abs(CO2))
    Ep_per = Ep/(np.abs(P)+np.abs(Ep)+np.abs(CO2))
    CO2_per = CO2/(np.abs(P)+np.abs(Ep)+np.abs(CO2))

    P_per = np.nanmedian(P_per, axis=1)
    Ep_per = np.nanmedian(Ep_per, axis=1)
    CO2_per = np.nanmedian(CO2_per, axis=1)

    RC = np.zeros((1116, 3))
    RC[:, 0] = P_per
    RC[:, 1] = Ep_per
    RC[:, 2] = CO2_per
    RC[np.isnan(RC)] = 0

    data = pd.read_excel(r"dataset\result.xlsx")
    lon = data['Lon']
    lat = data['Lat']
    climates = data['Main_climate']
    pasture = data['pasture']
    forest = data['forest']
    others = data['Others']

else:
    P, Ep, CO2 = np.zeros((550, 4)), np.zeros((550, 4)), np.zeros((550, 4))

    P[:, 0] = np.ravel(data['PET_FAO_P_contribution'])[index==1]
    P[:, 1] = np.ravel(data['PET_FAO_YANG_P_contribution'])[index==1]
    P[:, 2] = np.ravel(data['PET_PT_P_contribution'])[index==1]
    P[:, 3] = np.ravel(data['PET_HargreavesSamani_P_contribution'])[index==1]

    Ep[:, 0] = np.ravel(data['PET_FAO_Ep_contribution'])[index==1]
    Ep[:, 1] = np.ravel(data['PET_FAO_YANG_Ep_contribution'])[index==1]
    Ep[:, 2] = np.ravel(data['PET_PT_Ep_contribution'])[index==1]
    Ep[:, 3] = np.ravel(data['PET_HargreavesSamani_Ep_contribution'])[index==1]

    CO2[:, 0] = np.ravel(data['PET_FAO_CO2_contribution'])[index==1]
    CO2[:, 1] = np.ravel(data['PET_FAO_YANG_CO2_contribution'])[index==1]
    CO2[:, 2] = np.ravel(data['PET_PT_CO2_contribution'])[index==1]
    CO2[:, 3] = np.ravel(data['PET_HargreavesSamani_CO2_contribution'])[index==1]

    P_per = np.abs(P) / (np.abs(P) + np.abs(Ep) + np.abs(CO2))
    Ep_per = np.abs(Ep) / (np.abs(P) + np.abs(Ep) + np.abs(CO2))
    CO2_per = np.abs(CO2) / (np.abs(P) + np.abs(Ep) + np.abs(CO2))

    P_per = np.nanmedian(P_per, axis=1)
    Ep_per = np.nanmedian(Ep_per, axis=1)
    CO2_per = np.nanmedian(CO2_per, axis=1)

    AC = np.zeros((550, 3))
    AC[:, 0] = P_per
    AC[:, 1] = Ep_per
    AC[:, 2] = CO2_per
    AC[np.isnan(AC)] = 0

    P_per = P / (np.abs(P) + np.abs(Ep) + np.abs(CO2))
    Ep_per = Ep / (np.abs(P) + np.abs(Ep) + np.abs(CO2))
    CO2_per = CO2 / (np.abs(P) + np.abs(Ep) + np.abs(CO2))

    P_per = np.nanmedian(P_per, axis=1)
    Ep_per = np.nanmedian(Ep_per, axis=1)
    CO2_per = np.nanmedian(CO2_per, axis=1)

    RC = np.zeros((550, 3))
    RC[:, 0] = P_per
    RC[:, 1] = Ep_per
    RC[:, 2] = CO2_per
    RC[np.isnan(RC)] = 0

    data = pd.read_excel(r"dataset\result.xlsx")
    lon = np.ravel(data['Lon'])[index==1]
    lat = np.ravel(data['Lat'])[index==1]
    climates = np.ravel(data['Main_climate'])[index==1]
    pasture = np.ravel(data['pasture'])[index==1]
    forest = np.ravel(data['forest'])[index==1]
    others = np.ravel(data['Others'])[index==1]

def draw_picture(ax1, S, title, l):
    proj = ccrs.PlateCarree()
    ax1.set_global()
    name = r"dataset\continent_shp\continent.shp"
    shpfile = shpreader.Reader(name)
    shape_feature = cfeature.ShapelyFeature(shpfile.geometries(), crs=ccrs.PlateCarree())
    ax1.add_feature(shape_feature, edgecolor='k', facecolor='#DCDCDC', lw=0, ls=':', alpha=1, zorder=0)

    colorK = plt.get_cmap('RdBu')(np.linspace(0, 1, 300))
    colorneed = colorK[[i for i in range(100)] + [200 + i for i in range(100)]]
    cmap = ListedColormap(colorneed)

    plt.scatter(lon[others==1], lat[others==1], c=S[others==1] * 100, s=10, cmap=cmap, vmin=l[0],
                 vmax=l[-1],
                 marker='.', linewidths=0.5)

    plt.scatter(lon[pasture > 50], lat[pasture > 50], c=S[pasture > 50] * 100, s=10, cmap=cmap, vmin=l[0],
                vmax=l[-1],
                marker='x', linewidths=0.5)

    lon2 = lon[climates == 2]
    lat2 = lat[climates == 2]
    forest2 = forest[climates == 2]
    S2 = S[climates == 2]
    plt.scatter(lon2[forest2 > 50], lat2[forest2 > 50], c=S2[forest2 > 50] * 100, s=20, cmap=cmap, vmin=l[0],
                vmax=l[-1],
                marker=(3, 2), linewidths=0.5)
    lon1 = lon[climates == 3]
    lat1 = lat[climates == 3]
    forest1 = forest[climates == 3]
    S1 = S[climates == 3]
    plt.scatter(lon1[forest1 > 50], lat1[forest1 > 50], c=S1[forest1 > 50] * 100, s=20, cmap=cmap, vmin=l[0],
                vmax=l[-1],
                marker=(5, 2), linewidths=0.5)
    lon3 = lon[climates == 0]
    lat3 = lat[climates == 0]
    forest3 = forest[climates == 0]
    S3 = S[climates == 0]
    plt.scatter(lon3[forest3 > 50], lat3[forest3 > 50], c=S3[forest3 > 50] * 100, s=15, cmap=cmap, vmin=l[0],
                vmax=l[-1],
                marker='+', linewidths=0.5, edgecolor='None')

    ax1.axis('off')
    ax1.set_extent(extents, crs=proj)
    plt.xticks(family='serif')
    plt.yticks(family='serif')

    plt.title(title, fontsize=20, family='serif', pad=0)

    handles, labels = ax1.get_legend_handles_labels()
    return handles, labels

def draw_picture1(ax1, S, title, l, ls):
    proj = ccrs.PlateCarree()
    ax1.set_global()
    name = r"dataset\continent_shp\continent.shp"
    shpfile = shpreader.Reader(name)
    shape_feature = cfeature.ShapelyFeature(shpfile.geometries(), crs=ccrs.PlateCarree())
    ax1.add_feature(shape_feature, edgecolor='k', facecolor='#DCDCDC', lw=0, ls=':', alpha=1, zorder=0)

    colorK = plt.get_cmap('RdBu')(np.linspace(0, 1, 300))
    colorneed = colorK[[i for i in range(100)] + [200 + i for i in range(100)]]
    cmap = ListedColormap(colorneed)

    im = plt.scatter(lon[others == 1], lat[others == 1], c=S[others == 1] * 100, s=10, cmap=cmap, vmin=l[0],
                     vmax=l[-1],
                     marker='.', linewidths=0.5)

    plt.scatter(lon[pasture > 50], lat[pasture > 50], c=S[pasture > 50] * 100, s=10, cmap=cmap, vmin=l[0],
                vmax=l[-1],
                marker='x', linewidths=0.5)

    lon2 = lon[climates == 2]
    lat2 = lat[climates == 2]
    forest2 = forest[climates == 2]
    S2 = S[climates == 2]
    plt.scatter(lon2[forest2 > 50], lat2[forest2 > 50], c=S2[forest2 > 50] * 100, s=20, cmap=cmap, vmin=l[0],
                vmax=l[-1],
                marker=(3, 2), linewidths=0.5)
    lon1 = lon[climates == 3]
    lat1 = lat[climates == 3]
    forest1 = forest[climates == 3]
    S1 = S[climates == 3]
    plt.scatter(lon1[forest1 > 50], lat1[forest1 > 50], c=S1[forest1 > 50] * 100, s=20, cmap=cmap, vmin=l[0],
                vmax=l[-1],
                marker=(5, 2), linewidths=0.5)
    lon3 = lon[climates == 0]
    lat3 = lat[climates == 0]
    forest3 = forest[climates == 0]
    S3 = S[climates == 0]
    plt.scatter(lon3[forest3 > 50], lat3[forest3 > 50], c=S3[forest3 > 50] * 100, s=15, cmap=cmap, vmin=l[0],
                vmax=l[-1],
                marker='+', linewidths=0.5, edgecolor='None')

    plt.scatter(-999, -999, s=30, color='k', marker='+', linewidths=1.0, label='Tropical forest')
    plt.scatter(-999, -999, s=40, color='k', marker=(3, 2), linewidths=1.0, label='Temperate forest')
    plt.scatter(-999, -999, s=40, color='k', marker=(5, 2), linewidths=1.0, label='Cold forest')
    plt.scatter(-999, -999, s=20, color='k', marker='x', linewidths=1.0, label="pasture")
    plt.scatter(-999, -999, s=20, color='k', marker='.', linewidths=1.0, label="Others")
    plt.scatter(-999, -999, s=20, color='None', marker='.', linewidths=1.0, label=" ")

    c = ['#CCDFCC', '#B6D3D2', '#E2DBB0', '#E2D4D6', '#DADADA']
    alpha = 1
    plt.bar(-999, 0, color=c[0], label="Tropical", alpha=alpha)
    plt.bar(-999, 0, color=c[1], label="Arid", alpha=alpha)
    plt.bar(-999, 0, color=c[2], label="Temperate", alpha=alpha)
    plt.bar(-999, 0, color=c[3], label="Cold", alpha=alpha)
    plt.bar(-999, 0, color=c[4], label="Polar", alpha=alpha)
    ax1.axis('off')
    ax1.set_extent(extents, crs=proj)
    plt.xticks(family='serif')
    plt.yticks(family='serif')
    plt.title(title, fontsize=20, family='serif', pad=0)

    plt.tight_layout()
    plt.rcParams['savefig.dpi'] = 2000

    # Colorbar
    fig = plt.figure(figsize=(1, 6))
    ax2 = fig.add_subplot(111)
    # ax2_divider = make_axes_locatable(ax2)
    # cax2 = ax2_divider.append_axes("left", size="7%", pad="2%")
    cbar = fig.colorbar(im, cax=ax2, extend='both')
                        # orientation='horizontal'
    cbar.ax.tick_params(bottom=True, tickdir='inout', pad=2)

    cbar.set_ticks(l)
    cbar.set_ticklabels(ls, family='serif', fontsize=12)
    ax2.yaxis.set_ticks_position("left")
    handles, labels = ax1.get_legend_handles_labels()
    fig.patch.set_alpha(0)
    plt.tight_layout()
    plt.rcParams['savefig.dpi'] = 2000
    return handles, labels
proj = ccrs.PlateCarree()

def draw_picuture():
    fig = plt.figure(figsize=(6.5, 3))
    ax1 = fig.add_subplot(111, projection=proj)
    draw_picture(ax1, P_per, "P contribution", [-100 + 25 * i for i in range(9)])
    fig.patch.set_alpha(1)
    plt.tight_layout()
    plt.rcParams['savefig.dpi'] = 2000

    fig = plt.figure(figsize=(6.5, 3))
    ax1 = fig.add_subplot(111, projection=proj)
    draw_picture(ax1, Ep_per, "ET$\mathrm{_p}$ contribution", [-100 + 25 * i for i in range(9)])
    fig.patch.set_alpha(1)
    plt.tight_layout()
    plt.rcParams['savefig.dpi'] = 2000

    fig = plt.figure(figsize=(6.5, 3))
    ax1 = fig.add_subplot(111, projection=proj)
    handles, labels = draw_picture1(ax1, CO2_per, "eCO$_2$ contribution",
                                    [-100 + 25 * i for i in range(9)],
                                    [str(-100 + 25 * i) + '%' for i in range(9)])
    fig.patch.set_alpha(1)
    plt.tight_layout()
    plt.rcParams['savefig.dpi'] = 2000

    fig = plt.figure(figsize=(6.5, 3))
    plt.rcParams['xtick.direction'] = 'inout'
    plt.rcParams['ytick.direction'] = 'inout'
    ax = fig.add_subplot(111)
    ax.spines[['right', 'top']].set_visible(False)
    linewidth = 1.5
    ax.plot([-1, 8], [0, 0], ls='--', c='k', linewidth=1, alpha=1)
    boxprops1 = dict(linestyle='-', linewidth=linewidth, color='#1f77b4')
    boxprops2 = dict(linestyle='-', linewidth=linewidth, color='#ff7f0e')
    boxprops3 = dict(linestyle='-', linewidth=linewidth, color='#2ca02c')
    medianprops1 = dict(linestyle='-', linewidth=linewidth, color='#1f77b4')
    medianprops2 = dict(linestyle='-', linewidth=linewidth, color='#ff7f0e')
    medianprops3 = dict(linestyle='-', linewidth=linewidth, color='#2ca02c')
    capprops1 = dict(linestyle='-', linewidth=linewidth, color='#1f77b4')
    capprops2 = dict(linestyle='-', linewidth=linewidth, color='#ff7f0e')
    capprops3 = dict(linestyle='-', linewidth=linewidth, color='#2ca02c')
    whiskerprops1 = dict(linestyle='-', linewidth=linewidth, color='#1f77b4')
    whiskerprops2 = dict(linestyle='-', linewidth=linewidth, color='#ff7f0e')
    whiskerprops3 = dict(linestyle='-', linewidth=linewidth, color='#2ca02c')

    ax.boxplot(x=[AC[:, 0], RC[:, 0]],
               positions=[1, 4],
               boxprops=boxprops1,
               medianprops=medianprops1,
               capprops=capprops1,
               whiskerprops=whiskerprops1,
               showfliers=False,
               patch_artist=False)
    ax.boxplot(x=[AC[:, 1], RC[:, 1]],
               positions=[1.7, 4.7],
               boxprops=boxprops2,
               medianprops=medianprops2,
               capprops=capprops2,
               whiskerprops=whiskerprops2,
               showfliers=False,
               patch_artist=False)
    ax.boxplot(x=[AC[:, 2], RC[:, 2]],
               positions=[2.4, 5.4],
               boxprops=boxprops3,
               medianprops=medianprops3,
               capprops=capprops3,
               whiskerprops=whiskerprops3,
               showfliers=False,
               patch_artist=False)

    plt.gca().yaxis.set_major_locator(MultipleLocator(0.5))
    plt.gca().yaxis.set_minor_locator(MultipleLocator(0.1))
    plt.grid(True, which="major", axis='y', linestyle="--", color="lightgray", linewidth=1)
    plt.grid(True, which="minor", axis='y', linestyle=":",  color="lightgray",  linewidth=1)

    plt.xlim([0.2, 6.4])
    plt.ylim([-1.1, 1.1])
    plt.xticks([1, 1.7, 2.4, 4, 4.7, 5.4], ['P', 'ET$\mathrm{_p}$', 'eCO$_2$', 'P', 'ET$\mathrm{_p}$', 'eCO$_2$'], family='serif', fontsize=16)
    plt.yticks([-1, -0.5, 0, 0.5, 1], ['-100', '-50', '0', '50', '100'], family='serif', fontsize=14)
    plt.ylabel('Relative\ncontribution (%)', family='serif', fontsize=16)
    fig.text(0.76, 0.00, 'Real', fontfamily='serif',
             # transform=ax1.transAxes,
             fontsize=16,
             horizontalalignment='center', verticalalignment='bottom')
    fig.text(0.38, 0.00, 'Absolute', fontfamily='serif',
             # transform=ax1.transAxes,
             fontsize=16,
             horizontalalignment='center', verticalalignment='bottom')
    fig.patch.set_alpha(1)
    plt.tight_layout()
    plt.subplots_adjust(
        top=0.903,
        bottom=0.201,
        left=0.17,
        right=0.977,
        hspace=0.2,
        wspace=0.2)
    plt.rcParams['savefig.dpi'] = 2000
    plt.show()
draw_picuture()
