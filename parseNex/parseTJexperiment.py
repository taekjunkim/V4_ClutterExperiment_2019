#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 18:33:18 2019

parse nex file using nexfile provided by "https://www.neuroexplorer.com/downloadspage/"
neo.io.NeuroExplorerIO has some errors
1) cannot load waveform
2) cannot read onset time of each analog signal fragment

@author: taekjunkim
"""
#%%
import nexfile;
import numpy as np;

#%%
def main(filename,prevTime,numStims):

    reader = nexfile.Reader(useNumpy=True);
    fData = reader.ReadNexFile(filename);

    nvar, names, types = nex_info(fData);

#%% spikets
    neuronid = names[np.where(types==0)].tolist();
    numNeurons = len(neuronid);

    spikets = [];
    for i in np.arange(numNeurons):
        ts = nex_ts(fData, neuronid[i]);
        spikets.append(ts);

#%% markerts, markervals
    Strobed_chIdx = np.where(names=='Strobed')[0][0];
    markerts = fData['Variables'][Strobed_chIdx]['Timestamps'];    
    markervals = np.array(fData['Variables'][Strobed_chIdx]['Markers'],dtype=int)[0];

#%% get parseParams
    parseParams = get_parseParams();
    
#%% photodiode from CRT
    """
    ts = nex_ts(fData, parseParams['pdiodeChannel']);
    pdAboveDists = ts[1:] - ts[:-1];
    pdOnTS = np.append(ts[0],
                       ts[np.where(pdAboveDists > parseParams['pdiodeDistanceThreshold'])[0]+1]);
    pdOffTS = np.append(ts[np.where(pdAboveDists > parseParams['pdiodeDistanceThreshold'])[0]],ts[-1]);
    """
#%% photodiode from LCD
    adfreq, ts, fn, d = nex_cont(fData, 'AD14'); ## different depending on Rigs
    d2 = d[1:] - d[:-1];
    ts_old = ts[:];
    ts = [];
    for i in np.arange(len(fn)):
        ts = np.append(ts,np.linspace(0,fn[i]/adfreq,fn[i])+ts_old[i]);

    pdOnTS_raw = ts[np.where(d2>0.2)[0]+1];
    pdOffTS_raw = ts[np.where(d2<-0.2)[0]+1];    
    
    pdOn_dist = pdOnTS_raw[1:] - pdOnTS_raw[:-1];
    pdOnTS = np.append(pdOnTS_raw[0],
                       pdOnTS_raw[np.where(pdOn_dist>0.02)[0]+1]);

    pdOff_dist = pdOffTS_raw[1:] - pdOffTS_raw[:-1];
    pdOffTS = np.append(pdOffTS_raw[0],
                        pdOffTS_raw[np.where(pdOff_dist>0.02)[0]+1]);

    del pdOnTS_raw, pdOffTS_raw, pdOn_dist, pdOff_dist;

#%% Get experiment parameters (Task parameters) sent from Pype to Plexon
    counter = 0;
    experiment = dict();
    postTime = prevTime;
    experiment['iti_start'] = [];
    experiment['iti_end'] = [];    
    experiment['numNeurons'] = numNeurons;        
    experiment['neuronid'] = neuronid;        
    experiment['prevTime'] = prevTime;                        
    experiment['postTime'] = postTime;                            
    
    if markervals[counter] != parseParams['rfxCode']:
        print('markerval #'+str(counter)+' was not rfxCode');
    else:
        experiment['rfx'] = markervals[counter+1] - parseParams['yOffset'];
        counter = counter + 2;
        
    if markervals[counter] != parseParams['rfyCode']:
        print('markerval #'+str(counter)+' was not rfyCode');
    else:
        experiment['rfy'] = markervals[counter+1] - parseParams['yOffset'];
        counter = counter + 2;
    
    if markervals[counter] != parseParams['stimWidthCode']:
        print('markerval #'+str(counter)+' was not stimWidthCode');
    else:
        experiment['StimSize'] = markervals[counter+1] - parseParams['yOffset'];
        counter = counter + 2;

    if markervals[counter] != parseParams['itiCode']:
        print('markerval #'+str(counter)+' was not itiCode');
    else:
        experiment['iti'] = markervals[counter+1];
        counter = counter + 2;
    
    if markervals[counter] != parseParams['stim_timeCode']:
        print('markerval #'+str(counter)+' was not stim_timeCode');
    else:
        experiment['StimDur'] = markervals[counter+1];
        counter = counter + 2;
        
    if markervals[counter] != parseParams['isiCode']:
        print('markerval #'+str(counter)+' was not isiCode');
    else:
        experiment['isi'] = markervals[counter+1];
        counter = counter + 2;
        
    if markervals[counter] != parseParams['stim_numCode']: # Number of stimuli per trial
        print('markerval #'+str(counter)+' was not stim_numCode');
    else:
        #experiment['stim_num'] = markervals[counter+1];
        counter = counter + 2;
        

#%% Prepare StimStructs
    stimStructs = [];
    for i in np.arange(numStims):
        stimStructs.append(dict());
        stimStructs[i]['numInstances'] = 0;
        stimStructs[i]['timeOn'] = [];
        stimStructs[i]['timeOff'] = [];
        stimStructs[i]['pdOn'] = [];
        stimStructs[i]['pdOff'] = [];
        stimStructs[i]['neurons'] = [];        
        for j in np.arange(numNeurons):
            stimStructs[i]['neurons'].append(dict());

#%% Prepare to get stimulus information parameters                
    stimITIOns = np.where(markervals==parseParams['startITICode'])[0];
    if stimITIOns[0] != counter:
        print('The first start_iti code is offset');
    stimOns = np.where(markervals==parseParams['stimOnCode'])[0];        
    
    error_indices = [];
    completedITIs = 0;
    
#%% Get stimuli
    for i in np.arange(len(stimITIOns)-1): # the file should end with 
                                           # a startITI that we don't care about    
        if stimITIOns[i] < counter:
            continue;

        index = stimITIOns[i] + 1;
        next_code = markervals[index];

        if next_code == parseParams['endITICode']:
            experiment['iti_start'].append(markerts[stimITIOns[i]]);
            experiment['iti_end'].append(markerts[index]);
            completedITIs = completedITIs + 1;

        elif next_code == parseParams['pauseCode']:    
            if markervals[index+1] != parseParams['unpauseCode']:
                print('Found pause, but no unpause at '+str(index+1));
                print('continuing from next start_iti');                
                error_indices.append(index);           
                continue;
            index = index + 2;
            next_code = markervals[index];

            if next_code == parseParams['endITICode']:
                experiment['iti_start'].append(markerts[stimITIOns[i]]);
                experiment['iti_end'].append(markerts[index]);
                completedITIs = completedITIs + 1;
            else:
                print('Found bad code '+str(next_code)+' after start_iti at index '+str(index));
                print('continuing from next start_iti');                
                error_indices.append(index);           
                continue;

        else:                
            print('Found bad code '+str(next_code)+' after start_iti at index '+str(index));
            print('continuing from next start_iti');                
            error_indices.append(index);           
            continue;

        next_code2 = markervals[index+1];
        if next_code2 == parseParams['fixAcquiredCode']:
            pass;
        elif next_code2 == parseParams['UninitiatedTrialCode']:
            if markervals[index+2] != parseParams['startITICode']:
                error_indices.append(index+2);
                print('Found non start_iti code '+str(markervals[index+2])+
                      ' after Uninitiated trial at '+str(index+2));
            continue;
        else:
            print('Found bad code '+str(next_code2)+' after end_iti at index '
                  +str(stimITIOns[i]+2));
            error_indices.append(index);           
            continue;

        ndex = index + 2;
        trialCode = [];

        while (trialCode == []):        
            stimTimeCodeToStore = [];
            optionalCode = 0;
            
            stimCode = markervals[ndex+optionalCode];
            
            if stimCode == parseParams['fixLost']:
                if hasValidBreakFix(ndex+optionalCode,markervals,parseParams):
                    trialCode = parseParams['breakFixCode'];
                    continue;
            elif stimCode != parseParams['stimIDCode']:
                print('Found '+str(stimCode)+' as a stimID or breakfix code at stim time '
                      +str(markerts[ndex+optionalCode])+' at index '+str(ndex+optionalCode));
                print('continuing from next start_iti');                            
                error_indices.append(ndex+optionalCode);
                trialCode = parseParams['codeError'];
                continue;
                
            if markervals[ndex+1+optionalCode] == parseParams['fixLost']:
                if hasValidBreakFix(ndex+1+optionalCode,markervals,parseParams):
                    trialCode = parseParams['breakFixCode'];
                    continue;
            elif ((markervals[ndex+1+optionalCode] >= parseParams['stimIDOffset']) 
                  and (markervals[ndex+1+optionalCode] < parseParams['stimRotOffset'])): 
                stimIDCodeToStore = markervals[ndex+1+optionalCode];
            else:
                print('Found '+str(markervals[ndex+1])+' as a stimulus code at stim time '
                      +str(markerts[ndex+1+optionalCode])+' at index '+str(ndex+1+optionalCode));
                print('continuing from next start_iti');                            
                error_indices.append(ndex+optionalCode+1);
                trialCode = parseParams['codeError'];
                continue;                

            ## next code is either fixlost or stimOn
            codeIndex = ndex + 2 + optionalCode;
            code = markervals[codeIndex];
            if code == parseParams['fixLost']:
                if hasValidBreakFix(codeIndex,markervals,parseParams):
                    trialCode = parseParams['breakFixCode'];
                    continue;
            elif code != parseParams['stimOnCode']:          
                print('Missing StimOn or fixlost code, found '+str(code)+' at '+str(codeIndex))
                print('continuing from next start_iti');                                        
                error_indices.append(codeIndex);
                trialCode = parseParams['codeError'];
                continue;                
            else:
                stimOnTime = markerts[codeIndex];
                
            ## next code is either fixlost or stimOff
            codeIndex = ndex + 3 + optionalCode;
            code = markervals[codeIndex];
            if code == parseParams['fixLost']:
                if hasValidBreakFix(codeIndex,markervals,parseParams):
                    trialCode = parseParams['breakFixCode'];
                    continue;
            elif code != parseParams['stimOffCode']:          
                print('Missing StimOff or fixlost code, found '+str(code)+' at '+str(codeIndex))
                print('continuing from next start_iti');                                        
                error_indices.append(codeIndex);
                trialCode = parseParams['codeError'];
                continue;                
            else:
                stimOffTime = markerts[codeIndex];
                
            ## having made it here, we can now call this a completed stimulus presentation and record the results                
            sIndex = stimIDCodeToStore - parseParams['stimIDOffset'];
            sIndex = sIndex - 1; # for zero-based indexing in python (Matlab doesn't need this);
            if stimStructs[sIndex]['numInstances'] == []:
                stimStructs[sIndex]['numInstances'] = 1;
            else:                    
                stimStructs[sIndex]['numInstances'] = stimStructs[sIndex]['numInstances'] + 1;
                
            inst = stimStructs[sIndex]['numInstances'];
            inst = inst - 1; # for zero-based indexing in python (Matlab doesn't need this);
            stimStructs[sIndex]['timeOn'].append(stimOnTime);               
            stimStructs[sIndex]['timeOff'].append(stimOffTime);                               
            
            ## now find the pdiode events associated with
            pdOnsAfter = np.where(pdOnTS > stimOnTime)[0];
            if len(pdOnsAfter)==0:
                print('Error, did not find a photodiode on code after stimon at time '+str(stimOnTime));
                print('Ignoring... Continuing');
            else:
                pdOffsAfter = np.where(pdOffTS > pdOnTS[pdOnsAfter[0]])[0];
                if len(pdOffsAfter)==0:
                    print('Error, did not find a photodiode on code after stimon at time '+str(pdOnTS[pdOnsAfter[0]]));
                    print('Ignoring... Continuing');
                else:
                    stimStructs[sIndex]['pdOn'].append(pdOnTS[pdOnsAfter[0]]);
                    stimStructs[sIndex]['pdOff'].append(pdOffTS[pdOffsAfter[0]]);                    

            ## now get neural data
            for j in np.arange(numNeurons):
                mySpikes = np.array([]);
                if stimStructs[sIndex]['pdOff'] != []:
                    spikeIndices = np.where((spikets[j] >= (stimOnTime-prevTime)) & 
                                            (spikets[j] <= (stimStructs[sIndex]['pdOff'][inst]+postTime)))[0];
                else:
                    spikeIndices = np.where((spikets[j] >= (stimOnTime-prevTime)) & 
                                            (spikets[j] <= (stimOffTime+postTime)))[0];
                                            
                if len(spikeIndices)>0:
                    mySpikes = np.append(mySpikes,spikets[j][spikeIndices]);
                if inst == 0:
                    stimStructs[sIndex]['neurons'][j]['spikes'] = [];
                stimStructs[sIndex]['neurons'][j]['spikes'].append(mySpikes);    
                
            ## next code is either fixlost, an object code or correct_response
            codeIndex = ndex + 4 + optionalCode;
            code = markervals[codeIndex];

            if code == parseParams['fixLost']:
                if hasValidBreakFix(codeIndex,markervals,parseParams):
                    trialCode = parseParams['breakFixCode'];
                    continue;
            elif code == parseParams['correctCode']: # end of trial
                if markervals[codeIndex+1] != parseParams['startITICode']:
                    print('Missing startITI after '+str(markervals[codeIndex+1])+
                          ' at '+str(markerts[codeIndex+1])+' at index '+
                          str(codeIndex+1));
                    error_indices.append(codeIndex);
                    trialCode = parseParams['codeError'];
                    continue;                
                else:
                    trialCode = parseParams['correctCode'];
                    continue;
            elif code != parseParams['stimIDCode']:
                print('Found '+str(stimCode)+' as a stim ID code at stim time '+
                      str(markerts[codeIndex]));
                print('continuing from next start_iti');                        
                error_indices.append(codeIndex);
                trialCode = parseParams['codeError'];
                continue;                
            else:
                ndex = ndex + 4 + optionalCode;                    
                                    
#%% add stimStructs to experiment output, then return
    experiment['stimStructs'] = stimStructs;                        
    experiment['errors'] = error_indices;
    
    return experiment;

#%% hasValidBreakFix
def hasValidBreakFix(ndex, markervals, parseParams):
    if markervals[ndex+1] != parseParams['breakFixCode']:
        print('missing breakFixCode after '+str(markervals[ndex])+
              ' at index '+str(ndex));
    if markervals[ndex+2] != parseParams['startITICode']:
        print('missing startITI after '+str(markervals[ndex+1])+
              ' at index '+str(ndex));
    yesno = 1;    
    return yesno;


#%% nex_info
"""
nvar, names, types = nex_info(fData):
nvar: number of variables in the file
names: [nvar 64] array of variable names
types: [1 nvar] array of variable types
Interpretation of type values: 0-neuron, 1-event, 2-interval, 3-waveform, 
                               4-population vector, 5-continuous variable, 6 - marker
