%%% ApplyPatch
%%% shape in a patch is added to the image matrix
%%% required input: CurrImg, [xShift yShift], PatchNow, FGcolor, XY_jitter, C_jitter
%%% output: NewImg

function NewImg = ApplyPatch(CurrImg, xyShift, PatchNow, FGcolor, XY_jitter, C_jitter);

xShift = xyShift(1);
yShift = xyShift(2);

if XY_jitter==1
   Xjitter = (randperm(3,1)-2)*size(PatchNow,2)/10;
   Yjitter = (randperm(3,1)-2)*size(PatchNow,1)/10;
%    Xjitter = (randperm(3,1)-2)*size(PatchNow,2)/6;
%    Yjitter = (randperm(3,1)-2)*size(PatchNow,1)/6;   
else
   Xjitter = 0;   Yjitter = 0;
end


PatchX1 = round(size(CurrImg,2)/2 + xShift + Xjitter - size(PatchNow,2)/2);
PatchX2 = PatchX1+size(PatchNow,2)-1;
PatchY1 = round(size(CurrImg,1)/2 - yShift - Yjitter - size(PatchNow,1)/2);
PatchY2 = PatchY1+size(PatchNow,1)-1;

CropImg = CurrImg(PatchY1:PatchY2,PatchX1:PatchX2,:);
FGpart = find(PatchNow(:)<0.5);

for c=1:3 %%% color
    pNow = CropImg(:,:,c);
    if C_jitter == 1
        if c==1
           %Cjitter = (randperm(3,1)-1)*0.3+0.7;
           Cjitter = (randperm(3,1)-1)*0.15+0.6;           
        end
    else
        Cjitter = 1;
    end
    pNow(FGpart) = FGcolor(c)*Cjitter;
    CropImg(:,:,c) = pNow;
end
CurrImg(PatchY1:PatchY2,PatchX1:PatchX2,:) = CropImg;
NewImg = CurrImg;
