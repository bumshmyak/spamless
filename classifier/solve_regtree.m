function Ytest = solve_regtree(Xtrain, Ytrain, Xtest)
rtree = RegressionTree.fit(Xtrain, Ytrain, 'MinLeaf', 10);
Ytest = predict(rtree, Xtest);
end

