function [ypred,vpred] = GP_predict(GPM,xstar,Sigma_x)
% function [ypred,vpred] = GP_predict(GPM,xstar,Sigma_x)
% inputs:
%   GPM: model structure defined elsewhere
%   xstar: current input point xstar
%   Sigma_x: variances of current input put
% outputs:
%   ypred: predicted next river height
%   vpred: variance of prediction

% extract parameters
lag = GPM.lag;
Lk = GPM.Lk;
alpha = GPM.alpha;
X = GPM.X;
minheight = GPM.minheight;
[n_t,~] = size(xstar);
[n,~] = size(X);                % extracting optimised parameters
v1 = GPM.PARAMS(2);
wd = GPM.PARAMS(3:3+lag*2-1);

nsigp = sum(diag(Sigma_x)>0);       % number of non zero variances
if nsigp
    sigp = NaN(2*nsigp,2*lag);
    ysig = NaN(2*nsigp,1);
    vsig = NaN(2*nsigp,1);
    P = Sigma_x(lag-nsigp+1:lag,lag-nsigp+1:lag);
    [root,~] = chol(nsigp*P);
    rootfull = zeros(nsigp,2*lag);
    rootfull(:,lag-nsigp+1:lag) = root;
    for kk = 1:nsigp
        sigp(kk,:) = xstar + rootfull(kk,:);
        sigp(kk+nsigp,:) = xstar - rootfull(kk,:);
    end
    for ll = 1:2*nsigp
        sigp(ll,1:lag) = max([sigp(ll,1:lag);minheight*ones(1,lag)]);       % enforced rivermin
        Dstar = nan(n_t,n,lag*2);
        for dd = 1:2*lag
            Dstar(:,:,dd) = wd(dd)*bsxfun(@minus,sigp(ll,dd),X(:,dd)').^2;
        end
        Kstar = v1*exp(-0.5*sum(Dstar,3));
        ysig(ll) = Kstar*alpha;
        v = Lk\Kstar';
        vsig(ll) = v1 - v'*v;
        
    end
    ypred = sum(ysig)/(2*nsigp);
    vpred = (sum(vsig) + (ysig-ypred)'*(ysig-ypred))/(2*nsigp);
else
    Dstar = nan(n_t,n,lag*2);
    for dd = 1:2*lag
        Dstar(:,:,dd) = wd(dd)*bsxfun(@minus,xstar(:,dd),X(:,dd)').^2;
    end
    
    Kstar = v1*exp(-0.5*sum(Dstar,3));
    
    % mean prediction
    ypred = Kstar*alpha;
    % variance prediction
    v = Lk\Kstar';
    vpred = v1 - v'*v;
end

end

