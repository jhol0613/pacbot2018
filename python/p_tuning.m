data = csvread('p_test.csv');
t = linspace(1, 100, length(data));
plot(t, data(:,1), data(:,2), data(:,3), data(:,4))
legend('front left', 'front right', 'rear left', 'rear right')
xlabel('time (arbitrary units)')
ylabel('sensor reading (cm)')