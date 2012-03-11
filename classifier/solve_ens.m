function Ytest = solve_ens(Xtrain, Ytrain, Xtest)
rtree = RegressionTree.template('MinLeaf', 10)
ens = fitensemble(Xtrain, Ytrain, 'LSBoost', 20, 'tree');
Ytest = predict(ens, Xtest);
end

