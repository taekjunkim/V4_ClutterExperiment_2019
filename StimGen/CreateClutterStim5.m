%%% CreateClutterStim: 8 Shapes, 10 Repetition
%%% RF size is assumed to be 100x100 pixels
%%% Inter-Stimulus distance will be fixed as 0.5xRF, 1xRF, 1.5xRF
%%% Stimulus size: 0.5xRF

%%% No stim (1)
%%% Gray Center alone (2-9)
%%% Gray 1 Surround alone (10)
%%% Gray Center + Gray 1 Surround (11-18)
%%% Gray 3 Surround alone (19)
%%% Gray Center + Gray 3 Surround (20-27)
%%% Gray 6 Surround alone (28)
%%% Gray Center + Gray 6 Surround (Near) (29-36)
%%% Gray 12 Surround alone (37)
%%% Gray Center + Gray 12 Surround (Middle) (38-45)
%%% Gary 18 Surround alone (46)
%%% Gray Center + Gray 18 Surround (Far) (47-54)
%%% Gray 6 Circle Surround alone (55)
%%% Gray Center + Gray 6 Circle Surround (56-63)
%%% Gray 12 Small Near Surround alone (64)
%%% Gray Center + Gray 12 Small Near Surround (65-72)
%%% Gray 12 Small Near Circle Surround alone (73)
%%% Gray Center + Gray 12 Small Near Circle Surround (74-81)
%%% Color center alone (82-89)
%%% Color Center + Gray 6 Surround (Near) (90-97)
%%% Color 6 Surround alone (98)
%%% Gray Center + Color 6 Surround (Near) (99-106)

%%% Gray Center + Gray 6 Surround (PS) (107-114)
%%% Gray Center + Gray 6 Circle Surround (PS) (115-122)
%%% Gray Center + Gray 12 Small Near Surround (PS) (123-130)
%%% Gray Center + Gray 12 Small Near Circle Surround (PS) (131-138)

%%
NumRepeat = 10;

%% Color parameter: work only for mono-chromatic (R,G,B same);
FGcolor = [100 100 100];   %%% Center color
FGcolor2 = [100 100 100];  %%% Surround color
FGcolor3 = [70 70 70];  %%% Surround color in 6 Circle Surround condition and 12 Small Circle Surround condition
BGcolor = [40 40 40];

%% stimulus parameter
ShapeID = 16;
XY_jitter = 1; %%% even when 1, circle surround & center stimuli will have 0;
C_jitter = 1;  %%% even when 1, circle surround & center stimuli will have 0; 0.6,0.75,0.9
NumSurround = [1 3 6 12];  %%% Number conditions (1,3,6), 12 for small surround

%% RF parameter
RFsize = 100;
StimField = [RFsize*4 RFsize*4]; %%% 4xRF
scaleFactor1 = (140/100)*RFsize; %% To make Circle diameter 100 (load & see ShapeAll)

scaleFactor2 = 0.5;
StimSize_general = floor(scaleFactor1*scaleFactor2); %% for general stimuli
StimSize_circle = floor(0.95*StimSize_general); %% for circle surround stimuli
StimSize_small = floor(0.5*StimSize_general); %% for small surround stimuli

BGfield = ones(StimField(1),StimField(2),3);
for c=1:3
    BGfield(:,:,c) = BGfield(:,:,c)*BGcolor(c);
end

%% Creating center
load ShapeAll;
ShapeChosen = [];   k = 0;
for s=1:length(ShapeInfo)
    if ShapeInfo(s).StimIdx == ShapeID
       ShapeChosen = [ShapeChosen s];  
       CurrImg = BGfield;
       PatchNow = ShapeInfo(s).StimMtx;
       PatchNow = imresize(PatchNow,[StimSize_general StimSize_general]);
       NewImg = ApplyPatch(CurrImg, [0 0], PatchNow, FGcolor, 0, 0); % XYjitter=0, Cjitter=0 
       CurrImg = NewImg;
       k = k+1;
       CenterStim(k).Img = CurrImg;
    end
end
disp('Center stimulus were created');

