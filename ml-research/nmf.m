function [W, H] = nmf(V, k)
%Implement the algorithim described in
% https://papers.nips.cc/paper/1861-algorithms-for-non-negative-matrix-factorization.pdf

[m, n] = size(V);

% Not sure what to init these to for best results
W = rand(m, k);
H = rand(k, n);

% Not really sure when to stop converging either
epsilon = 0.000000001;

cost = norm(V - W * H) ^ 2;
i = 0;
while true
    HNumerMatrix = W' * V;
    HDenomMatrix = W' * W;
    for a = 1:k
        for mu = 1:n
            H(a, mu) = H(a, mu) * (HNumerMatrix(a, mu) / (HDenomMatrix * H)(a, mu));
        end
    end

    WNumerMatrix = V * H';
    WDenomMatrix = H * H';
    for i = 1:m
        for a = 1:k
            W(i, a) = W(i, a) * (WNumerMatrix(i, a) / (W * WDenomMatrix)(i, a));
        end
    end

    costPrime = norm(V - W * H) ^ 2;
    if abs(cost - costPrime) < epsilon
        break;
    end
    cost = costPrime;
end

end
