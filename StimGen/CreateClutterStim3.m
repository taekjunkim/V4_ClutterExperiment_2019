%%% CreateClutterStim: 8 Shapes, 15 Repetition
%%% RF size is assumed to be 100x100 pixels
%%% Inter-Stimulus distance will be fixed as 0.5xRF, 1xRF, 1.5xRF
%%% Stimulus size: 0.3xRF, 0.5xRF, 0.7xRF

%%% No stim (1)
%%% Center alone (2-9)
%%% 1 Surround alone (10)
%%% Center + 1 Surround (11-18)
%%% 3 Surround alone (19)
%%% Center + 3 Surround (20-27)
%%% 6 Surround alone (28)
%%% Center + 6 Surround (Near) (29-36)
%%% 12 Surround alone (37)
%%% Center + 12 Surround (Middle) (38-45)
%%% 18 Surround alone (46)
%%% Center + 18 Surround (Far) (47-54)
%%% Center + 12 Near Small Circle (Far) (55-62)

%% 
NumRepeat = 15;

%% Color parameter: work only for mono-chromatic (R,G,B same);
FGcolor = [100 100 100];   %%% Center color
FGcolor2 = [100 100 100];  %%% Surround color
FGcolor3 = [70 70 70];  %%% Surround color in salient condition 
BGcolor = [40 40 40];

%% stimulus parameter
ShapeID = 16;
XY_jitter = 1; %%% even when 1, circle surround & center stimuli will have 0;
C_jitter = 1;  %%% even when 1, circle surround & center stimuli will have 0; 0.6,0.7,0.8
NumSurround = [1 3 6 12];  %%% Number conditions (1,3,6), 8 for small surround

%% RF parameter
RFsize = 100;
StimField = [RFsize*4+40 RFsize*4+40]; %%% 4xRF + extra
StimSize100 = (140/100)*RFsize; %% To make Circle diameter 200 (load & see ShapeAll)

scaleFactor = 0.5;
StimSize = floor(StimSize100*scaleFactor);
StimSize3 = floor(0.5*StimSize);

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
       PatchNow = imresize(PatchNow,[StimSize StimSize]);
       NewImg = ApplyPatch(CurrImg, [0 0], PatchNow, FGcolor, 0, 0);
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
    updateImg = AddByRotation(CurrImg,ISD,StimSize,RotOffset,NumSurrHere,FGcolor2,XY_jitter,C_jitter,ShapeInfo,99:370);
    Surr1Near(r).Img = updateImg;
    
    %%% 3 Surround: Dist1
    ISD = RFsize/2;
    NumSurrHere = NumSurround(2);
    RotOffset = (r-1)*360/(20*NumSurround(2));
    CurrImg = BGfield;
    updateImg = AddByRotation(CurrImg,ISD,StimSize,RotOffset,NumSurrHere,FGcolor2,XY_jitter,C_jitter,ShapeInfo,99:370);
    Surr3Near(r).Img = updateImg;
    
    %%% 6 Surround (Near): Dist1
    ISD = RFsize/2;
    NumSurrHere = NumSurround(3);
    RotOffset = (r-1)*360/(NumRepeat*NumSurrHere);    
    CurrImg = BGfield;
    updateImg = AddByRotation(CurrImg,ISD,StimSize,RotOffset,NumSurrHere,FGcolor2,XY_jitter,C_jitter,ShapeInfo,99:370);
    Surr6Near(r).Img = updateImg;
    
    %%% 12 Surround (Middle): Dist2
    ISD = 2*RFsize/2;
    NumSurrHere = NumSurround(3)*2;
    RotOffset = (r-1)*360/(NumRepeat*NumSurrHere);    
    CurrImg = BGfield;
    updateImg = AddByRotation(CurrImg,ISD,StimSize,RotOffset,NumSurrHere,FGcolor2,XY_jitter,C_jitter,ShapeInfo,99:370);
    SurrMiddle(r).Img = updateImg;
    
    %%% 18 Surround (Far): Dist3
    ISD = 3*RFsize/2;
    NumSurrHere = NumSurround(3)*3;
    RotOffset = (r-1)*360/(NumRepeat*NumSurrHere);            
    CurrImg = BGfield;
    updateImg = AddByRotation(CurrImg,ISD,StimSize,RotOffset,NumSurrHere,FGcolor2,XY_jitter,C_jitter,ShapeInfo,99:370);
    SurrFar(r).Img = updateImg;

    %%% 12 Surround (Neaer Small Circle): Dist1
    ISD = RFsize/2;
    NumSurrHere = NumSurround(3)*2;
    RotOffset = (r-1)*360/(NumRepeat*NumSurrHere);            
    CurrImg = BGfield;
    updateImg = AddByRotation(CurrImg,ISD,StimSize3,RotOffset,NumSurrHere,FGcolor3,0,0,ShapeInfo,[]); %% XY_jitter = 0, C_jitter = 0;
    SurrNearSmallCircle(r).Img = updateImg;
    
    
end
disp('Surround stimuli were created');

