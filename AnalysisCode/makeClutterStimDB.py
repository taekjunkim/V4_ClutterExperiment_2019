#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 14:17:31 2019

makeClutterStimDB.py

@author: taekjunkim
"""
#%% Necessary modules
import glob;
import json;
import gzip;
import numpy as np;

savedir = '../../../2.DataFiles/ProcessedFiles/ClutterStim/';

#%%
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

#%% load existing DB file
DBfile = glob.glob(savedir+'ClutterStimDB.json.gz');
if not DBfile:
    pData = [];
    fStart = 0;    
else:
    f = gzip.GzipFile(DBfile[0],'r');
    pData = json.loads(f.read().decode('utf-8'));
    f.close();
    fStart = pData[-1]['fNum']+1;

#%% Add single files to DB
files = glob.glob(savedir+'*_ClutterStim_*');
files.sort();

if len(files)>fStart:
    for i in range(fStart,len(files)):
        fname = files[i];
        f = gzip.GzipFile(fname,'r');
        cData = json.loads(f.read().decode('utf-8'));
        f.close()
        
        for j in range(cData['numNeurons']):
            pData.append(dict());
            pData[-1]['filename'] = cData['filename'];    
            pData[-1]['neuronid'] = cData['neuronid'][j];
            pData[-1]['RFpos'] = [cData['rfx'],cData['rfy']];
            pData[-1]['fNum'] = i;        
            
            if cData['filename'][20:27]=='Mar2019':
                """
                No stim (0)
                Gray Center Alone (1-8)
                Gray Surround 1 Near Alone (9)
                Gray Center + Gray Surround 1 Near (10-17)
                Gray Surround 3 Near Alone (18)
                Gray Center + Gray Surround 3 Near (19-26)
                Gray Surround 6 Near Alone (27)
                Gray Center + Gray Surround 6 Near (28-35)
                Gray Surround 12 Middle Alone (36)
                Gray Center + Gray Surround 12 Middle (37-44)
                Gray Surround 18 Far Alone (45)
                Gray Center + Gray Surround 18 Far (46-53)
                """
                pData[-1]['NoStim'] = cData['StimResp'][0]['neurons'][j]; 
                pData[-1]['grCe'] = []; 
                pData[-1]['grSu1Ne'] = cData['StimResp'][9]['neurons'][j];
                pData[-1]['grCe_grSu1Ne'] = []; 
                pData[-1]['grSu3Ne'] = cData['StimResp'][18]['neurons'][j]; 
                pData[-1]['grCe_grSu3Ne'] = [];             
                pData[-1]['grSu6Ne'] = cData['StimResp'][27]['neurons'][j];             
                pData[-1]['grCe_grSu6Ne'] = [];                  
                pData[-1]['grSu12Mi'] = cData['StimResp'][36]['neurons'][j];                         
                pData[-1]['grCe_grSu12Mi'] = [];                              
                pData[-1]['guSu18Fa'] = cData['StimResp'][45]['neurons'][j];                         
                pData[-1]['grCe_grSu18Fa'] = [];                              
    
                for n in range(8):
                    pData[-1]['grCe'].append(cData['StimResp'][n+1]['neurons'][j]);      
                    pData[-1]['grCe_grSu1Ne'].append(cData['StimResp'][n+10]['neurons'][j]);                      
                    pData[-1]['grCe_grSu3Ne'].append(cData['StimResp'][n+19]['neurons'][j]);                                      
                    pData[-1]['grCe_grSu6Ne'].append(cData['StimResp'][n+28]['neurons'][j]);                                                      
                    pData[-1]['grCe_grSu12Mi'].append(cData['StimResp'][n+37]['neurons'][j]);                                                                      
                    pData[-1]['grCe_grSu18Fa'].append(cData['StimResp'][n+46]['neurons'][j]);   
                    
            elif cData['filename'][20:27]=='Aug2019':
                """
                No stim (0)
                Gray Center Alone (1-8)
                Gray Surround 1 Near Alone (9)
                Gray Center + Gray Surround 1 Near (10-17)
                Gray Surround 3 Near Alone (18)
                Gray Center + Gray Surround 3 Near (19-26)
                Gray Surround 6 Near Alone (27)
                Gray Center + Gray Surround 6 Near (28-35)
                Gray Surround 12 Middle Alone (36)
                Gray Center + Gray Surround 12 Middle (37-44)
                Gray Surround 18 Far Alone (45)
                Gray Center + Gray Surround 18 Far (46-53)
                Gray Surround 12 Small Circle Near Alone (54)
                Gray Center + Gray Surround 12 Small Circle Near (55-62)
                """
                pData[-1]['NoStim'] = cData['StimResp'][0]['neurons'][j]; 
                pData[-1]['grCe'] = []; 
                pData[-1]['grSu1Ne'] = cData['StimResp'][9]['neurons'][j];
                pData[-1]['grCe_grSu1Ne'] = []; 
                pData[-1]['grSu3Ne'] = cData['StimResp'][18]['neurons'][j]; 
                pData[-1]['grCe_grSu3Ne'] = [];             
                pData[-1]['grSu6Ne'] = cData['StimResp'][27]['neurons'][j];             
                pData[-1]['grCe_grSu6Ne'] = [];                  
                pData[-1]['grSu12Mi'] = cData['StimResp'][36]['neurons'][j];                         
                pData[-1]['grCe_grSu12Mi'] = [];                              
                pData[-1]['guSu18Fa'] = cData['StimResp'][45]['neurons'][j];                         
                pData[-1]['grCe_grSu18Fa'] = [];                              
                pData[-1]['grSu12SmCiNe'] = cData['StimResp'][54]['neurons'][j];                 
                pData[-1]['grCe_grSu12SmCiNe'] = [];      
    
                for n in range(8):
                    pData[-1]['grCe'].append(cData['StimResp'][n+1]['neurons'][j]);      
                    pData[-1]['grCe_grSu1Ne'].append(cData['StimResp'][n+10]['neurons'][j]); 
                    pData[-1]['grCe_grSu3Ne'].append(cData['StimResp'][n+19]['neurons'][j]); 
                    pData[-1]['grCe_grSu6Ne'].append(cData['StimResp'][n+28]['neurons'][j]); 
                    pData[-1]['grCe_grSu12Mi'].append(cData['StimResp'][n+37]['neurons'][j]); 
                    pData[-1]['grCe_grSu18Fa'].append(cData['StimResp'][n+46]['neurons'][j]); 
                    pData[-1]['grCe_grSu12SmCiNe'].append(cData['StimResp'][n+55]['neurons'][j]); 
                
            elif cData['filename'][20:27]=='Sep2019':            
                """
                No stim (0)
                Gray Center Alone (1-8)
                Gray Surround 1 Near Alone (9)
                Gray Center + Gray Surround 1 Near (10-17)
                Gray Surround 3 Near Alone (18)
                Gray Center + Gray Surround 3 Near (19-26)
                Gray Surround 6 Near Alone (27)
                Gray Center + Gray Surround 6 Near (28-35)
                Gray Surround 12 Middle Alone (36)
                Gray Center + Gray Surround 12 Middle (37-44)
                Gray Surround 18 Far Alone (45)
                Gray Center + Gray Surround 18 Far (46-53)
                Gray Surround 6 Circle Near Alone (54)
                Gray Center + Gray Surround 6 Circle Near (55-62)
                Gray Surround 12 Small Near Alone (63)
                Gray Center + Gray Surround 12 Small Near (64-71)
                Color Center alone (72-79)
                Color Center + Gray Surround 6 Near (80-87)  
                Gray Center + Gray Surround 6 Near (PS) (88-95)  
                Gray Center + Gray Surround 6 Circle Near (PS) (96-103)  
                Gray Center + Gray Surround 12 Small Near (PS)  (104-111)  
                """            
                pData[-1]['NoStim'] = cData['StimResp'][0]['neurons'][j]; 
                pData[-1]['grCe'] = []; 
                pData[-1]['grSu1Ne'] = cData['StimResp'][9]['neurons'][j];
                pData[-1]['grCe_grSu1Ne'] = []; 
                pData[-1]['grSu3Ne'] = cData['StimResp'][18]['neurons'][j]; 
                pData[-1]['grCe_grSu3Ne'] = [];             
                pData[-1]['grSu6Ne'] = cData['StimResp'][27]['neurons'][j];             
                pData[-1]['grCe_grSu6Ne'] = [];                  
                pData[-1]['grSu12Mi'] = cData['StimResp'][36]['neurons'][j];                         
                pData[-1]['grCe_grSu12Mi'] = [];                              
                pData[-1]['guSu18Fa'] = cData['StimResp'][45]['neurons'][j];                         
                pData[-1]['grCe_grSu18Fa'] = [];                              
                pData[-1]['grSu6CiNe'] = cData['StimResp'][54]['neurons'][j];                 
                pData[-1]['grCe_grSu6CiNe'] = [];                                 
                pData[-1]['grSu12SmNe'] = cData['StimResp'][63]['neurons'][j];                 
                pData[-1]['grCe_grSu12SmNe'] = [];                                 
                pData[-1]['coCe'] = [];                                 
                pData[-1]['coCe_grSu6Ne'] = [];                               
                pData[-1]['grCe_grSu6Ne_PS'] = [];                 
                pData[-1]['grCe_grSu6CiNe_PS'] = [];                 
                pData[-1]['grCe_grSu12SmNe_PS'] = [];                 
                pData[-1]['grCe_grSu12SmCiNe_PS'] = [];                             
    
                for n in range(8):
                    pData[-1]['grCe'].append(cData['StimResp'][n+1]['neurons'][j]);      
                    pData[-1]['grCe_grSu1Ne'].append(cData['StimResp'][n+10]['neurons'][j]); 
                    pData[-1]['grCe_grSu3Ne'].append(cData['StimResp'][n+19]['neurons'][j]); 
                    pData[-1]['grCe_grSu6Ne'].append(cData['StimResp'][n+28]['neurons'][j]); 
                    pData[-1]['grCe_grSu12Mi'].append(cData['StimResp'][n+37]['neurons'][j]); 
                    pData[-1]['grCe_grSu18Fa'].append(cData['StimResp'][n+46]['neurons'][j]); 
                    pData[-1]['grCe_grSu6CiNe'].append(cData['StimResp'][n+55]['neurons'][j]);
                    pData[-1]['grCe_grSu12SmNe'].append(cData['StimResp'][n+64]['neurons'][j]); 
                    pData[-1]['coCe'].append(cData['StimResp'][n+72]['neurons'][j]);    
                    pData[-1]['coCe_grSu6Ne'].append(cData['StimResp'][n+80]['neurons'][j]);   
                    pData[-1]['grCe_grSu6Ne_PS'].append(cData['StimResp'][n+88]['neurons'][j]);   
                    pData[-1]['grCe_grSu6CiNe_PS'].append(cData['StimResp'][n+96]['neurons'][j]);   
                    pData[-1]['grCe_grSu12SmNe_PS'].append(cData['StimResp'][n+104]['neurons'][j]);   
                
            elif cData['filename'][20:27]=='Oct2019':                        
                """
                No stim (0)
                Gray Center Alone (1-8)
                Gray Surround 1 Near Alone (9)
                Gray Center + Gray Surround 1 Near (10-17)
                Gray Surround 3 Near Alone (18)
                Gray Center + Gray Surround 3 Near (19-26)
                Gray Surround 6 Near Alone (27)
                Gray Center + Gray Surround 6 Near (28-35)
                Gray Surround 12 Middle Alone (36)
                Gray Center + Gray Surround 12 Middle (37-44)
                Gray Surround 18 Far Alone (45)
                Gray Center + Gray Surround 18 Far (46-53)
                Gray Surround 6 Circle Near Alone (54)
                Gray Center + Gray Surround 6 Circle Near (55-62)
                Gray Surround 12 Small Near Alone (63)
                Gray Center + Gray Surround 12 Small Near (64-71)
                Gray Surround 12 Small Circle Near Alone (72)
                Gray Center + Gray Surround 12 Small Circle Near (73-80)
                Color Center Alone (81-88)
                Color Center + Gray Surround 6 Near (89-96)
                Color Surround 6 Near Alone (97)
                Gray Center + Color Surround 6 Near (98-105)
                Gray Center + Gray Surround 6 Near (PS) (106-113)
                Gray Center + Gray Surround 6 Circle Near (PS) (114-121)
                Gray Center + Gray Surround 12 Small Near (PS) (122-129)
                Gray Center + Gray Surround 12 Small Circle Near (PS) (130-137)
                """
                pData[-1]['NoStim'] = cData['StimResp'][0]['neurons'][j]; 
                pData[-1]['grCe'] = []; 
                pData[-1]['grSu1Ne'] = cData['StimResp'][9]['neurons'][j];
                pData[-1]['grCe_grSu1Ne'] = []; 
                pData[-1]['grSu3Ne'] = cData['StimResp'][18]['neurons'][j]; 
                pData[-1]['grCe_grSu3Ne'] = [];             
                pData[-1]['grSu6Ne'] = cData['StimResp'][27]['neurons'][j];             
                pData[-1]['grCe_grSu6Ne'] = [];                  
                pData[-1]['grSu12Mi'] = cData['StimResp'][36]['neurons'][j];                         
                pData[-1]['grCe_grSu12Mi'] = [];                              
                pData[-1]['guSu18Fa'] = cData['StimResp'][45]['neurons'][j];                         
                pData[-1]['grCe_grSu18Fa'] = [];                              
                pData[-1]['grSu6CiNe'] = cData['StimResp'][54]['neurons'][j];                 
                pData[-1]['grCe_grSu6CiNe'] = [];                                 
                pData[-1]['grSu12SmNe'] = cData['StimResp'][63]['neurons'][j];                 
                pData[-1]['grCe_grSu12SmNe'] = [];                                 
                pData[-1]['grSu12SmCiNe'] = cData['StimResp'][72]['neurons'][j];                 
                pData[-1]['grCe_grSu12SmCiNe'] = [];      
                pData[-1]['coCe'] = [];                                 
                pData[-1]['coCe_grSu6Ne'] = [];                           
                pData[-1]['coSu6Ne'] = cData['StimResp'][97]['neurons'][j];      
                pData[-1]['grCe_coSu6Ne'] = [];                 
                pData[-1]['grCe_grSu6Ne_PS'] = [];                 
                pData[-1]['grCe_grSu6CiNe_PS'] = [];                 
                pData[-1]['grCe_grSu12SmNe_PS'] = [];                 
                pData[-1]['grCe_grSu12SmCiNe_PS'] = [];                             
    
                for n in range(8):
                    pData[-1]['grCe'].append(cData['StimResp'][n+1]['neurons'][j]);      
                    pData[-1]['grCe_grSu1Ne'].append(cData['StimResp'][n+10]['neurons'][j]); 
                    pData[-1]['grCe_grSu3Ne'].append(cData['StimResp'][n+19]['neurons'][j]); 
                    pData[-1]['grCe_grSu6Ne'].append(cData['StimResp'][n+28]['neurons'][j]); 
                    pData[-1]['grCe_grSu12Mi'].append(cData['StimResp'][n+37]['neurons'][j]); 
                    pData[-1]['grCe_grSu18Fa'].append(cData['StimResp'][n+46]['neurons'][j]); 
                    pData[-1]['grCe_grSu6CiNe'].append(cData['StimResp'][n+55]['neurons'][j]);
                    pData[-1]['grCe_grSu12SmNe'].append(cData['StimResp'][n+64]['neurons'][j]); 
                    pData[-1]['grCe_grSu12SmCiNe'].append(cData['StimResp'][n+73]['neurons'][j]); 
                    pData[-1]['coCe'].append(cData['StimResp'][n+81]['neurons'][j]);    
                    pData[-1]['coCe_grSu6Ne'].append(cData['StimResp'][n+89]['neurons'][j]);   
                    pData[-1]['grCe_coSu6Ne'].append(cData['StimResp'][n+98]['neurons'][j]);   
                    pData[-1]['grCe_grSu6Ne_PS'].append(cData['StimResp'][n+106]['neurons'][j]);   
                    pData[-1]['grCe_grSu6CiNe_PS'].append(cData['StimResp'][n+114]['neurons'][j]);   
                    pData[-1]['grCe_grSu12SmNe_PS'].append(cData['StimResp'][n+122]['neurons'][j]);   
                    pData[-1]['grCe_grSu12SmCiNe_PS'].append(cData['StimResp'][n+130]['neurons'][j]); 
            
            print(pData[-1]['filename']+' - ',str(len(pData))+' was done');                   
        del cData;
    
    savedir = '../../../2.DataFiles/ProcessedFiles/ClutterStim/'
    f = gzip.GzipFile(savedir+'ClutterStimDB.json.gz','w');
    f.write(json.dumps(pData, cls=NumpyEncoder).encode('utf-8'));
    f.close();
else:
    print('Current DB file is up-to-date')