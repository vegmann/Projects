
%hamiltonianen helt enkelt
function H= hamilt(u,N,c)
A=derivex(N-2);
H=(norm(u(N+1:2*N,1))^2)/2-c^2*dot(A*u(1:N,1),u(1:N,1))/2;
end


%skapar matrisen som ger andraderivatan
function A = derivex(N)
h=1/(N);
d=linspace(-2/h^2,-2/h^2,N+2);
v=linspace(1/h^2,1/h^2,N+1);
A=zeros(N+2)+diag(d)+diag(v,1)+diag(v,-1);
A(1,2)=2/h^2;
A(N+2,N+1)=2/h^2;
end
%givet u och N spottar ut du
function dudt2 = derivet(u,N,c)
    A=derivex(N);
    u1=u(N+3:2*(N)+2,1)';
    u2=(c^2*A*u(1:N+2,1))';
    dudt2=[u1,u2]';
end


%skapar startvektorn
function u = uvector(g,dg,N)
    step=1/N;
    h=1/(N);
    u=[g(0)];
    du=[0];
    steps=0;
    for ii=1:N-2
        u=[u,g(step)];
        %du=[du,dg(step)];
        du=[du,0];
        step=step+h;
        steps=[steps,step];
    end 
  
    u=[u,0];
    du=[du,0];
    u=[u,du]';
    
end

%startvärden
c=1;
g=@(x) (exp(-200*(x-0.5)^2));
dg=@(x) (-(400*x-200)*exp(-200*(x-0.5)^2));
N=50;
x=(((1:N+1)-1)/(N));
u=uvector(g,dg,N+1);
start=u;
endtime=1;
step=0.0025;
t=step;
nstep=round(endtime/step);
position=[u(1:N+1,1)];
time=[];
energy=[];
A=derivex(N-1);

%symplektisk euler
for ii=1:nstep
    t=t+step;
    q = u(1:N+1);
    v = u(N+2:end);
    v = v + step*c^2*(A*q);   
    q = q + step*v;           

    u = [q; v];
    position=[position,q];
    time=[time,t];
    H=hamilt(u,N+1,c);
    energy=[energy,H];
end

%for ii=1:nstep-1
    %du=derivet(u,N);
    %u=u+du*step;
    %u(N+3:2*(N)+2,1)
   % time=[time,t];
    %position=[position,u(1:N,1)];
   % t=t+step;
   % energy=[energy,hamilt(u,N)];
%end

function dudt2 = derivet2(t,u)
    N=20;
    c=1;
    A=derivex(N);
    u1=u(N+2:2*(N+1),1)';
    u2=(c*A*u(1:N+1,1))';
    dudt2=[u1,u2]';
end

%[t,y] = ode45(@derivet2, time, start);
nframe=nstep+1;
% kommando för film
mov(1:nframe)= struct('cdata',[],'colormap',[]);
figure;
plot([x'],start(1:N+1,1), 'b', 'Linewidth', 1); %Plot vid tiden t=0.
axis([0 1 -1 1])
%set(gca, 'nextplot', 'replacechildren')
drawnow
mov(1)=getframe; %(gcf)Första frame i filmen.
for m=1:nstep
X = [x']; U = [position(1:N+1,m)];
plot(X, U, 'b', 'Linewidth', 1)
hold on;
%typ approximativ exakt lösning 
 t = (m)*step;
 list=[0];
 u_exact=[0.5*( g(-c*t) + g(c*t) )];
 for ii=1:N
    xp = mod(ii*1/N + c*t, 2);
    xp(xp > 1) = 2 - xp(xp > 1);
    xm = mod(ii*1/N - c*t, 2);
    xm(xm > 1) = 2 - xm(xm > 1);
    ug = 0.5*( g(xp) + g(xm) );
    %ug=0.5*( g((1/(N-1))*ii-c*t) + g((1/(N-1)*ii+c*t) ));
    u_exact=[u_exact,ug];
    list=[list,ii*(1/(N-1))];
 end

%plot(X',u_exact','r--','Linewidth',1)
hold off;

.....
text(0.05,-0.8, sprintf('t=%.2f', t))
set(gca, 'nextplot', 'replacechildren')
drawnow
mov(m+1)=getframe(gcf);
end
plot(time,energy)
  


 