%% Combine all stimulus set
for r=1:NumRepeat    
    %%% No stim (1)
    StimSet((r-1)*54+1).Img = uint8(BGfield);
    %%% Center alone (2-9)
    for n=1:8
        StimSet((r-1)*54+1+n).Img = uint8(CenterStim(n).Img);
    end
    %%% 1 Surround alone (10)
    StimSet((r-1)*54+10).Img = uint8(Surr1Near(r).Img);
    %%% Center + 1 Surround (11-18)
    for n=1:8
        CurrImg = Surr1Near(r).Img;
        PatchNow = ShapeInfo(ShapeChosen(n)).StimMtx;
        PatchNow = imresize(PatchNow,[StimSize StimSize]);
        NewImg = ApplyPatch(CurrImg, [0 0], PatchNow, FGcolor, 0, 0);
        StimSet((r-1)*54+10+n).Img = uint8(NewImg);
    end
    %%% 3 Surround alone (19)
    StimSet((r-1)*54+19).Img = uint8(Surr3Near(r).Img);
    %%% Center + 3 Surround (20-27)
    for n=1:8
        CurrImg = Surr3Near(r).Img;
        PatchNow = ShapeInfo(ShapeChosen(n)).StimMtx;
        PatchNow = imresize(PatchNow,[StimSize StimSize]);
        NewImg = ApplyPatch(CurrImg, [0 0], PatchNow, FGcolor, 0, 0);
        StimSet((r-1)*54+19+n).Img = uint8(NewImg);
    end
    %%% 6 Surround alone (28)
    StimSet((r-1)*54+28).Img = uint8(Surr6Near(r).Img);
    %%% Center + 6 Surround (Near) (29-36)
    for n=1:8
        CurrImg = Surr6Near(r).Img;
        PatchNow = ShapeInfo(ShapeChosen(n)).StimMtx;
        PatchNow = imresize(PatchNow,[StimSize StimSize]);
        NewImg = ApplyPatch(CurrImg, [0 0], PatchNow, FGcolor, 0, 0);
        StimSet((r-1)*54+28+n).Img = uint8(NewImg);
    end
    %%% 12 Surround alone (37)
    StimSet((r-1)*54+37).Img = uint8(SurrMiddle(r).Img);
    %%% Center + 12 Surround (Middle) (38-45)
    for n=1:8
        CurrImg = SurrMiddle(r).Img;
        PatchNow = ShapeInfo(ShapeChosen(n)).StimMtx;
        PatchNow = imresize(PatchNow,[StimSize StimSize]);
        NewImg = ApplyPatch(CurrImg, [0 0], PatchNow, FGcolor, 0, 0);
        StimSet((r-1)*54+37+n).Img = uint8(NewImg);
    end
    %%% 18 Surround alone (46)
    StimSet((r-1)*54+46).Img = uint8(SurrFar(r).Img);
    %%% Center + 18 Surround (Far) (47-54)
    for n=1:8
        CurrImg = SurrFar(r).Img;
        PatchNow = ShapeInfo(ShapeChosen(n)).StimMtx;
        PatchNow = imresize(PatchNow,[StimSize StimSize]);
        NewImg = ApplyPatch(CurrImg, [0 0], PatchNow, FGcolor, 0, 0);
        StimSet((r-1)*54+46+n).Img = uint8(NewImg);
    end
    
    disp([num2str(r),'th trial was computed']);
end

%% crop images
for r=1:NumRepeat    
    %%% No stim (1): 110x110
    StimSet((r-1)*54+1).Img = uint8(StimSet((r-1)*54+1).Img(166:275,166:275,:));
    %%% Center alone (2-9)
    for n=1:8
        StimSet((r-1)*54+1+n).Img = uint8(StimSet((r-1)*54+1+n).Img(166:275,166:275,:));
    end
    %%% 1 Surround alone (10): 220x220
    StimSet((r-1)*54+10).Img = uint8(StimSet((r-1)*54+10).Img(111:330,111:330,:));
    %%% Center + 1 Surround (11-18)
    for n=1:8
        StimSet((r-1)*54+10+n).Img = uint8(StimSet((r-1)*54+10+n).Img(111:330,111:330,:));
    end
    %%% 3 Surround alone (19): 220x220
    StimSet((r-1)*54+19).Img = uint8(StimSet((r-1)*54+19).Img(111:330,111:330,:));
    %%% Center + 3 Surround (20-27)
    for n=1:8
        StimSet((r-1)*54+19+n).Img = uint8(StimSet((r-1)*54+19+n).Img(111:330,111:330,:));
    end
    %%% 6 Surround alone (28): 220x220
    StimSet((r-1)*54+28).Img = uint8(StimSet((r-1)*54+28).Img(111:330,111:330,:));
    %%% Center + 6 Surround (Near) (29-36)
    for n=1:8
        StimSet((r-1)*54+28+n).Img = uint8(StimSet((r-1)*54+28+n).Img(111:330,111:330,:));
    end
    %%% 12 Surround alone (37): 330x330
    StimSet((r-1)*54+37).Img = uint8(StimSet((r-1)*54+37).Img(56:385,56:385,:));
    %%% Center + 12 Surround (Middle) (38-45)
    for n=1:8
        StimSet((r-1)*54+37+n).Img = uint8(StimSet((r-1)*54+37+n).Img(56:385,56:385,:));
    end
    %%% 18 Surround alone (46): 440x440
    StimSet((r-1)*54+46).Img = uint8(StimSet((r-1)*54+46).Img);
    %%% Center + 18 Surround (Far) (47-54)
    for n=1:8
        StimSet((r-1)*54+46+n).Img = uint8(StimSet((r-1)*54+46+n).Img);
    end
    
    disp([num2str(r),'th trial was cropped']);
end