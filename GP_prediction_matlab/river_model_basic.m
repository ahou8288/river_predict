function [xnext] = river_model_basic(x,rainfall,params)
%RIVER_MODEL_BASIC Summary of this function goes here
%   Detailed explanation goes here

C1 = params.C1;
R1 = params.R1;
C2 = params.C2;
R2 = params.R2;
T = params.T;

xnext = NaN(4,1);
xnext(1) = x(1) + T*(rainfall(1)*0.1 + rainfall(2)*0.2 + rainfall(3)*0.7 - x(1)/C1/R1); % catchment
xnext(2) = max(x(2) + T*(x(1)/C1/R1 - max((x(2)-0.1),0)/C2/R2),0.1) ; % river height
xnext(3) = x(1)/C1/R1; % flow from catchment
xnext(4) = max((x(2)-0.1),0)/C2/R2; % flow from river


end

