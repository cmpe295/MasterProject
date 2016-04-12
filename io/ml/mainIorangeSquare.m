

%% Initialization
clear ; close all; clc


%% ======================= lotting the original data=======================
%clean the data first
data = data1 = load('../output/training_data_iorange.txt');

%generate 11 more features, we may not use them all, tune this in the future
data(:,1) = data1(:,1)./100;
data(:,2) = (data1(:,1)./100).^2;
data(:,3) = (data1(:,1)./100).^3;
data(:,4) = (data1(:,1)./100).^4;
data(:,5) = (data1(:,1)./100).^5;
data(:,6) = (data1(:,1)./100).^6;
data(:,7) = (data1(:,1)./100).^7;
data(:,8) = (data1(:,1)./100).^8;
data(:,9) = (data1(:,1)./100).^9;
data(:,10) = (data1(:,1)./100).^10;
data(:,11) = (data1(:,1)./100).^11;
data(:,12) = (data1(:,1)./100).^12;

data(:,3:3) = log(data(:,3:3));



fprintf('Plotting Data ...\n')
X = data(:, 1:6); 
y = data1(:,3);
m = length(y); % number of training examples

% Plot Data
% Note: You have to complete the code in plotData.m
figure; % open a new figure window

plot (data(:,1),y,'rx','MarkerSize',1);
xlabel('io range size in 100 GB');
ylabel('performance improvement in percentage');


% Scale features and set them to zero mean
fprintf('Normalizing Features ...\n');

[X mu sigma] = featureNormalize(X);

% Add intercept term to X
X = [ones(m, 1) X];



fprintf('Running gradient descent ...\n');

% Choose some alpha value
alpha = 0.02;
num_iters = 4000;
% Init Theta and Run Gradient Descent 
theta = zeros(length(X(1,:)), 1);
[theta, J_history] = gradientDescentMulti(X, y, theta, alpha, num_iters);


% Plot the linear fit
hold on; % keep previous plot visible
plot(data(:,1),  X*theta, '-','MarkerSize',1, 'LineWidth', 2)
legend('Training data', 'Linear regression')
hold off % don't overlay any more plots on this figure

% Plot the convergence graph
 figure;
 plot(1:numel(J_history), J_history, '-b', 'LineWidth', 2);
 xlabel('Number of iterations');
 ylabel('Cost J');

% Display gradient descent's result
fprintf('Theta computed from gradient descent: \n');
fprintf(' %f \n', theta);