%% Creating surround
for r=1:NumRepeat %%% repetition
    %%% 1 Surround: Dist1
    ISD = RFsize/2;   
    NumSurrHere = NumSurround(1);
    RotOffset = (r-1)*360/(NumRepeat*NumSurrHere);
    CurrImg = BGfield;
    updateImg = AddByRotation(CurrImg,ISD,StimSize_general,RotOffset,NumSurrHere,FGcolor2,XY_jitter,C_jitter,ShapeInfo,99:370);
    Surr1Near(r).Img = updateImg;
    
    %%% 3 Surround: Dist1
    ISD = RFsize/2;
    NumSurrHere = NumSurround(2);
    RotOffset = (r-1)*360/(20*NumSurround(2));
    CurrImg = BGfield;
    updateImg = AddByRotation(CurrImg,ISD,StimSize_general,RotOffset,NumSurrHere,FGcolor2,XY_jitter,C_jitter,ShapeInfo,99:370);
    Surr3Near(r).Img = updateImg;
    
    %%% 6 Surround (Near): Dist1
    ISD = RFsize/2;
    NumSurrHere = NumSurround(3);
    RotOffset = (r-1)*360/(NumRepeat*NumSurrHere);    
    CurrImg = BGfield;
    updateImg = AddByRotation(CurrImg,ISD,StimSize_general,RotOffset,NumSurrHere,FGcolor2,XY_jitter,C_jitter,ShapeInfo,99:370);
    Surr6Near(r).Img = updateImg;
    
    %%% 12 Surround (Middle): Dist2
    ISD = 2*RFsize/2;
    NumSurrHere = NumSurround(3)*2;
    RotOffset = (r-1)*360/(NumRepeat*NumSurrHere);    
    CurrImg = BGfield;
    updateImg = AddByRotation(CurrImg,ISD,StimSize_general,RotOffset,NumSurrHere,FGcolor2,XY_jitter,C_jitter,ShapeInfo,99:370);
    SurrMiddle(r).Img = updateImg;
    
    %%% 18 Surround (Far): Dist3
    ISD = 3*RFsize/2;
    NumSurrHere = NumSurround(3)*3;
    RotOffset = (r-1)*360/(NumRepeat*NumSurrHere);            
    CurrImg = BGfield;
    updateImg = AddByRotation(CurrImg,ISD,StimSize_general,RotOffset,NumSurrHere,FGcolor2,XY_jitter,C_jitter,ShapeInfo,99:370);
    SurrFar(r).Img = updateImg;

    %%% 6 Circle Surround (near): Dist1
    ISD = RFsize/2;
    NumSurrHere = NumSurround(3);
    RotOffset = (r-1)*360/(NumRepeat*NumSurrHere);            
    CurrImg = BGfield;
    updateImg = AddByRotation(CurrImg,ISD,StimSize_circle,RotOffset,NumSurrHere,FGcolor3,0,0,ShapeInfo,[]); %% XY_jitter = 0, C_jitter = 0;
    Surr6NearCircle(r).Img = updateImg;
    
    %%% 12 Small Surround (near): Dist1
    ISD = RFsize/2;
    NumSurrHere = NumSurround(3)*2;
    RotOffset = (r-1)*360/(NumRepeat*NumSurrHere);            
    CurrImg = BGfield;
    updateImg = AddByRotation(CurrImg,ISD,StimSize_small,RotOffset,NumSurrHere,FGcolor2,XY_jitter,C_jitter,ShapeInfo,99:370); %% XY_jitter = 0, C_jitter = 0;
    Surr12NearSmall(r).Img = updateImg;

    %%% 12 Small Circle Surround (near): Dist1
    ISD = RFsize/2;
    NumSurrHere = NumSurround(3)*2;
    RotOffset = (r-1)*360/(NumRepeat*NumSurrHere);            
    CurrImg = BGfield;
    updateImg = AddByRotation(CurrImg,ISD,StimSize_small,RotOffset,NumSurrHere,FGcolor3,0,0,ShapeInfo,[]); %% XY_jitter = 0, C_jitter = 0;
    Surr12NearSmallCircle(r).Img = updateImg;
    
