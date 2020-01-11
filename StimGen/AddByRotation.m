%%% AddByRotation
%%% call ApplyPatch function to put Patch along the circle boundary

function updateImg = AddByRotation(CurrImg,ISD,StimSize,RotOffset,NumSurrHere,FGcolor,XY_jitter,C_jitter,ShapeInfo,ShapeChosen)

for n=1:NumSurrHere
    RotNow = (n-1)*360/NumSurrHere + RotOffset;
    RotPI = RotNow*pi/180;
    xShift = cos(RotPI)*ISD - sin(RotPI)*0;
    yShift = sin(RotPI)*ISD + cos(RotPI)*0;
    xyShift = [xShift yShift];
    if ~isempty(ShapeChosen)
       ShapeNow = ShapeChosen(randperm(length(ShapeChosen),1));
    else
       ShapeNow = 2;
    end
    PatchNow = ShapeInfo(ShapeNow).StimMtx;
    PatchNow = imresize(PatchNow,[StimSize StimSize]);
    NewImg = ApplyPatch(CurrImg, xyShift, PatchNow, FGcolor, XY_jitter, C_jitter);
    CurrImg = NewImg;
end
updateImg = CurrImg;
