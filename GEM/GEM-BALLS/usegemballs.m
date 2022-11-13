% USEGEMBALLS uses a classifier built by <a href="matlab:eval('help traingemballs')">traingemballs</a> to classify new data X
% 
% usage:
% Y = usegemballs(classifier,X)
%
%
% X is a n x d input vector, where
%  n is the number of test points
%  d is the number of features;
%
% Y is the n x 1 vector of output labels.
%
% For more information, see
% <a href="matlab:web('https://doi.org/10.1109/LCSYS.2018.2840427')">"A New Classification Algorithm With Guaranteed Sensitivity and Specificity for Medical Applications"</a>,
% by A. Carè, F.A. Ramponi, M.C. Campi.  IEEE Control Systems Letters, vol. 2, no. 3, pp. 393-398, July 2018.
%
% See also traingemballs, validategemballs
%
% Authors: Algo Carè, Federico Alessandro Ramponi
% Date: 30/06/18

function Y = usegemballs(classifier,X)
n = size(X,1);
d = size(X,2);
Y = zeros(n,1);

for i = 1:n
   
    found = 0;
    j = 1;
    while found==0
       if norm(classifier(j,1:d)-X(i,:),2) < classifier(j,d+1)
          found=1;
          Y(i) = classifier(j,d+2);
       else
           j = j+1;
       end     
    end
     
end
