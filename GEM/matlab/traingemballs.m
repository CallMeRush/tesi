% TRAINGEMBALLS generates a simple self-validating GEM classifier with 
% a given balance between false-positive and false-negative error rates.
%
%
% [classifier,kp,kn,Np,Nn] = traingemballs(X,Y,cp,cn)
% 
% • X is a n x d vector, where
%   n is the number of training points 
%     (the first one is used as initial
%      point in constructing the classifier)
%   d is the number of features
%
% • Y is a column vector containing 0 or 1 labels
% • cp, cn are natural numbers (default cp=1, cn=1).
%
% DEFINITIONS:
% • (X(1,:),Y(1)) is a special point that we call "STARTING POINT".
% • We call "EFFECTIVE TRAINING SET" the training set without the STARTING POINT.  
% • We call "POSITIVE points" the points with label 1.
% • We call "NEGATIVE points" the points with label 0.
%
% OUTPUT:
% • 'classifier' is the classifier. See <a href="matlab:eval('help
% usemballs')":>usegemballs</a> for how to use it.
% • 'Np' is the number of the positive points in the effective training set.
% • 'Nn' is the number of negative points in the effective training set. 
% • 'kp' is the number of positive points in the effective training set that
%   are misclassified in leave-one-out cross-validation.
% • 'kn' is the number of negative points points in the effective training set that
%   are misclassified in leave-one-out cross-validation.
%
% INTERPRETATION:
% • kp/Np is a leave-one-out estimate of the false-positive rate.
% • kn/Nn is a leave-one-out estimate of the false-negative rate. 
% 
% The user-chosen parameters cn and cp affect the (data-dependent) kn:kp ratio
% so that kn/kp is expected to approximate cn/cp.
% Therefore, cp and cn tune the balance between false-positive and the false-negative error rates. 
%
% An accurate upper-bound on the false-positive and the false-negative
% ratio is provided by <a href="matlab:eval('help validategemballs')":>validategemballs</a>
%
%
% The rigorous theoretical justification for the upper-bounds can be found 
% in 
% [1]: <a href="matlab:web('https://doi.org/10.1109/LCSYS.2018.2840427')">"A New Classification Algorithm With Guaranteed Sensitivity and Specificity for Medical Applications"</a>,
% by A. Carè, F.A. Ramponi, M.C. Campi.  IEEE Control Systems Letters, vol. 2, no. 3, pp. 393-398, July 2018.
%
%
%
% Authors: Algo Carè, Federico Alessandro Ramponi
% Date: 30/06/18

function [classifier,kp,kn,Np,Nn] = traingemballs(X,Y,cp,cn)
if nargin==2
       cp=1;
       cn=1;
end
Y=double(Y);
LAB1=1;
LAB2=0;
LAB=[LAB1;LAB2];

LAB1pos=find(Y==LAB1);
LAB2pos=find(Y==LAB2);

if ~isequal(sort([LAB2pos;LAB1pos],'ascend'),[1:length(Y)]');
    error(['the training must contain ', num2str(LAB2),'- or ',num2str(LAB1),'-labelled points only'])
end

Np=length(LAB1pos)-(Y(1)==LAB1);
Nn=length(LAB2pos)-(Y(1)==LAB2);

%%% useful redefinitions and data structures
Y(LAB1pos)=1;
Y(LAB2pos)=2;
c1=cp; c2=cn;
c=[c1;c2];
S1=[]; S2=[];

S={S1;S2};

classifier=[];
complete=0;

 xc=X(1,:);
 yc=Y(1);
 
 R=X(2:end,:);
 L=Y(2:end);

 
while (complete==0)
 oppositelabel=mod(yc,2)+1; %(currentlabel == yc)
 [distances,ind]=sort(sqrt(sum( (ones(size(R,1),1)*xc-R).^2 ,2)) ,'ascend');

 R=R(ind,:);
 L=L(ind);

 OppositePos=find(L==oppositelabel);
 SuppPos=OppositePos(1:min(c(oppositelabel),length(OppositePos)));

 Supp=S{oppositelabel};

 if c(oppositelabel)>length(OppositePos)
    
    complete=1;
    
    classifier=[classifier; [xc,Inf,LAB(yc)]]; 
    Supp=[Supp;R(SuppPos,:);Inf(1,size(X,2))]; %When an y-valued ball has infinite radius, it has a (1-y)-valued "support point" at Inf.

 else
    classifier=[classifier; [xc,distances(SuppPos(end)),LAB(yc)]];
    Supp=[Supp;R(SuppPos,:)];
    
    xc=R(SuppPos(end),:);
    yc=L(SuppPos(end));
    
    R=R(SuppPos(end)+1:end,:);
    L=L(SuppPos(end)+1:end);
 end
 
S{oppositelabel}=Supp;
end

kp=size(S{1},1); 
kn=size(S{2},1);



