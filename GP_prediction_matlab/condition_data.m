function [X,y] = condition_data(riverheights,rainfalls,lag)
%CONDITION_DATA Summary of this function goes here
%   Detailed explanation goes here

[~,n_heights] = size(riverheights); 
y = nan(n_heights-lag,1);
X = nan(n_heights-lag,lag*2);
for k = lag+1:n_heights
    y(k-lag) = riverheights(k);
    X(k-lag,:) = [riverheights(k-lag:k-1) rainfalls(k-lag:k-1)'];
end


end

