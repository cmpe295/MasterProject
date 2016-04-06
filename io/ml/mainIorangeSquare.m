

%% Initialization
clear ; close all; clc


%% ======================= lotting the original data=======================
%clean the data first
data = data1 = load('../output/training_data_iorange.txt');
data(:,1) = data1(:,1)./100;
data(:,2) = (data1(:,1)./100).^2;
data(:,3) = (data1(:,1)./100).^3;
data(:,4) = (data1(:,1)./100).^4;
data(:,5) = (data1(:,1)./100).^5;

data(:,6) = 69.783 ./ data1(:,3);

fprintf('Plotting Data ...\n')
X = data(:, 1:5); 
y = data(:, 6);
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
alpha = 0.002;
num_iters = 4000;

% Init Theta and Run Gradient Descent 
theta = zeros(6, 1);
[theta, J_history] = gradientDescentMulti(X, y, theta, alpha, num_iters);


% Plot the linear fit
hold on; % keep previous plot visible
plot(data(:,1),  X*theta, '-','MarkerSize',1)
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


