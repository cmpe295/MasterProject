

clear ; close all; clc

fprintf('Loading data ...\n');

%% Load Data and tune it
data = data1 = load('../output/training_data_bufsize_iorange.txt');
data(:,1) = data1(:,1)./100;
data(:,2) = (data1(:,1)./100).^2;
data(:,3) = (data1(:,2)./100);

data(:,4) = 69.783 ./ data1(:,3);
X = data(:, 1:3);
y = data(:, 4);
m = length(y);

figure; % open a new figure window

plot (data(:,1),y,'rx','MarkerSize',1);
xlabel('buffer size in 100 GB');
ylabel('performance improvement in percentage');

% Scale features and set them to zero mean
fprintf('Normalizing Features ...\n');

[X mu sigma] = featureNormalize(X);

% Add intercept term to X
X = [ones(m, 1) X];



fprintf('Running gradient descent ...\n');

% Choose some alpha value
alpha = 0.01;
num_iters = 4000;

% Init Theta and Run Gradient Descent 
theta = zeros(4, 1);
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

