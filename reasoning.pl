% Possible states:
quantity('Inflow', '0', '0').
quantity('Inflow', '0', '+').
%quantity('Inflow', '0', '-').
quantity('Inflow', '+', '0').
quantity('Inflow', '+', '+').
%quantity('Inflow', '+', '-').

quantity('Outflow', '0', '0').
quantity('Outflow', '0', '+').
quantity('Outflow', '0', '-').
quantity('Outflow', '+', '0').
quantity('Outflow', '+', '+').
quantity('Outflow', '+', '-').
quantity('Outflow', 'max', '0').
quantity('Outflow', 'max', '+').
%quantity('Outflow', 'max', '-').

quantity('Volume', '0', '0').
quantity('Volume', '0', '+').
quantity('Volume', '0', '-').
quantity('Volume', '+', '0').
quantity('Volume', '+', '+').
quantity('Volume', '+', '-').
quantity('Volume', 'max', '0').
quantity('Volume', 'max', '+').
%quantity('Volume', 'max', '-').

valid_states(Inflow, Volume, Outflow):-
	proportionality(Outflow, Volume),
	influence_inflow(Inflow, Volume), nl.


% if inflow = +, than deriv of volume is '+', if inflow = 0, than deriv of volume is '0'
% according to slides lecture 2 qualitative reasoning
influence_inflow(quantity('Inflow', I, C), quantity('Volume', A, I)):-
	quantity('Inflow', I, C),
	quantity('Volume', A, I).

% state and derivative of volume and outflow are always equal
proportionality(quantity('Outflow', A, I), quantity('Volume', A, I)):-
	quantity('Outflow', A, I).

% vraag1: influence outflow: doet er niet meer toe omdat vanwege proportionality vol==out??
% vraag2: kan inf(+,+), vol(0,+), out(0,+)?
% vraag3: kan inf(+,0), vol(0,+), out(0,+)?
