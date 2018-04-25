clf
data = csvread('p_test.csv');
%data = data(1:20, :);
t = linspace(1, 100, length(data));
hold on
for i = 1:5
    plot(t, data(:,i));
end
plot(t, 7*ones(1, length(t)), '--');
plot(t, zeros(1, length(t)), '--');
legend('front left', 'front right', 'rear left', 'rear right', ...
    'correction factor')
xlabel('time (arbitrary units)')
ylabel('sensor reading (cm)')
shg