"""                               

def nex_info(fData):
    nvar = len(fData['Variables']);
    names = [];
    types = [];
    for i in np.arange(nvar):
        names.append(fData['Variables'][i]['Header']['Name']);
        types.append(fData['Variables'][i]['Header']['Type']);     
    names = np.array(names);    
    types = np.array(types);    
    return nvar, names, types

#%% nex_ts
"""
ts = nex_ts(fData, varname)
Read timestamps from a .nex file
ts - array of timestamps (in seconds)
"""                               

def nex_ts(fData,varname):
    nvar = len(fData['Variables']);
    for i in np.arange(nvar):
        if fData['Variables'][i]['Header']['Name'] == varname:
            ts = fData['Variables'][i]['Timestamps'];
            break;
    return ts;

#%% nex_cont
"""
adfreq, ts, fn, d = nex_cont(fData, varname)
 
continuous (a/d) data come in fragments. Each fragment has a timestamp
and a number of a/d data points. The timestamp corresponds to
the time of recording of the first a/d value in this fragment.
All the data values stored in the vector d. 

OUTPUT:
    adfreq - sampling frequency of analog data 
    ts - array of fragment timestamps (one timestamp for fragment, in seconds)
    fn - number of data points in each fragment
    d - array of a/d values (in millivolts)
