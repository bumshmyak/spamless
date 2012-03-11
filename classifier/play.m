clear;

load('../data/prepared_train.txt');
Xtrain = prepared_train(:, 2:end);
Ytrain = prepared_train(:, 1);
load('../data/prepared_control.txt')

Ypred = solve_ens(Xtrain, Ytrain, prepared_control);
Ypred = (Ypred + abs(min(Ypred))) / (max(Ypred) - min(Ypred)); 
dlmwrite('../data/results/res2.txt', horzcat((0:size(Ypred, 1) - 1)', Ypred),...
    'delimiter', ',', 'precision', 10)
