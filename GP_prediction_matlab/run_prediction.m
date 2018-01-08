% put data into the form required
% Script for demonstrating the prediction on simulated data

load('sim_data1000');
% load('GP_model_lag9');
load('GPM_2000_lag10');

% define starting params params
lag = GPM.lag;                % feedback lag


[x,y] = condition_data(riverheight,rainfalls,lag);


%% predicting
kstart = 400;           % choose timestep at which to predict forward from
npred = 100;             % number of points to predict forward

x_start = x(kstart,:);

ypred = nan(npred,1);
vpred = nan(npred,1);

xstar = x_start;
Sigma_x = zeros(2*lag);

for i = 1:npred

    [ypred(i),vpred(i)] = GP_predict(GPM,xstar,Sigma_x); % predict next height

    % prepare for next iteration
    xstar = [xstar(2:lag) ypred(i) x(kstart+i,lag+1:lag*2)];
    Sigma_x(1:lag-1,1:lag-1) = Sigma_x(2:lag,2:lag); 
    Sigma_x(lag,lag) = vpred(i);
    i
end



%% compare
figure(1)
subplot 211
plot((kstart+lag:kstart+npred+lag-1),y(kstart:kstart+npred-1))   % the NaN padding is because teh y value is for k+1 prediction
hold on
% plot((kstart+lag:kstart+npred+lag-1),ypred,'o')
errorbar((kstart+lag:kstart+npred+lag-1),ypred,sqrt(vpred),'o') % 1e6 factor is included as the variance is too small to see atm
hold off
ylim([0 max(ypred)*1.3])
legend('simulated true','predicted')
ylabel('River height')
xlabel('Interval')
subplot 212
plot((kstart+lag-1:kstart+npred+lag-2),x(kstart:kstart+npred-1,lag*2))
xlabel('interval')
ylabel('rainfall')

% figure(2)
% plot(vpred)

