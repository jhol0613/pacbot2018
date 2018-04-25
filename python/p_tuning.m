data = csvread('p_test.csv');
t = linspace(1, 100, length(data));
hold on
for i = 1:4
    plot(t, data(:,i));
end
legend('front left', 'front right', 'rear left', 'rear right')
xlabel('time (arbitrary units)')
ylabel('sensor reading (cm)')
shg