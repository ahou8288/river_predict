%% Train


load('sim_data2000');

% [GPM] = GP_train(riverheight,rainfalls,3);


% lags = 2:15;
% LogLs = NaN(size(lags));
% Losses = NaN(size(lags));
% VLosses = NaN(size(lags));
% for i = 1:length(lags)
%     [GPM] = GP_train(riverheight,rainfalls,lags(i));
%     LogLs(i) = GPM.LogL;
%     Losses(i) = GPM.Loss;
%     VLosses(i) = GPM.VLoss;
%     
%     figure(1)
%     clf
%     subplot 311
%     plot(lags,LogLs,'o-')
%     subplot 312
%     plot(lags,Losses,'o-')
%     subplot 313
%     plot(lags,VLosses,'o-')
%     drawnow
% end


%% retraining with the lag that seemed to work best
lag = 10;
[GPM] = GP_train(riverheight,rainfalls,lag);