end
disp('Surround stimuli were created');

%% PS parameter
Nsc = 4;
CenterCrop = RFsize*1.5; %% use the center 150x150 (RFsize assumed to be 100)
Nresize = 128;  

Nor = 4; % Number of orientations
Na = 7; % Number of spatial neighbors considered for spatial correlations
Niter = 50; % Number of iterations of the synthesis loop


%% Create PS statistics
for r=1:NumRepeat    
    %%% Center + 6 Surround (Near) (PS)
    for n=1:8
        CurrImg = Surr6Near(r).Img;
        PatchNow = ShapeInfo(ShapeChosen(n)).StimMtx;
        PatchNow = imresize(PatchNow,[StimSize_general StimSize_general]);
        NewImg = ApplyPatch(CurrImg, [0 0], PatchNow, FGcolor, 0, 0);
        CenterSurr6Near(r).shape(n).Img = NewImg;
        
        % use cental 150x150 to compute PS statistics
        CenterRegion = NewImg(floor((StimField(2)-CenterCrop)/2)+1:...
                              floor((StimField(2)-CenterCrop)/2)+CenterCrop,...
                              floor((StimField(1)-CenterCrop)/2)+1:...
                              floor((StimField(1)-CenterCrop)/2)+CenterCrop,1);
        CenterRegion = imresize(CenterRegion,[Nresize Nresize]); 
        CenterRegion = double(CenterRegion);
        [params] = textureAnalysis(CenterRegion, Nsc, Nor, Na);
        count = 0; err_count = 0;
        while count == err_count
            try 
               im = textureSynthesis(params,[Nresize Nresize],Niter); 
            catch
               err_count = err_count+1; 
               close all;
            end
            count = count+1;
        end
        close all;
        imNow = imresize(im,[CenterCrop CenterCrop]);
        for c=1:3
            NewImg(floor((StimField(2)-CenterCrop)/2)+1:...
                   floor((StimField(2)-CenterCrop)/2)+CenterCrop,...
                   floor((StimField(1)-CenterCrop)/2)+1:...
                   floor((StimField(1)-CenterCrop)/2)+CenterCrop,c) = imNow; 
        end
        CenterSurr6Near(r).shape(n).PS_Img = NewImg;
    end
    disp(['CenterSurr6Near: repetition #',num2str(r),' was done']);

    %%% Center + 6 Surround Circle (Near) (PS)
    for n=1:8
        CurrImg = Surr6NearCircle(r).Img;
        PatchNow = ShapeInfo(ShapeChosen(n)).StimMtx;
        PatchNow = imresize(PatchNow,[StimSize_general StimSize_general]);
        NewImg = ApplyPatch(CurrImg, [0 0], PatchNow, FGcolor, 0, 0);
        CenterSurr6NearCircle(r).shape(n).Img = NewImg; 
        
        % use cental 150x150 to compute PS statistics
        CenterRegion = NewImg(floor((StimField(2)-CenterCrop)/2)+1:...
                              floor((StimField(2)-CenterCrop)/2)+CenterCrop,...
                              floor((StimField(1)-CenterCrop)/2)+1:...
                              floor((StimField(1)-CenterCrop)/2)+CenterCrop,1);
        CenterRegion = imresize(CenterRegion,[Nresize Nresize]); 
        CenterRegion = double(CenterRegion);
        [params] = textureAnalysis(CenterRegion, Nsc, Nor, Na);
        count = 0; err_count = 0;
        while count == err_count
            try 
               im = textureSynthesis(params,[Nresize Nresize],Niter); 
            catch
               err_count = err_count+1; 
               close all;
            end
            count = count+1;
        end
        close all;
        imNow = imresize(im,[CenterCrop CenterCrop]);
        for c=1:3
            NewImg(floor((StimField(2)-CenterCrop)/2)+1:...
                   floor((StimField(2)-CenterCrop)/2)+CenterCrop,...
                   floor((StimField(1)-CenterCrop)/2)+1:...
                   floor((StimField(1)-CenterCrop)/2)+CenterCrop,c) = imNow; 
        end
        CenterSurr6NearCircle(r).shape(n).PS_Img = NewImg;
    end
    disp(['CenterSurr6NearCircle: repetition #',num2str(r),' was done']);
    
    %%% Center + 12 Surround Small (Near) (PS)
    for n=1:8
        CurrImg = Surr12NearSmall(r).Img;
        PatchNow = ShapeInfo(ShapeChosen(n)).StimMtx;
        PatchNow = imresize(PatchNow,[StimSize_general StimSize_general]);
        NewImg = ApplyPatch(CurrImg, [0 0], PatchNow, FGcolor, 0, 0);
        CenterSurr12NearSmall(r).shape(n).Img = NewImg;
        
        % use cental 150x150 to compute PS statistics
        CenterRegion = NewImg(floor((StimField(2)-CenterCrop)/2)+1:...
                              floor((StimField(2)-CenterCrop)/2)+CenterCrop,...
                              floor((StimField(1)-CenterCrop)/2)+1:...
                              floor((StimField(1)-CenterCrop)/2)+CenterCrop,1);
        CenterRegion = imresize(CenterRegion,[Nresize Nresize]); 
        CenterRegion = double(CenterRegion);
        [params] = textureAnalysis(CenterRegion, Nsc, Nor, Na);
        count = 0; err_count = 0;
        while count == err_count
            try 
               im = textureSynthesis(params,[Nresize Nresize],Niter); 
            catch
               err_count = err_count+1; 
               close all;
            end
            count = count+1;
        end
        close all;
        imNow = imresize(im,[CenterCrop CenterCrop]);
        for c=1:3
            NewImg(floor((StimField(2)-CenterCrop)/2)+1:...
                   floor((StimField(2)-CenterCrop)/2)+CenterCrop,...
                   floor((StimField(1)-CenterCrop)/2)+1:...
                   floor((StimField(1)-CenterCrop)/2)+CenterCrop,c) = imNow; 
        end
        CenterSurr12NearSmall(r).shape(n).PS_Img = NewImg;
    end
    disp(['CenterSurr12NearSmall: repetition #',num2str(r),' was done']);

    %%% Center + 12 Surround Small Circle (Near) (PS)
    for n=1:8
        CurrImg = Surr12NearSmallCircle(r).Img;
        PatchNow = ShapeInfo(ShapeChosen(n)).StimMtx;
        PatchNow = imresize(PatchNow,[StimSize_general StimSize_general]);
        NewImg = ApplyPatch(CurrImg, [0 0], PatchNow, FGcolor, 0, 0);
        CenterSurr12NearSmallCircle(r).shape(n).Img = NewImg;
        
        % use cental 150x150 to compute PS statistics
        CenterRegion = NewImg(floor((StimField(2)-CenterCrop)/2)+1:...
                              floor((StimField(2)-CenterCrop)/2)+CenterCrop,...
                              floor((StimField(1)-CenterCrop)/2)+1:...
                              floor((StimField(1)-CenterCrop)/2)+CenterCrop,1);
        CenterRegion = imresize(CenterRegion,[Nresize Nresize]); 
        CenterRegion = double(CenterRegion);
        [params] = textureAnalysis(CenterRegion, Nsc, Nor, Na);
        count = 0; err_count = 0;
        while count == err_count
            try 
               im = textureSynthesis(params,[Nresize Nresize],Niter); 
            catch
               err_count = err_count+1; 
               close all;
            end
            count = count+1;
        end
        close all;
        imNow = imresize(im,[CenterCrop CenterCrop]);
        for c=1:3
            NewImg(floor((StimField(2)-CenterCrop)/2)+1:...
                   floor((StimField(2)-CenterCrop)/2)+CenterCrop,...
                   floor((StimField(1)-CenterCrop)/2)+1:...
                   floor((StimField(1)-CenterCrop)/2)+CenterCrop,c) = imNow; 
        end
        CenterSurr12NearSmallCircle(r).shape(n).PS_Img = NewImg;
    end
    disp(['CenterSurr12NearSmallCircle: repetition #',num2str(r),' was done']);
    
