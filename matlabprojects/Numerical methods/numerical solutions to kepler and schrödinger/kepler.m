% Initialvärden
a=0.5;
y0=[(1-a),0,0,sqrt((1+a)/(1-a))]';
step= 5e-4;
endtime=100;
nstep=round(endtime/step);
time=linspace(0, endtime, nstep + 1);

% Omskrivning till första ordningens system 
function y = derive(t,x)
    x1new=x(3,1);
    x2new=x(4,1);
    x3=-x(1,1)/((x(1,1)^2+x(2,1)^2)^(3/2));
    x4=-x(2,1)/((x(1,1)^2+x(2,1)^2)^(3/2));
    y=[x1new,x2new,x3,x4]';
end

% Hamiltonianen
function H = hamiltonian(x)
    H=0.5*(sqrt(x(3,1)^2+x(4,1)^2))^2 - 1/(sqrt(x(1,1)^2+x(2,1)^2));
end

% Euler framåt
function [pos1, pos2, H, time] = eulerForward(y0, step, endtime)

nstep=round(endtime/step);

pos1=zeros(1, nstep + 1);
pos2=zeros(1, nstep + 1);
H=zeros(1, nstep + 1);

y=y0;
t=0;

pos1(1)=y(1);
pos2(1)=y(2);
time=linspace(0, endtime, nstep + 1);
H(1)=hamiltonian(y);

for ii=1:nstep
    t=t+step;
    dy=derive(t,y);
    y=y+step*dy;
    pos1(ii+1)=y(1);
    pos2(ii+1)=y(2);
    H(ii+1)=hamiltonian(y);
end
end

% Symplektisk Euler
function [pos1, pos2, H, time] = eulerSymplectic(y0, step, endtime)

nstep=round(endtime/step);

pos1=zeros(1, nstep + 1);
pos2=zeros(1, nstep + 1);
H=zeros(1, nstep + 1);

y=y0;
t=0;

pos1(1)=y(1);
pos2(1)=y(2);
time=linspace(0, endtime, nstep + 1);
H(1)=hamiltonian(y);
for ii=1:nstep
    t=t+step;
    p1next=y(3,1)-step*(y(1,1)/((y(1,1)^2+y(2,1)^2)^(3/2)));
    p2next=y(4,1)-step*(y(2,1)/((y(1,1)^2+y(2,1)^2)^(3/2)));
    q1next=y(1,1)+step*(p1next);
    q2next=y(2,1)+step*(p2next);
    y=[q1next,q2next,p1next,p2next]';
    pos1(ii+1)=y(1);
    pos2(ii+1)=y(2);
    H(ii+1)=hamiltonian(y);
end
end

% Jacobianen för Newtons metod 
function J = Jacobian(f, x, h, metod)
    f0 = f(0,x);
    dfdx = zeros(4,4);
    eps = 1e-8;
    for i = 1:4
        x_temp = x;
        x_temp(i) = x_temp(i) + eps;
        dfdx(:,i) = (f(0, x_temp) - f0) / eps;
    end
    if strcmp(metod, 'euler bakåt') 
            J = eye(4) - h * dfdx; 
    elseif strcmp(metod, 'mittpunktsmetoden') 
            J = eye(4) - (h/2) * dfdx; 
    end
end

% Euler bakåt
function [pos1, pos2, H, time] = eulerBackward(y0, step, endtime)
nstep=round(endtime/step);

pos1=zeros(1, nstep + 1);
pos2=zeros(1, nstep + 1);
H=zeros(1, nstep + 1);

y=y0;
t=0;

pos1(1)=y(1);
pos2(1)=y(2);
time=linspace(0, endtime, nstep + 1);
H(1)=hamiltonian(y);
for ii=1:nstep
    y_prev = y;
    x = y_prev; %Initialgissning för Newtons metod
    t = t + step;
    for iter = 1:10
        F = x - y_prev - step*derive(1,x);
        J = Jacobian(@derive, x, step, 'euler bakåt');
        delta = J \ F;
        x = x - delta;
        if norm(delta) < 1e-10, break;
        end
    end
    y = x;
    pos1(ii+1)=y(1);
    pos2(ii+1)=y(2);
    H(ii+1)=hamiltonian(y);
end
end

% Mittpunktsmetoden
function [pos1, pos2, H, time] = midpoint(y0, step, endtime)
nstep=round(endtime/step);

pos1=zeros(1, nstep + 1);
pos2=zeros(1, nstep + 1);
H=zeros(1, nstep + 1);

y=y0;
t=0;

