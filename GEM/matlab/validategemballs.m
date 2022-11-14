% VALIDATEGEMBALLS computes upper bounds on the type I and type II errors of gemballs, 
% by using its self-validating properties (Theorem 2.1, <a href="matlab:web('https://doi.org/10.1109/LCSYS.2018.2840427')":>[1]</a>)
% 
% [errp,errn] = validategemballs(kp,kn,Np,Nn,betan,betap)
%
% Np,Nn,kp,kn - Output of  <a href="matlab:eval('help traingemballs')">traingemballs</a>. See  <a href="matlab:eval('help traingemballs')">traingemballs</a>
%               for definitions. 
% betap, betan - confidence parameters (real numbers in (0,1)).
%                NOTE: small values imply high confidence
%
% Short explanation:
%  Let  
%  - pp be the probability that a (new) POSITIVE point is misclassified;
%  - pn be the probability that a (new) NEGATIVE point is misclassified;
%  then, it holds that:
%  pp<=errp holds true with confidence 1-betap
%  pn<=errn holds true with confidence 1-betan
%  (pp<=errp and pn<=errn hold true simultaneusly with confidence
%   1-betap-betan)
%
% For a complete explanation see  
% [1]: <a href="matlab:web('https://doi.org/10.1109/LCSYS.2018.2840427')">"A New Classification Algorithm With Guaranteed Sensitivity and Specificity for Medical Applications"</a>,
% by A. Carè, F.A. Ramponi, M.C. Campi.  IEEE Control Systems Letters, vol. 2, no. 3, pp. 393-398, July 2018.
%
%
% Authors: Algo Carè, Federico Alessandro Ramponi
% Date: 30/06/18

function [errp,errn] = validategemballs(kp,kn,Np,Nn,betap,betan)


if kp<0 || kp>Np+1 || kn<0 || kn>Nn+1
    error('wrong input values')
end
    
if kp==0
    errp=0;
elseif kp==Np+1
    errp=1;
else
    errp=betainv(1-betap/Np,kp,Np-kp+1);
end

if kn==0
    errn=0;
elseif kn==Nn+1
    errn=1;
else
    errn=betainv(1-betan/Nn,kn,Nn-kn+1);
end
