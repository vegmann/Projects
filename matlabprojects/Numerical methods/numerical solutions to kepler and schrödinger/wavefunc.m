
%räknar ut energin för systemet
function H= hamilt(u,N,c)
A=derivex(N-2);
H=(norm(u(N-1:2*(N-2),1))^2)/2-c^2*dot(A*u(1:N-2,1),u(1:N-2,1))/2;
end

%givet ett N räknar ut deriveringsmatrisen 
function A = derivex(N)
h=1/(N+2);
d=linspace(-2/h^2,-2/h^2,N);
v=linspace(1/h^2,1/h^2,N-1);
A=zeros(N)+diag(d)+diag(v,1)+diag(v,-1);
end

%givet vektorn u räknar ut den resulterade deriverade vektorn, borde dock
%ändra så att konstanten c är ett argument
function dudt2 = derivet(u,N,c)
    A=derivex(N-2);
    u1=u(N-1:2*(N-2),1)';
    u2=(c^2*A*u(1:N-2,1))';
    dudt2=[u1,u2]';
end

%skapar en startvektor vid t=0 givet begynnelsefunktion
function u = uvector(g,dg,N)
    step=1/N;
    h=1/N;
    u=[];
    du=[];
    for ii=1:N-2
        step
        u=[u,g(step)];
        %du=[du,dg(step)];
        %kommenterat ifall man skulle ha begynnelsevilkor för derivatan
        du=[du,0];
        step=step+h;
       
    end 
    %u=[u,0];
    %du=[du,dg(1)];
    u=[u,du]';
end

%massa konstanter och startvärden
c=1;
g=@(x) (exp(-200*(x-0.5)^2));
dg=@(x) (-(400*x-200)*exp(-200*(x-0.5)^2));
N=50;
x=(((2:N-1)-1)/(N-1));
u=uvector(g,dg,N);
start=u;
endtime=1;
step=0.0025;
t=step;
nstep=round(endtime/step);
position=[u(1:N-2,1)];
time=[];
energy=[];
A=derivex(N-2);
%euler frammåt, finns absolut bättre och kommer göra om det finns tid
%men efterssom det är så kort tid beskrivs pulsen på ett ok sätt
%for ii=1:nstep-1
  %  du=derivet(u,N,c);
  %  u=u+du*step;
   % time=[time,t];
   % position=[position,u(1:N-2,1)];
   % t=t+step;
   % H=hamilt(u,N);
   % energy=[energy,H];
   %end

 for ii=1:nstep-1
    t=t+step;
    q = u(1:N-2);
    v = u(N-1:end);
    v = v + step*c^2*(A*q);   
    q = q + step*v;           

    u = [q; v];
    position=[position,q];
    time=[time,t];
    H=hamilt(u,N,c);
    energy=[energy,H];
end

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
plot([0;x';1],start(1:N,1), 'b', 'Linewidth', 1); %Plot vid tiden t=0.
axis([0 1 -1 1])
%set(gca, 'nextplot', 'replacechildren')
drawnow
mov(1)=getframe; %(gcf)Första frame i filmen.
for m=1:nstep
X = [0;x';1]; U = [0;position(1:N-2,m);0];
plot(X, U, 'b', 'Linewidth', 1)
hold on;
%Plotta även lösningen från d'Alemberts formel
 t = (m)*step;
 list=[0];
 u_exact=[0.5*( g(-c*t) + g(c*t) )];
 for ii=1:N-1
    ug=0.5*( g((1/(N))*ii-c*t) + g((1/(N)*ii+c*t) ));
    u_exact=[u_exact,ug];
    list=[list,ii*(1/(N-1))];
 end
 
%u_exact=[u_exact, 0.5*( g(1-c*t) + g(1+c*t) )];
 
plot(X',u_exact','r--','Linewidth',1)
hold off;

.....
text(0.05,-0.8, sprintf('t=%.2f', t))
set(gca, 'nextplot', 'replacechildren')
drawnow
mov(m+1)=getframe(gcf);
end
img = read(v, 120);
imshow(img)

       

  


 
