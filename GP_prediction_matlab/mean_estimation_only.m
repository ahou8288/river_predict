% put data into the form required


load('sim_data1000');

% define starting params params
lag = 10;                % feedback lag
wd = ones(lag*2,1);     % weighting params
v1 = 1;                 % prior variance
v0 = 0.01;              % measurement noise


[~,n_heights] = size(riverheight); 
y = nan(n_heights-lag,1);
x = nan(n_heights-lag,lag*2);
for k = lag+1:n_heights
    y(k-lag) = riverheight(k);
    x(k-lag,:) = [riverheight(k-lag:k-1) rainfalls(k-lag:k-1)'];
end

% consider reordering points based on measurement values

%% Train



% options = optimoptions('fmincon','SpecifyObjectiveGradient',false,'Display','iter');
% objective = @(params)hparamOpt(params,x,y,lag);
% PARAMS = fmincon(objective,[v0;v1;wd],[],[],[],[],eps*ones(2*lag+2,1),1000*ones(2*lag+2,1),[],options);

% objective = @(params)hparamOpt_brute(params,x,y,lag);
% options = optimoptions('fmincon','Algorithm','active-set','SpecifyObjectiveGradient',false);
% objective = @(params)hparamOpt(params,x,y,lag);
% options = optimoptions('fmincon','Algorithm','active-set','SpecifyObjectiveGradient',true,'CheckGradients',false);
% problem = createOptimProblem('fmincon','objective',objective,'x0',[v0;v1;wd],'lb',eps*ones(2*lag+2,1),'ub',1000*ones(2*lag+2,1),'options',options);
% gs = GlobalSearch;
% gs.NumTrialPoints = 200;
% gs.NumStageOnePoints = 20;
% gs.FunctionTolerance = 1e-6;
% gs.Display = 'iter';
% gs.MaxTime = 1200;
% warning('off','all')
% [PARAMS,f] = run(gs,problem);
% warning('on','all')


% save params
% save('params10','PARAMS','lag')

%% form training K
load('params10')

v0 = PARAMS(1);      % extracting optimised parameters
v1 = PARAMS(2);
wd = PARAMS(3:3+lag*2-1);
n_points = length(y);

D = nan(n_points,n_points,lag*2);
for dd = 1:2*lag
    D(:,:,dd) = wd(dd)*bsxfun(@minus,x(:,dd),x(:,dd)').^2;
end
K = v1*exp(-0.5*sum(D,3))+v0*eye(n_points); % training K
% tic
Lk = chol(K,'lower'); % the lower cholesky decomp of K
alpha = Lk'\(Lk\y);
% plotting K
% figure(2)
% mesh(K) % this is interesting as it shows we have a large amount of replicated data


%% predicting
kstart = 500;           % choose timestep at which to predict forward from
npred = 100;             % number of points to predict forward

x_start = x(kstart,:);

ypred = nan(npred,1);
vpred = nan(npred,1);

xstar = x_start;


for i = 1:npred
    Dstar = nan(1,n_points,lag*2);
    for dd = 1:2*lag
        Dstar(:,:,dd) = wd(dd)*bsxfun(@minus,xstar(:,dd),x(:,dd)').^2;
    end
    
   
    Kstar = v1*exp(-0.5*sum(Dstar,3));
    
    % mean prediction
    ypred(i) = Kstar*alpha;
    
    % variance prediction
    v = Lk\Kstar';
%     vpred(i) = Kprior - Kstar*(K\Kstar');      
    vpred(i) = v1 - v'*v;
    xstar = [xstar(2:lag) ypred(i) x(kstart+i,lag+1:lag*2)];

end
% toc
% vpred = max(eps,vpred); % because i calculated this the shit way


%% compare
figure(3)
subplot 211
plot((kstart+lag:kstart+npred+lag-1),y(kstart:kstart+npred-1))   % the NaN padding is because teh y value is for k+1 prediction
hold on
% plot((kstart+lag:kstart+npred+lag-1),ypred,'o')
errorbar((kstart+lag:kstart+npred+lag-1),ypred,sqrt(vpred)*1e5,'o') % 1e6 factor is included as the variance is too small to see atm
hold off
legend('simulated true','predicted')
ylabel('River height')
xlabel('Interval')
subplot 212
plot((kstart+lag-1:kstart+npred+lag-2),x(kstart:kstart+npred-1,lag*2))
xlabel('interval')
ylabel('rainfall')

% figure(4)
% subplot 211
% plot(riverheight)
% subplot 212
% plot(rainfalls)
