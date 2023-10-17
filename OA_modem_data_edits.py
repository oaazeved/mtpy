import os
os.chdir(r'/Users/oazevedo3/Documents/GitHub/mtpy') # change to path where mtpy is installed
from mtpy.core.mt import MT
from mtpy.utils.calculator import get_period_list
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/oazevedo3/Documents/LIGERA/results/test_04/modem.data', delim_whitespace=True, 
    names=['Period(s)', 'Code', 'GG_Lat', 'GG_Lon', 'X(m)', 'Y(m)', 'Z(m)', 'Component', 'Real', 'Imag', 'Error'], skiprows=8)
found_periods = np.array([54.361710, 140.300500, 225.393300, 362.095800, 581.709900, 934.518300, 87.332430, 1501.310000, 
            2411.864000, 33.838540, 21.063450, 0.762701, 0.183953, 0.295521, 0.474757, 3.162275, 1.225280, 
            1.968419, 0.071276, 5.080217, 8.161400, 0.114505, 0.004146, 0.044367, 0.027617, 0.017191, 
            0.010701, 0.006661, 0.002581, 0.001607, 0.001000, 13.111330, 3874.677000, 6224.673000, 10000.000000])
found_periods.sort()
# print(found_periods)
# found_periods = found_periods[found_periods <= 2000.0]
# print(found_periods)
edi_path = r'/Users/oazevedo3/Documents/LIGERA/PROJ_4_2nd_round_exports_Compact'
savepath = r'/Users/oazevedo3/Documents/LIGERA/results/test_04'
edi_names = ['P=NIC04_R=NIC12_(H)_Workbench_1.edi', 'P=NIC18_R=NIC12_(H)_Workbench_1.edi', 
            'P=NIC36_R=NIC16_(H)_Workbench_1.edi', 'P=NIC06_R=NIC54_(H)_Workbench_1.edi', 
            'P=NIC22_R=NIC14_(H)_Workbench_1.edi', 'P=NIC37_R=NIC36_(H)_Workbench_1.edi', 
            'P=NIC08_R=NIC02_(H)_Workbench_1.edi', 'P=NIC23_R=NIC61_(H)_Workbench_1.edi', 
            'P=NIC39_R=NIC04_(H)_Workbench_1.edi', 'P=NIC10_R=NIC15_(H)_Workbench_1.edi', 
            'P=NIC25_2_R=NIC04_(H)_Workbench_1.edi', 'P=NIC40_R=NIC26_(H)_Workbench_1.edi', 
            'P=NIC11_R=NIC04_(H)_Workbench_1.edi', 'P=NIC26_R=NIC23_(H)_Workbench_1.edi', 
            'P=NIC50_R=NIC51_(H)_Workbench_1.edi', 'P=NIC12_R=NIC04_(H)_Workbench_1.edi', 
            'P=NIC28_R=NIC14_(H)_Workbench_1.edi', 'P=NIC51_R=NIC50_(H)_Workbench_1.edi', 
            'P=NIC13_R=NIC09_(H)_Workbench_1.edi', 'P=NIC29_R=NIC23_(H)_Workbench_1.edi', 
            'P=NIC52_R=NIC23_(H)_Workbench_1.edi', 'P=NIC14_R=NIC09_(H)_Workbench_1.edi', 
            'P=NIC30_R=NIC36_(H)_Workbench_1.edi', 'P=NIC53_R=NIC06_(H)_Workbench_1.edi', 
            'P=NIC16_R=NIC36_(H)_Workbench_1.edi', 'P=NIC32_R=NIC23_(H)_Workbench_1.edi', 
            'P=NIC54_R=NIC53_(H)_Workbench_1.edi', 'P=NIC17_R=NIC52_(H)_Workbench_1.edi', 
            'P=NIC35_R=NIC16_(H)_Workbench_1.edi'] #, 'P=NIC61_R=NIC23_(H)_Workbench_1.edi']
sites = ['NIC04', 'NIC18', 'NIC36', 'NIC06', 'NIC22', 'NIC37', 'NIC08', 'NIC23', 'NIC39', 'NIC10', 
        'NIC25', 'NIC40', 'NIC11', 'NIC26', 'NIC50', 'NIC12', 'NIC28', 'NIC51', 'NIC13', 'NIC29', 
        'NIC52', 'NIC14', 'NIC30', 'NIC53', 'NIC16', 'NIC32', 'NIC54', 'NIC17', 'NIC35']#, 'NIC61']

