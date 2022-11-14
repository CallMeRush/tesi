%BASIC CLASSIFICATION SCHEME WITH A SELF-VALIDATING CLASSIFIER.

%Ground truth: X uniformly distributed over [-0.5,0.5]^5
%
%Y=1 if X(1)+X(2)+X(3)+X(4)+X(5)>0
%Y=0 otherwise
%
%Ground truth is usually unknown. Here it is given for the sake of
%comparing the result of self-testing with the actual misclassification
%rates.
%
%We generate a training set with N data points
N=200;

Xtrain=rand(N,5)-0.5;
Ytrain=double(sum(Xtrain,2)>0);

%Train the classifier
[classifier,kp,kn,Np,Nn]=traingemballs(Xtrain,Ytrain);

%The output values kp,kn,Np,Nn are related to the empirical False Positive 
% and False Negative rates. In fact, leave-one-out errors can be computed as
%follows:
LOOFalseNegative=kp/Np
LOOFalsePositive=kn/Nn
%These are estimates that can be useful in practice. Moreover, based on 
%kp,kn,Np,Nn, RIGOROUS upper-bounds on FalsePositive and FalseNegative 
%rates can be obtained.
%These bounds are the output values of validategemballs and by construction 
%they are valid simultaneusly with confidence 1-2*beta 
%(e.g., confidence 90% when beta=0.05);
beta=0.05;
%%[GuaranteedFalseNegativeRate,GuaranteedFalsePositiveRate]=validategemballs(kp,kn,Np,Nn,beta,beta)

%In this simulation example, we can check with fresh simulated data 
%that the bounds provided by theory were satisfied:

Xtest=rand(10000,5)-0.5;

Ytest=usegemballs(classifier,Xtest);
Ytrue=double(sum(Xtest,2)>0);

FalseNegativeRateOnNewData=length(find( Ytrue==1 & Ytest==0))/length(find(Ytrue==1))
FalsePositiveRateOnNewData=length(find( Ytrue==0 & Ytest==1))/length(find(Ytrue==0))
