clf
data = csvread('p_test.csv');
%data = data(1:20, :);
t = linspace(1, 100, length(data));
hold on
subplot(2, 1, 1)
plot(t, data(:,1), t, data(:,2), t, data(:,3), t, data(:,4), ...
    t, 7*ones(1, length(t)), '--' );

legend('front left', 'front right', 'rear left', 'rear right');
xlabel('time (arbitrary units)');
ylabel('sensor reading (cm)');

subplot(2, 1, 2);
plot(t, data(:,5), t, zeros(1, length(t)), '--');

shg