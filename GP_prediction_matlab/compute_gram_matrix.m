function [Lk,alpha] = compute_gram_matrix(X,y,PARAMS,lag)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here

v0 = PARAMS(1);                 % extracting optimised parameters
v1 = PARAMS(2);
wd = PARAMS(3:end);

[n,n_in] = size(X);

D = nan(n,n,n_in);
for dd = 1:2*lag
    D(:,:,dd) = wd(dd)*bsxfun(@minus,X(:,dd),X(:,dd)').^2;
end
K = v1*exp(-0.5*sum(D,3))+v0*eye(n); % training K
% tic
Lk = chol(K,'lower'); % the lower cholesky decomp of K
alpha = Lk'\(Lk\y);


end

