function [GPM] = GP_train(riverheights,rainfalls,lag)
%GP_TRAIN Summary of this function goes here
%   Detailed explanation goes here

[X,y] = condition_data(riverheights,rainfalls,lag);
GPM.minheight = min(y);

[n,~] = size(y);            % total number of data points;

% parameter starting values for optimisation
wd = ones(lag*2,1); v1 = 1; v0 = 0.01;              % measurement noise
PARAMS0 = [v0;v1;wd];

Aset = 1:n;              % Active set, Currently using full set
Cset = 1:n;              % cross validation set, currently using full set

options = optimoptions('fmincon','SpecifyObjectiveGradient',true,'Display','iter');
objective = @(params)hparamOpt(params,X(Aset,:),y(Aset,:),lag);
[PARAMS,F] = fmincon(objective,PARAMS0,[],[],[],[],eps^(1/2)*ones(2*lag+2,1),1000*ones(2*lag+2,1),[],options);

% compute gram matrix
[Lk,alpha] = compute_gram_matrix(X(Aset,:),y(Aset),PARAMS,lag);

GPM.alpha = alpha;
GPM.Lk = Lk;
GPM.X = X(Aset,:);
GPM.lag = lag;
GPM.LogL = F;
GPM.PARAMS = PARAMS;

% cross validate
[Loss,VLoss] = cross_validate(GPM,X(Cset,:),y(Cset));

GPM.Loss = Loss; 
GPM.VLoss = VLoss;

end

