params.C1 = 5;
params.R1 = 1;
params.C2 = 2;
params.R2 = 1;
params.T = 1;

N = 2000;

rainchance1 = rand(N,1)>0.95;
rainchance2 = [0;rainchance1(1:end-1)] .* (rand(N,1)>0.4);
rainchance3 = [0;rainchance2(1:end-1)] .* (rand(N,1)>0.7);
rainfalls = (rainchance1+rainchance2+rainchance3) .* 5.*abs(randn(N,1));
rainfalls(1:3) = zeros(3,1);

% simualate
x = NaN(4,N+1);
x(:,1) = [0;0.2;0;0];
x(:,2) = [0;0.2;0;0];
x(:,3) = [0;0.2;0;0];

for k = 3:N  
    x(:,k+1) = river_model_basic(x(:,k),rainfalls([k;k-1;k-2]),params);
     
end

figure(1)
clf
subplot 211
plot(rainfalls)
title('rainfall')
subplot 212
plot(x(2,:))
title('river level')

figure(2)
plot(rainchance1+rainchance2+rainchance3)

%% save data
% riverheight = x(2,:);
% save('sim_data2000','rainfalls','riverheight')