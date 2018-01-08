function [LogL,g] = hparamOpt(params,x,y,lag)
%HPARAMOPT_BRUTE Summary of this function goes here
%   Detailed explanation goes here

v0 = params(1);
v1 = params(2);
wd = params(3:end);
[n_points,n_in] = size(x);

D = nan(n_points,n_points,n_in);

for dd = 1:n_in
    D(:,:,dd) = wd(dd)*bsxfun(@minus,x(:,dd),x(:,dd)').^2;
end

temp = exp(-0.5*sum(D,3));
K = v1*temp+v0*eye(n_points); % TODO add measurement noise to K
K = 0.5*(K+K'); % numerical fix
try
    [L,npd] = chol(K,'lower');

    count = 0; % more numerical tweaking to make pd
    while(npd)
        K = K + (2+count)*abs(min([eps;eig(K)]))*eye(size(K));
        [L,npd] = chol(K,'lower');
        count = count+1;
        if (count ==20)
            error('cant make pd');
        end
    end
catch
    L = 100;
    
end

LogL = sum(log(diag(L))) + 0.5*y'*(L'\(L\y))+n_points/2*log(2*pi); % the negative log likelihood

% calculate gradients
dKdv0 = eye(n_points);
dKdv1 = temp;
dKdwd = nan(n_points,n_points,lag*2);
for dd = 1:n_in
   dKdwd(:,:,dd) = -0.5*v1*temp.*D(:,:,dd)/wd(dd);
end

g = NaN(size(params));
g(1) = 0.5*trace(L'\(L\dKdv0)) - 0.5*y'*  (L'\(L\(dKdv0*(L'\(L\y)))));
% g(1) = 0.5*trace(K\dKdv0) - 0.5*y'*(K\(dKdv0*(K\y)));
g(2) = 0.5*trace(L'\(L\dKdv1)) - 0.5*y'*  (L'\(L\(dKdv1*(L'\(L\y)))));
for dd = 1:n_in
   g(dd+2) = 0.5*trace(L'\(L\dKdwd(:,:,dd))) - 0.5*y'*  (L'\(L\(dKdwd(:,:,dd)*(L'\(L\y)))));
end


end