end

%% Stimulus crop
% CenterStim
for n=1:length(CenterStim)
    CenterStim(n).Img = CenterStim(n).Img(151:250,151:250,:);
end

% Surr Alone or Center+Surround
for n=1:10
    Surr1Near(n).Img = Surr1Near(n).Img(101:300,101:300,:);
    Surr3Near(n).Img = Surr3Near(n).Img(101:300,101:300,:);
    Surr6Near(n).Img = Surr6Near(n).Img(101:300,101:300,:);
    Surr6NearCircle(n).Img = Surr6NearCircle(n).Img(101:300,101:300,:);
    Surr12NearSmall(n).Img = Surr12NearSmall(n).Img(101:300,101:300,:);   
    Surr12NearSmallCircle(n).Img = Surr12NearSmallCircle(n).Img(101:300,101:300,:);       
    SurrMiddle(n).Img = SurrMiddle(n).Img(51:350,51:350,:);
    
    for m=1:8
        CenterSurr6Near(n).shape(m).Img = CenterSurr6Near(n).shape(m).Img(101:300,101:300,:);
        CenterSurr6Near(n).shape(m).PS_Img = CenterSurr6Near(n).shape(m).PS_Img(101:300,101:300,:);
        
        CenterSurr6NearCircle(n).shape(m).Img = CenterSurr6NearCircle(n).shape(m).Img(101:300,101:300,:);
        CenterSurr6NearCircle(n).shape(m).PS_Img = CenterSurr6NearCircle(n).shape(m).PS_Img(101:300,101:300,:);

        CenterSurr12NearSmall(n).shape(m).Img = CenterSurr12NearSmall(n).shape(m).Img(101:300,101:300,:);
        CenterSurr12NearSmall(n).shape(m).PS_Img = CenterSurr12NearSmall(n).shape(m).PS_Img(101:300,101:300,:);

        CenterSurr12NearSmallCircle(n).shape(m).Img = CenterSurr12NearSmallCircle(n).shape(m).Img(101:300,101:300,:);
        CenterSurr12NearSmallCircle(n).shape(m).PS_Img = CenterSurr12NearSmallCircle(n).shape(m).PS_Img(101:300,101:300,:);
    end
