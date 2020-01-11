#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 16:38:14 2019

RndDotRFmap_Analysis.py

@author: taekjunkim
"""
import sys;
sys.path.append('./parseNex');
sys.path.append('./makeSDF');

import numpy as np;
import makeSDF;

filedir = '../../../2.DataFiles/RawFiles/NexFiles/RFmapping/';
filename = 'F191219_RndDot_RFmap1_recut.nex';
prevTime = 0.3;
numStims = 50;

xRange = [1,7];
yRange = [-9,-3];

import parseTJexperiment as parse;
experiment = parse.main(filedir+filename,prevTime,numStims);

TimeOfInterest = np.arange(int(prevTime*1000+50),int(prevTime*1000+experiment['StimDur']+100+1));

#%%
StimResp = [];
mResp = np.zeros((numStims,experiment['numNeurons']));
for i in np.arange(len(experiment['stimStructs'])):
    StimResp.append(dict());
    StimResp[i]['timeOn'] = experiment['stimStructs'][i]['timeOn'];
    StimResp[i]['timeOff'] = experiment['stimStructs'][i]['timeOff'];    
    StimResp[i]['pdOn'] = experiment['stimStructs'][i]['pdOn'];
    StimResp[i]['pdOff'] = experiment['stimStructs'][i]['pdOff'];        
    StimResp[i]['neurons'] = experiment['stimStructs'][i]['neurons'];        

    if i<numStims-1:
        StimResp[i]['xPos'] = int(np.floor(i/7)) + xRange[0];
        StimResp[i]['yPos'] = i%7 + yRange[0];    
    else:
        StimResp[i]['xPos'] = np.nan;
        StimResp[i]['yPos'] = np.nan;        


    for j in np.arange(experiment['numNeurons']):
        NumRepeat = len(StimResp[i]['pdOn']);
        sigLength = int(experiment['StimDur'] + experiment['prevTime']*1000 
                    + experiment['postTime']*1000);       
        StimResp[i]['neurons'][j]['spkMtx'] = np.zeros((NumRepeat,sigLength),dtype=int);
        
        for r in np.arange(NumRepeat):
            spkTime = StimResp[i]['neurons'][j]['spikes'][r] - StimResp[i]['pdOn'][r];
            spkTime = spkTime[:]*1000 + experiment['prevTime']*1000;
            spkTime = spkTime.astype(int);
            StimResp[i]['neurons'][j]['spkMtx'][r,spkTime] = 1;
        
        StimResp[i]['neurons'][j]['meanSDF'] = makeSDF.getSDF(StimResp[i]['neurons'][j]['spkMtx'],1000);
        mResp[i,j] = np.mean(StimResp[i]['neurons'][j]['meanSDF'][TimeOfInterest])
        
#%%
del experiment['stimStructs'];
del experiment['iti_start'];
del experiment['iti_end'];
del experiment['iti'];
experiment['filename'] = filename;
experiment['StimResp'] = StimResp;
experiment['xRange'] = xRange;
experiment['yRange'] = yRange;

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


savedir = '../../../2.DataFiles/ProcessedFiles/RFmapping/'
f = gzip.GzipFile(savedir+filename[:-4]+'.json.gz','w');
f.write(json.dumps(experiment, cls=NumpyEncoder).encode('utf-8'));
f.close();


#%%
#%% load cell data
"""
import json;
import gzip;

savedir = '../../../2.DataFiles/ProcessedFiles/RFmapping/'
f = gzip.GzipFile(savedir+filename[:-4]+'.json.gz','r');
Data = json.loads(f.read().decode('utf-8'));
f.close();
"""
       
#%%
import matplotlib.pyplot as plt;
import scipy.optimize as opt;

def twoD_Gaussian(posData, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    (x, y) = posData;
    xo = float(xo);
    yo = float(yo);         
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2);
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2);
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2);
    g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) 
                            + c*((y-yo)**2)));
    return g.ravel()

#%%
x = np.arange(xRange[0],xRange[1]+1,1);
y = np.arange(yRange[0],yRange[1]+1,1);
x, y = np.meshgrid(x,y);
posData = np.vstack((x.ravel(),y.ravel()));

init_guess = [1,xRange[0]+2,yRange[0]+2,3,3,0,0.1]; #amp,xo,yo,sigx,sigy,theta,offset

x2 = np.arange(xRange[0],xRange[1]+0.01,0.01);
y2 = np.arange(yRange[0],yRange[1]+0.01,0.01);
x2, y2 = np.meshgrid(x2,y2);
posData2 = np.vstack((x2.ravel(),y2.ravel()));

plt.figure(dpi=200);

for j in np.arange(experiment['numNeurons']):        
    plt.subplot(2,2,j+1);
    RFmap = np.zeros((xRange[1]-xRange[0]+1,yRange[1]-yRange[0]+1));
    for i in np.arange(numStims):
        if i<numStims-1:
            rowNum = i%7;
            colNum = int(np.floor(i/7));
            RFmap[rowNum,colNum] = mResp[i,j];
    RFmap = RFmap - mResp[-1,j];        
    RFmap = RFmap/np.max(abs(RFmap));
    #plt.imshow(RFmap,vmin=-1,vmax=1,cmap='bwr',origin='lower');  
    plt.imshow(RFmap,origin='lower',extent=(xRange[0]-0.5,xRange[1]+0.5,
                                            yRange[0]-0.5,yRange[1]+0.5));      

    plt.subplot(2,2,j+3);
    popt, pcov = opt.curve_fit(twoD_Gaussian, posData, RFmap.ravel(), p0=init_guess)
    data_fitted = twoD_Gaussian(posData2, *popt);
    plt.imshow(data_fitted.reshape(601,601),origin='lower',extent=(xRange[0],xRange[1],
                                            yRange[0],yRange[1]));         
    plt.contour(x2, y2, data_fitted.reshape(601,601), 6, colors='w')
