import os
os.chdir(r'/Users/oazevedo3/Documents/GitHub/mtpy') # change to path where mtpy is installed
from mtpy.core.mt import MT
from mtpy.utils.calculator import get_period_list
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/oazevedo3/Documents/LIGERA/processing/edi_conv/modem.data', delim_whitespace=True, 
    names=['Period(s)', 'Code', 'GG_Lat', 'GG_Lon', 'X(m)', 'Y(m)', 'Z(m)', 'Component', 'Real', 'Imag', 'Error'], skiprows=8)

grouped = df.groupby("Code")

#print(grouped.get_group('sam'))

# most_periods = 0
# for group in grouped:
#     if pd.size(group['Period(s)']) > most_periods:
#         most_periods = pd.size(group['Period(s)'])
# print(most_periods)
#print(df['Period(s)'].value_counts().values)
#num_freqs = df.groupby('Code').size()/4
#print(num_freqs == num_freqs.max()) # 33 freqs

found_periods = np.array([54.361710, 140.300500, 225.393300, 362.095800, 581.709900, 934.518300, 87.332430, 1501.310000, 
    2411.864000, 33.838540, 21.063450, 0.762701, 0.183953, 0.295521, 0.474757, 3.162275, 1.225280, 
    1.968419, 0.071276, 5.080217, 8.161400, 0.114505, 0.004146, 0.044367, 0.027617, 0.017191, 
    0.010701, 0.006661, 0.002581, 0.001607, 0.001000, 13.111330, 3874.677000, 6224.673000, 10000.000000])
found_periods.sort()
# print(found_periods)

# fig = plt.figure()
# subplot = fig.add_subplot(111)
# subplot.vlines(found_periods, -1, 1)
# subplot.set_xscale('log')
# plt.show()

# directory format for windows users
edi_path = r'/Users/oazevedo3/Documents/LIGERA/PROJ_4_2nd_round_exports_Compact'
savepath = r'/Users/oazevedo3/Documents/LIGERA/processing/edi_conv'
edi_names = ['P=NIC04_R=NIC12_(H)_Workbench_1.edi'] # , 'P=NIC18_R=NIC12_(H)_Workbench_1.edi', 
# 'P=NIC36_R=NIC16_(H)_Workbench_1.edi', 'P=NIC06_R=NIC54_(H)_Workbench_1.edi', 
# 'P=NIC22_R=NIC14_(H)_Workbench_1.edi', 'P=NIC37_R=NIC36_(H)_Workbench_1.edi', 
# 'P=NIC08_R=NIC02_(H)_Workbench_1.edi', 'P=NIC23_R=NIC61_(H)_Workbench_1.edi', 
# 'P=NIC39_R=NIC04_(H)_Workbench_1.edi', 'P=NIC10_R=NIC15_(H)_Workbench_1.edi', 
# 'P=NIC25_2_R=NIC04_(H)_Workbench_1.edi', 'P=NIC40_R=NIC26_(H)_Workbench_1.edi', 
# 'P=NIC11_R=NIC04_(H)_Workbench_1.edi', 'P=NIC26_R=NIC23_(H)_Workbench_1.edi', 
# 'P=NIC50_R=NIC51_(H)_Workbench_1.edi', 'P=NIC12_R=NIC04_(H)_Workbench_1.edi', 
# 'P=NIC28_R=NIC14_(H)_Workbench_1.edi', 'P=NIC51_R=NIC50_(H)_Workbench_1.edi', 
# 'P=NIC13_R=NIC09_(H)_Workbench_1.edi', 'P=NIC29_R=NIC23_(H)_Workbench_1.edi', 
# 'P=NIC52_R=NIC23_(H)_Workbench_1.edi', 'P=NIC14_R=NIC09_(H)_Workbench_1.edi', 
# 'P=NIC30_R=NIC36_(H)_Workbench_1.edi', 'P=NIC53_R=NIC06_(H)_Workbench_1.edi', 
# 'P=NIC16_R=NIC36_(H)_Workbench_1.edi', 'P=NIC32_R=NIC23_(H)_Workbench_1.edi', 
# 'P=NIC54_R=NIC53_(H)_Workbench_1.edi', 'P=NIC17_R=NIC52_(H)_Workbench_1.edi', 
# 'P=NIC35_R=NIC16_(H)_Workbench_1.edi', 'P=NIC61_R=NIC23_(H)_Workbench_1.edi']

sites = ['NIC04', 'NIC18', 'NIC36', 'NIC06', 'NIC22', 'NIC37', 'NIC08', 'NIC23', 'NIC39', 'NIC10', 
        'NIC25_2', 'NIC40', 'NIC11', 'NIC26', 'NIC50', 'NIC12', 'NIC28', 'NIC51', 'NIC13', 'NIC29', 
        'NIC52', 'NIC14', 'NIC30', 'NIC53', 'NIC16', 'NIC54', 'NIC17', 'NIC35', 'NIC61']

for i, name in enumerate(edi_names):
    edi_file = os.path.join(edi_path, name)
    mtObj = MT(edi_file)
    #new_freq_list = 1./get_period_list(1e-4,1e3,5) # 5 periods per decade from 0.0001 to 100000 s
    #desired_freqs = 1./get_period_list(1e-3,1e4,5) # 5 periods per decade from 0.01 to 10000 s
    desired_freqs = 1.0/found_periods
    if np.max(desired_freqs) > np.max(mtObj.Z.freq):
        mask = desired_freqs <= np.max(mtObj.Z.freq)
        desired_freqs = desired_freqs[mask]
    if np.min(desired_freqs) < np.min(mtObj.Z.freq):
        mask = desired_freqs >= np.min(mtObj.Z.freq)
        desired_freqs = desired_freqs[mask]

    # create new Z and Tipper objects containing interpolated data
    new_Z_obj, new_Tipper_obj = mtObj.interpolate(desired_freqs)
    # print('\n')
    # print('freqs:')
    # print(mtObj.Z.freq)
    # print('\n')
    # print('z:')
    # print(mtObj.Z.z)
    print('\n')
    print('z_err:')
    z_index = np.array([0, 0])
    print(mtObj.Z.z_err[:,z_index])
#    print(mtObj.Z.z_err[:,0,0])
    print('\n')
    # print(mtObj.Site.__dict__)
                            #    [:, 0, 0]   [:, 0, 1]   [:, 1, 0]   [:, 1, 1]
    for j, component in enumerate(['ZXX']):#,      'ZXY',      'ZYX',      'ZYY']):
        print('\n')
        print(df.loc[(df['Code']==sites[i]) & (df['Component']==component)]['Error'])
        print('\n')
        #df.loc[(df['Code']==sites[i]) & (df['Component']==component)]['Error'] = mtObj.Z.z_err[:,,]

        pass

    # # write a new edi file using the new data
    # mtObj.write_mt_file(save_dir=savepath, fn_basename=name, file_type='edi', # edi or xml format
    #                     new_Z_obj=new_Z_obj, # provide a z object to update the data
    #                     new_Tipper_obj=new_Tipper_obj, # provide a tipper object to update the data
    #                     longitude_format='LONG', # write longitudes as 'LON' or 'LONG'
    #                     latlon_format='dd' # write as decimal degrees (any other input
    #                                         # will write as degrees minutes seconds
    #                     )