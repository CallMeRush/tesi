%ADVANCED CLASSIFICATION SCHEME WITH A POOL SELF-VALIDATING CLASSIFIER.

%Ground truth: X uniformly distributed over [-0.5,0.5]^5
%
%Y=1 if X(1)+X(2)+X(3)+X(4)+X(5)>0
%Y=0 otherwise
%
%
%Generate a training set with N data points
N=200;

Xtrain=rand(N,5)-0.5;
Ytrain=double(sum(Xtrain,2)>0);

%Train the classifiers
CLASSIFIERS=cell(N,1);
CLASSIFIERS_PROPERTIES=zeros(N,4);

for i=1:N
    %swap the first and the i-th point
        xtemp=Xtrain(i,:);
        ytemp=Ytrain(i);
        Xtrain(i,:)=Xtrain(1,:);
        Ytrain(i)=Ytrain(1);
        Xtrain(1,:)=xtemp;
        Ytrain(1)=ytemp;
    %%%%
    
    
    [classifier,kp,kn,Np,Nn]=traingemballs(Xtrain,Ytrain);
    
    CLASSIFIERS{i}=classifier;
    CLASSIFIERS_PROPERTIES(i,1)=kp;
    CLASSIFIERS_PROPERTIES(i,2)=kn;
    CLASSIFIERS_PROPERTIES(i,3)=Np;
    CLASSIFIERS_PROPERTIES(i,4)=Nn;
    
    
end

%Check with fresh simulated data the performance of the the majority classifier:
M=1000;
Xtest=rand(M,5)-0.5;
Ytrue=double(sum(Xtest,2)>0);
Ytest=zeros(M,1);

for i=1:N
Ytest=Ytest+usegemballs(CLASSIFIERS{i},Xtest);
end
Ytest=Ytest/N;
Ymaj=(Ytest>0.5);

FalseNegativeRateOnNewData=length(find( Ytrue==1 & Ymaj==0))/length(find(Ytrue==1))
FalsePositiveRateOnNewData=length(find( Ytrue==0 & Ymaj==1))/length(find(Ytrue==0))
