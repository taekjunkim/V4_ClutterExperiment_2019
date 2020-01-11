#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 16:38:14 2019

ClutterStim032219_Analysis.py

@author: taekjunkim
"""
import sys;
sys.path.append('./parseNex');
sys.path.append('./makeSDF');

import numpy as np;
import makeSDF;

filedir = '../../../2.DataFiles/RawFiles/NexFiles/ClutterStim/';
filename = 'F190805_ClutterStim_Mar2019_recut.nex';
prevTime = 0.3;
numStims = 54*15;  ## stimuli changed depending on repetition numbers
                   ## so number of condition (54) * number of repetition (15)

import parseTJexperiment as parse;
experiment = parse.main(filedir+filename,prevTime,numStims);

TimeOfInterest = np.arange(int(prevTime*1000+50),int(prevTime*1000+experiment['StimDur']+100+1));

#%%
StimResp = [];
mResp = np.zeros((numStims,experiment['numNeurons']));
for i in np.arange(len(experiment['stimStructs'])):
    CondNum = int(i%54);
    RepNum = int(np.floor(i/54))+1;
    
    if RepNum==1:
        StimResp.append(dict());
        StimResp[CondNum]['timeOn'] = experiment['stimStructs'][i]['timeOn'];
        StimResp[CondNum]['timeOff'] = experiment['stimStructs'][i]['timeOff'];    
        StimResp[CondNum]['pdOn'] = experiment['stimStructs'][i]['pdOn'];
        StimResp[CondNum]['pdOff'] = experiment['stimStructs'][i]['pdOff'];     
        StimResp[CondNum]['neurons'] = experiment['stimStructs'][i]['neurons'];             
    else:
        StimResp[CondNum]['timeOn'].append(experiment['stimStructs'][i]['timeOn'][0]);
        StimResp[CondNum]['timeOff'].append(experiment['stimStructs'][i]['timeOff'][0]);    
        StimResp[CondNum]['pdOn'].append(experiment['stimStructs'][i]['pdOn'][0]);
        StimResp[CondNum]['pdOff'].append(experiment['stimStructs'][i]['pdOff'][0]);     
        for j in np.arange(experiment['numNeurons']):
            StimResp[CondNum]['neurons'][j]['spikes'].append(experiment['stimStructs'][i]['neurons'][j]['spikes'][0]);
        
#%%
for i in np.arange(len(StimResp)):
    for j in np.arange(experiment['numNeurons']):
        NumRepeat = len(StimResp[i]['pdOn']);
        sigLength = int(experiment['StimDur'] + experiment['prevTime']*1000 
                    + experiment['postTime']*1000);       
        StimResp[i]['neurons'][j]['spkMtx'] = np.zeros((NumRepeat,sigLength),dtype=int);
        StimResp[i]['neurons'][j]['numspikes'] = np.zeros((NumRepeat,1),dtype=int);        
        for r in np.arange(NumRepeat):
            spkTime = StimResp[i]['neurons'][j]['spikes'][r] - StimResp[i]['pdOn'][r];
            spkTime = spkTime[:]*1000 + experiment['prevTime']*1000;
            spkTime = spkTime[np.where(spkTime[:]<900)];
            spkTime = spkTime.astype(int);
            StimResp[i]['neurons'][j]['spkMtx'][r,spkTime] = 1;
            StimResp[i]['neurons'][j]['numspikes'][r] = np.sum(StimResp[i]['neurons'][j]['spkMtx'][r,TimeOfInterest]);            
        
        StimResp[i]['neurons'][j]['meanSDF'] = makeSDF.getSDF(StimResp[i]['neurons'][j]['spkMtx'],1000);
        mResp[i,j] = np.mean(StimResp[i]['neurons'][j]['meanSDF'][TimeOfInterest])
        
#%%
del experiment['stimStructs'];
del experiment['iti_start'];
del experiment['iti_end'];
del experiment['iti'];
experiment['filename'] = filename;
experiment['StimResp'] = StimResp;

#%%
import json;
import gzip;

class NumpyEncoder(json.JSONEncoder):
    # Special json encoder for numpy types 
    """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
            np.int16, np.int32, np.int64, np.uint8,
            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, 
            np.float64)):
            return float(obj)z`
        elif isinstance(obj,(np.ndarray,)): #### This is the fix
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj,np.ndarray): #### This is the fix
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

savedir = '../../../2.DataFiles/ProcessedFiles/ClutterStim/'
f = gzip.GzipFile(savedir+filename[:-4]+'.json.gz','w');
f.write(json.dumps(experiment, cls=NumpyEncoder).encode('utf-8'));
f.close();


#%%
#%% load cell data
"""
import json;
import gzip;

f = gzip.GzipFile(filename[:-4]+'.json.gz','r');
Data = json.loads(f.read().decode('utf-8'));
f.close();
"""
       
#%% Stimulus conditions
"""
No stim (0)
Center alone (1-8)
1 Surround alone (9)
Center + 1 Surround (10-17)
3 Surround alone (18)
Center + 3 Surround (19-26)
6 Surround alone (27)
Center + 6 Surround (Near) (28-35)
12 Surround alone (36)
Center + 12 Surround (Middle) (37-44)
18 Surround alone (45)
Center + 18 Surround (Far) (46-53)  
"""

#%% Drawing part
import matplotlib.pyplot as plt;

for j in np.arange(experiment['numNeurons']):
    plt.figure(figsize=(20/2.54,15/2.54),dpi=200);
    
    NoStim = np.mean(StimResp[0]['neurons'][j]['meanSDF'][TimeOfInterest]);
    
    ## Control of near surround stimulus number
    cAlone = mResp[1:9,j];
    cS1 = mResp[10:18,j];
    cS3 = mResp[19:27,j];
    cS6 = mResp[28:36,j];    
    
    cAlone_ste = [];
    cS1_ste = [];   cS3_ste = [];   cS6_ste = [];
    for i in np.arange(8):
        cAlone_ste.append((np.std(StimResp[1+i]['neurons'][j]['numspikes'])*1000/350)
                            /(np.sqrt(len(StimResp[1+i]['neurons'][j]['numspikes']))));
        cS1_ste.append((np.std(StimResp[10+i]['neurons'][j]['numspikes'])*1000/350)
                            /(np.sqrt(len(StimResp[10+i]['neurons'][j]['numspikes']))));
        cS3_ste.append((np.std(StimResp[19+i]['neurons'][j]['numspikes'])*1000/350)
                            /(np.sqrt(len(StimResp[19+i]['neurons'][j]['numspikes']))));
        cS6_ste.append((np.std(StimResp[28+i]['neurons'][j]['numspikes'])*1000/350)
                            /(np.sqrt(len(StimResp[28+i]['neurons'][j]['numspikes']))));
    rk = np.flip(np.argsort(cAlone)); ## ranking of shape preference    
    
    plt.subplot(3,2,1);
    plt.errorbar(np.arange(1,9),cAlone[rk],np.array(cAlone_ste)[rk],color=[1,0,0]);
    plt.errorbar(np.arange(1,9),cS1[rk],np.array(cS1_ste)[rk],color=[0.6,0.6,0.6]);
    plt.errorbar(np.arange(1,9),cS3[rk],np.array(cS3_ste)[rk],color=[0.3,0.3,0.3]);
    plt.errorbar(np.arange(1,9),cS6[rk],np.array(cS6_ste)[rk],color=[0,0,0]);    
    plt.title('# of Near Surround Stims');
    
    plt.subplot(3,2,3);
    cAlone_sdf = np.zeros((900,));
    cS1_sdf = np.zeros((900,));
    cS3_sdf = np.zeros((900,));
    cS6_sdf = np.zeros((900,));    
    for i in np.arange(8):
        cAlone_sdf += StimResp[1+i]['neurons'][j]['meanSDF'];
        cS1_sdf += StimResp[10+i]['neurons'][j]['meanSDF'];
        cS3_sdf += StimResp[19+i]['neurons'][j]['meanSDF'];
        cS6_sdf += StimResp[28+i]['neurons'][j]['meanSDF'];        
    plt.plot(np.arange(-100,500),cAlone_sdf[200:800]/8,color=[1,0,0]);
    plt.plot(np.arange(-100,500),cS1_sdf[200:800]/8,color=[0.6,0.6,0.6]);
    plt.plot(np.arange(-100,500),cS3_sdf[200:800]/8,color=[0.3,0.3,0.3]);
    plt.plot(np.arange(-100,500),cS6_sdf[200:800]/8,color=[0,0,0]);        
    
    plt.subplot(3,2,5);
    modMtx1 = np.empty((3,900));
    modMtx1[0,:] = cS1_sdf[:];
    modMtx1[1,:] = cS3_sdf[:];
    modMtx1[2,:] = cS6_sdf[:];
    modSD1 = np.std(modMtx1,axis=0);
    plt.plot(np.arange(-100,500),modSD1[200:800]/8,color=[0,0,1]);
    del modMtx1, modSD1;
    
    ## Control of center-surround distance    
    cS12 = mResp[37:45,j];
    cS18 = mResp[46:54,j];    
    cS12_ste = [];   cS18_ste = [];
    for i in np.arange(8):
        cS12_ste.append((np.std(StimResp[37+i]['neurons'][j]['numspikes'])*1000/350)
                            /(np.sqrt(len(StimResp[37+i]['neurons'][j]['numspikes']))));
        cS18_ste.append((np.std(StimResp[46+i]['neurons'][j]['numspikes'])*1000/350)
                            /(np.sqrt(len(StimResp[46+i]['neurons'][j]['numspikes']))));
        
    plt.subplot(3,2,2);
    plt.errorbar(np.arange(1,9),cAlone[rk],np.array(cAlone_ste)[rk],color=[1,0,0]);
    plt.errorbar(np.arange(1,9),cS6[rk],np.array(cS6_ste)[rk],color=[0,0,0]);
    plt.errorbar(np.arange(1,9),cS12[rk],np.array(cS12_ste)[rk],color=[0.3,0.3,0.3]);
    plt.errorbar(np.arange(1,9),cS18[rk],np.array(cS18_ste)[rk],color=[0.6,0.6,0.6]);    
    plt.title('Center-Surround distance');    
    
    plt.subplot(3,2,4);
    cS12_sdf = np.zeros((900,));
    cS18_sdf = np.zeros((900,));
    for i in np.arange(8):
        cS12_sdf += StimResp[37+i]['neurons'][j]['meanSDF'];
        cS18_sdf += StimResp[46+i]['neurons'][j]['meanSDF'];        
    plt.plot(np.arange(-100,500),cAlone_sdf[200:800]/8,color=[1,0,0]);
    plt.plot(np.arange(-100,500),cS18_sdf[200:800]/8,color=[0.6,0.6,0.6]);
    plt.plot(np.arange(-100,500),cS12_sdf[200:800]/8,color=[0.3,0.3,0.3]);
    plt.plot(np.arange(-100,500),cS6_sdf[200:800]/8,color=[0,0,0]);        
    
    plt.subplot(3,2,6);
    modMtx2 = np.empty((3,900));
    modMtx2[0,:] = cS6_sdf[:];
    modMtx2[1,:] = cS12_sdf[:];
    modMtx2[2,:] = cS18_sdf[:];
    modSD2 = np.std(modMtx2,axis=0);
    plt.plot(np.arange(-100,500),modSD2[200:800]/8,color=[0,0,1]);
    del modMtx2, modSD2;
    