"""                               

def nex_cont(fData,varname):
    nvar = len(fData['Variables']);
    for i in np.arange(nvar):
        if fData['Variables'][i]['Header']['Name'] == varname:
            adfreq = fData['Variables'][i]['Header']['SamplingRate'];
            ts = fData['Variables'][i]['FragmentTimestamps'];
            fn = fData['Variables'][i]['FragmentCounts'];            
            d = fData['Variables'][i]['ContinuousValues'];                        
            break;
    return adfreq, ts, fn, d;
#%% Load parameters, which will be compared with markervals
def get_parseParams():    
    parseParams = {};
    parseParams['add_extra_isiCode'] = 67;
    parseParams['background_infoCode'] = 70;
    parseParams['bar_downCode'] = 26;
    parseParams['bar_upCode'] = 25;
    parseParams['blackRespIndex'] = 101;
    parseParams['blank'] = 1;
    parseParams['breakFixCode'] = 6;
    parseParams['codeError'] = -1;
    parseParams['colorCode'] = 42;
    parseParams['correctCode'] = 0;
    parseParams['distanceThreshold'] = 10;
    parseParams['dot_radCode'] = 63;
    parseParams['EARLY_RELEASECode'] = 4;
    parseParams['end_post_trialCode'] = 19;
    parseParams['end_pre_trialCode'] = 17;
    parseParams['end_wait_barCode'] = 24;
    parseParams['end_wait_fixationCode'] = 21;
    parseParams['endITICode'] = 13;
    parseParams['extraCode'] = 74;
    parseParams['eye_startCode'] = 14;
    parseParams['eye_stopCode'] = 15;
    parseParams['fix_doneCode'] = 34;
    parseParams['fix_offCode'] = 30;
    parseParams['fix_onCode'] = 29;
    parseParams['fixAcquiredCode'] = 31;
    parseParams['fixation_occursCode'] = 22;
    parseParams['fixLost'] = 33;
    parseParams['foreground_infoCode'] = 69;
    parseParams['gen_modeCode'] = 65;
    parseParams['gen_submodeCode'] = 66;
    parseParams['isiCode'] = 47;
    parseParams['itiCode'] = 45;
    parseParams['LATE_RESPCode'] = 5;
    parseParams['line_widthCode'] = 64;
    parseParams['location_flip_infoCode'] = 73;
    parseParams['mask_infoCode'] = 54;
    parseParams['mask_offCode'] = 56;
    parseParams['mask_onCode'] = 55;
    parseParams['maxCode'] = 4095;
    parseParams['maxColorValue'] = 256;
    parseParams['MAXRT_EXCEEDEDCode'] = 3;
    parseParams['midground_infoCode'] = 68;
    parseParams['NO_RESPCode'] = 8;
    parseParams['occl_infoCode'] = 53;
    parseParams['occlmodeCode'] = 52;
    parseParams['occlshapeCode'] = 62;
    parseParams['OneBasedIndexing'] = 1;
    parseParams['onset_timeCode'] = 71;
    parseParams['pauseCode'] = 100;
    parseParams['pdiodeChannel'] = 'Event002';
    parseParams['pdiodeDistanceThreshold'] = 0.02;
    parseParams['pdiodeThresh'] = 4.8;
    parseParams['perispaceCode'] = 61;
    parseParams['plexFloatMultCode'] = 1000;
    parseParams['plexYOffsetCode'] = 600;
    parseParams['positionCode'] = 57;
    parseParams['radius_code'] = 80;
    parseParams['rewardCode'] = 37;
    parseParams['rfxCode'] = 43;
    parseParams['rfyCode'] = 44;
    parseParams['rotIDCode'] = 50;
    parseParams['second_stimuliCode'] = 72;
    parseParams['start_post_trialCode'] = 18;
    parseParams['start_pre_trialCode'] = 16;
    parseParams['start_spontCode'] = 35;
    parseParams['start_trialCode'] = 10;
    parseParams['start_wait_barCode'] = 23;
    parseParams['start_wait_fixationCode'] = 20;
    parseParams['startITICode'] = 12;
    parseParams['stim_numCode'] = 48;
    parseParams['stim_timeCode'] = 46;
    parseParams['stimColors'] = [];
    parseParams['stimdurCode'] = 51;
    parseParams['stimHeightCode'] = 59;
    parseParams['stimIDCode'] = 49;
    parseParams['stimIDOffset'] = 200;
    parseParams['stimOffCode'] = 39;
    parseParams['stimOnCode'] = 38;
    parseParams['stimRotOffset'] = 3736;
    parseParams['stimShapeCode'] = 60;
    parseParams['stimWidthCode'] = 58;
    parseParams['stop_spontCode'] = 36;
    parseParams['stop_trialCode'] = 11;
    parseParams['strobeBitChannel'] = 'AD17';
    parseParams['strobeThresh'] = 2;
    parseParams['targets_offCode'] = 41;
    parseParams['targets_onCode'] = 40;
    parseParams['test_offCode'] = 28;
    parseParams['test_onCode'] = 27;
    parseParams['UninitiatedTrialCode'] = 2;
    parseParams['unpauseCode'] = 101;
    parseParams['USER_ABORTCode'] = 1;
    parseParams['WRONG_RESPCode'] = 7;
    parseParams['yOffset'] = 600;
    return parseParams
