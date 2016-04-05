

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

plot (data(:,3),y,'bx','MarkerSize',1);
xlabel('buffer size in 100 GB');
ylabel('performance improvement in percentage');

