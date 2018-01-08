function [Loss,VLoss] = cross_validate(GP,X_cross,y_cross)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here


X = GP.X;
alpha = GP.alpha;
PARAMS = GP.PARAMS;
lag = GP.lag;
Lk = GP.Lk;

v1 = PARAMS(2);
wd = PARAMS(3:3+lag*2-1);


% initial loss on cross_valication set
[Nc,~] = size(X_cross);
[N,~] = size(X);

Dstar = nan(Nc,N,lag*2);
for dd = 1:2*lag
    Dstar(:,:,dd) = wd(dd)*bsxfun(@minus,X_cross(:,dd),X(:,dd)').^2;
end
Kstar = v1*exp(-0.5*sum(Dstar,3));
ypred = Kstar*alpha;

v = Lk\Kstar';
V = v1*eye(Nc,Nc) - v'*v;

Loss = norm(y_cross-ypred);
VLoss = norm(diag(V));

end