end
disp('Stimuli were center cropped')

%% uint8
% CenterStim
for n=1:length(CenterStim)
    CenterStim(n).Img = uint8(CenterStim(n).Img);
end

% Surr Alone or Center+Surround
for n=1:10
    Surr1Near(n).Img = uint8(Surr1Near(n).Img);
    Surr3Near(n).Img = uint8(Surr3Near(n).Img);
    Surr6Near(n).Img = uint8(Surr6Near(n).Img);
    Surr6NearCircle(n).Img = uint8(Surr6NearCircle(n).Img);
    Surr12NearSmall(n).Img = uint8(Surr12NearSmall(n).Img);
    Surr12NearSmallCircle(n).Img = uint8(Surr12NearSmallCircle(n).Img);
    SurrMiddle(n).Img = uint8(SurrMiddle(n).Img);
    
    for m=1:8
        CenterSurr6Near(n).shape(m).Img = uint8(CenterSurr6Near(n).shape(m).Img);
        CenterSurr6Near(n).shape(m).PS_Img = uint8(CenterSurr6Near(n).shape(m).PS_Img);
        
        CenterSurr6NearCircle(n).shape(m).Img = uint8(CenterSurr6NearCircle(n).shape(m).Img);
        CenterSurr6NearCircle(n).shape(m).PS_Img = uint8(CenterSurr6NearCircle(n).shape(m).PS_Img);

        CenterSurr12NearSmall(n).shape(m).Img = uint8(CenterSurr12NearSmall(n).shape(m).Img);
        CenterSurr12NearSmall(n).shape(m).PS_Img = uint8(CenterSurr12NearSmall(n).shape(m).PS_Img);

        CenterSurr12NearSmallCircle(n).shape(m).Img = uint8(CenterSurr12NearSmallCircle(n).shape(m).Img);
        CenterSurr12NearSmallCircle(n).shape(m).PS_Img = uint8(CenterSurr12NearSmallCircle(n).shape(m).PS_Img);
    end
end
disp('uint8 was done')