pos1(1)=y(1);
pos2(1)=y(2);
time=linspace(0, endtime, nstep + 1);
H(1)=hamiltonian(y);
for ii=1:nstep
    y_prev = y;
    x = y_prev; %Initialgissning för Newtons metod
    t = t + step;
    for iter = 1:10
        F = x - y_prev - step*derive(1,(y_prev + x) / 2);
        J = Jacobian(@derive, (y + x) / 2, step, 'mittpunktsmetoden');
        delta = J \ F;
        x = x - delta;
        if norm(delta) < 1e-10, break;
        end
    end
    y = x;
    pos1(ii+1)=y(1);
    pos2(ii+1)=y(2);
    H(ii+1)=hamiltonian(y);
end
end

[pos1, pos2, H1] = eulerForward(y0, step, endtime);
[pos3, pos4, H2] = eulerSymplectic(y0, step, endtime);
[pos5, pos6, H3] = eulerBackward(y0, step, endtime);
[pos7, pos8, H4] = midpoint(y0, step, endtime);

% Uppgift 1 d)
%hold on;
%plot(pos1, pos2, 'red') %Euler framåt
%plot(pos3, pos4, 'blue') %Symplektisk Euler
%plot(pos5, pos6, 'green') %Euler bakåt
%plot(pos7, pos8, 'black') %Mittpunktsmetoden

% Uppgift 1 e)
%hold on; 
%plot(time, H1, 'red') %Euler framåt
%plot(time, H2, 'blue') %Symplektisk Euler
%plot(time, H3, 'green') %Euler bakåt
%plot(time, H4, 'black') %Mittpunktsmetoden

% Uppgift 3
step= 5e-4;
endtime=500;
nstep=round(endtime/step);
time=linspace(0, endtime, nstep + 1);

function [pos1, pos2, H, time] = ode45Method(y0, step, endtime)
nstep=round(endtime/step);

pos1=zeros(1, nstep + 1);
pos2=zeros(1, nstep + 1);
H=zeros(1, nstep + 1);

y=y0;
t=0;

pos1(1)=y(1);
pos2(1)=y(2);
time=linspace(0, endtime, nstep + 1);
H(1)=hamiltonian(y);

opt = odeset('RelTol',1e-10,'AbsTol',1e-10);
[t, y] = ode45(@derive, time, y0, opt);
pos1=y(:, 1); 
pos2=y(:, 2);
H=hamiltonian(y);
end

H0 = hamiltonian(y0);
steps = [5e-1, 5e-2, 5e-3, 5e-4];

err_vec_symp = zeros(size(steps));
err_vec_mid  = zeros(size(steps));
H_err_vec_symp = zeros(size(steps));
H_err_vec_mid  = zeros(size(steps));

for ii=1:length(steps)
    step=steps(ii);

    [pos3, pos4, H2] = eulerSymplectic(y0, step, endtime);
    [pos7, pos8, H4] = midpoint(y0, step, endtime);
    [pos9, pos10, H5] = ode45Method(y0, step, endtime);

    err_symp = sqrt((pos3(end)-pos9(end))^2 + (pos4(end)-pos10(end))^2);
    err_mid  = sqrt((pos7(end)-pos9(end))^2 + (pos8(end)-pos10(end))^2);

    H_err_symp = abs(H2(end) - H0);
    H_err_mid  = abs(H4(end) - H0);
    H_err_ode  = abs(H5(end) - H0);

    err_vec_symp(ii) = err_symp;
    err_vec_mid(ii)  = err_mid;
    H_err_vec_symp(ii) = H_err_symp;
    H_err_vec_mid(ii)  = H_err_mid;

    fprintf('\n--- Steglängd: %e ---\n', step);
    fprintf('Symplektisk Euler: [%.6f, %.6f] | Globalt fel: %.2e | Energiförlust: %.2e\n', ...
        pos3(end), pos4(end), err_symp, H_err_symp);
    fprintf('Mittpunktsmetod:   [%.6f, %.6f] | Globalt fel: %.2e | Energiförlust: %.2e\n', ...
        pos7(end), pos8(end), err_mid, H_err_mid);
    fprintf('ode45 (Referens):  [%.6f, %.6f]\n', ...
        pos9(end), pos10(end));
end

% Figur 1: Globalt positionsfel (Log-Log plot för noggrannhetsordning)
figure;
loglog(steps, err_vec_symp, '-o', steps, err_vec_mid, '-s');
xlabel('Steglängd (h)'); ylabel('Globalt positionsfel');
legend('Symplektisk Euler (Ordning 1)', 'Mittpunktsmetod (Ordning 2)');

% Figur 2: Energifel (Hamiltonian)
figure;
loglog(steps, H_err_vec_symp, '-o', steps, H_err_vec_mid, '-s');
xlabel('Steglängd (h)'); ylabel('Absolut energifel |H_{slut} - H_0|');
legend('Symplektisk Euler', 'Mittpunktsmetod');