for i, name in enumerate(edi_names):
    edi_file = os.path.join(edi_path, name)
    mtObj = MT(edi_file)
    desired_freqs = 1.0/found_periods
    if np.max(desired_freqs) > np.max(mtObj.Z.freq):
        mask = desired_freqs <= np.max(mtObj.Z.freq)
        desired_freqs = desired_freqs[mask]
    if np.min(desired_freqs) < np.min(mtObj.Z.freq):
        mask = desired_freqs >= np.min(mtObj.Z.freq)
        desired_freqs = desired_freqs[mask]
    # create new Z and Tipper objects containing interpolated data
    new_Z_obj, _ = mtObj.interpolate(desired_freqs)
    # df.loc[(df['Code']==sites[i]) & (df['Component']=='ZXX'), 'Error'] = [abs(np.real(new_Z_obj.z[j,0,0]))*0.2 if (zerr<(abs(np.real(new_Z_obj.z[j,0,0]))*0.2)) else zerr for j, zerr in enumerate(new_Z_obj.z_err[:,0,0])]
    # df.loc[(df['Code']==sites[i]) & (df['Component']=='ZXY'), 'Error'] = [abs(np.real(new_Z_obj.z[j,0,1]))*0.05 if (zerr<(abs(np.real(new_Z_obj.z[j,0,1]))*0.05)) else zerr for j, zerr in enumerate(new_Z_obj.z_err[:,0,1])]
    # df.loc[(df['Code']==sites[i]) & (df['Component']=='ZYX'), 'Error'] = [abs(np.real(new_Z_obj.z[j,1,0]))*0.05 if (zerr<(abs(np.real(new_Z_obj.z[j,1,0]))*0.05)) else zerr for j, zerr in enumerate(new_Z_obj.z_err[:,1,0])]
    # df.loc[(df['Code']==sites[i]) & (df['Component']=='ZYY'), 'Error'] = [abs(np.real(new_Z_obj.z[j,1,1]))*0.2 if (zerr<(abs(np.real(new_Z_obj.z[j,1,1]))*0.2)) else zerr for j, zerr in enumerate(new_Z_obj.z_err[:,1,1])]
    df.loc[(df['Code']==sites[i]) & (df['Component']=='ZXX'), 'Error'] = [np.abs(new_Z_obj.z[j,0,0])*0.2 if (zerr<(np.abs(new_Z_obj.z[j,0,0])*0.2)) else zerr for j, zerr in enumerate(new_Z_obj.z_err[:,0,0])]
    df.loc[(df['Code']==sites[i]) & (df['Component']=='ZXY'), 'Error'] = [np.abs(new_Z_obj.z[j,0,1])*0.05 if (zerr<(np.abs(new_Z_obj.z[j,0,1])*0.05)) else zerr for j, zerr in enumerate(new_Z_obj.z_err[:,0,1])]
    df.loc[(df['Code']==sites[i]) & (df['Component']=='ZYX'), 'Error'] = [np.abs(new_Z_obj.z[j,1,0])*0.05 if (zerr<(np.abs(new_Z_obj.z[j,1,0])*0.05)) else zerr for j, zerr in enumerate(new_Z_obj.z_err[:,1,0])]
    df.loc[(df['Code']==sites[i]) & (df['Component']=='ZYY'), 'Error'] = [np.abs(new_Z_obj.z[j,1,1])*0.2 if (zerr<(np.abs(new_Z_obj.z[j,1,1])*0.2)) else zerr for j, zerr in enumerate(new_Z_obj.z_err[:,1,1])]


w_sites = ['7hn' 'bao' 'cdp' 'mot' 'sam' 'sjb' 'ter']
err_array = df[['Code', 'Component', 'Real', 'Imag', 'Error']].to_numpy()
codes = err_array[:,0]
components = err_array[:,1]
real = err_array[:,2]
imag = err_array[:,3]
errs = err_array[:,4]
for _, site in enumerate(w_sites):
    select = (codes==site) & (components=='ZXX')
    errs[select] = [np.abs(real[select] + 1j*imag[select])*0.2 if (err<(np.abs(real[select] + 1j*imag[select]))*0.2) else err for _, err in enumerate(errs[select])]
    select = (codes==site) & (components=='ZYY')
    errs[select] = [np.abs(real[select] + 1j*imag[select])*0.2 if (err<(np.abs(real[select] + 1j*imag[select]))*0.2) else err for _, err in enumerate(errs[select])]
    select = (codes==site) & (components=='ZXY')
    errs[select] = [np.abs(real[select] + 1j*imag[select])*0.05 if (err<(np.abs(real[select] + 1j*imag[select]))*0.05) else err for _, err in enumerate(errs[select])]
    select = (codes==site) & (components=='ZYX')
    errs[select] = [np.abs(real[select] + 1j*imag[select])*0.05 if (err<(np.abs(real[select] + 1j*imag[select]))*0.05) else err for _, err in enumerate(errs[select])]

fig = plt.figure()
subplot = fig.add_subplot(111)
subplot.bar(range(0,len(errs)), err_array[:,4]-errs)
plt.show()



# df.to_csv(path_or_buf=savepath+r'/modem.data', sep=' ', header=False, index=False)
# data_header = "# written by a dog's breakfast of mtpy (Kirkby et al.) and pandas assembled by Oliver Azevedo, plus M3D from University of Alberta, 2018. Based on M3DET by Ersan Turkoglu (2006).\n# Period(s) Code GG_Lat GG_Lon X(m) Y(m) Z(m) Component Real Imag Error\n> Full_Impedance\n> exp(+i\omega t)\n> [mV/km]/[nT]\n> 0.00\n> 10.0836 -85.3647\n> 35 36\n"
# with open(savepath+r'/modem.data', 'r') as original:
#     data = original.read()
# with open(savepath+r'/modem.data', 'w') as modified:
#     modified.write(data_header + data)
