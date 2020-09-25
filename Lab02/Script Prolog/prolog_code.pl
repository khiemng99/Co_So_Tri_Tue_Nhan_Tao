%fact
male(prince_phillip).
male(prince_charles).
male(prince_andrew).
male(prince_william).
male(prince_harry).
male(prince_george).
male(prince_louis).
male(archie_harrison).
male(mark_phillips).
male(timothy_laurence).
male(prince_edward).
male(peter_phillips).
male(mike_tindall).
male(james).

female(queen_elizabeth).
female(diana).
female(camilla_parker_bowles).
female(sarah_ferguson).
female(kate_middleton).
female(meghan_markle).
female(princess_eugenie).
female(princess_beatrice).
female(princess_charlotte).
female(princess_anne).
female(sophie_rhys_jones).
female(autumn_phillips).
female(zara_tindall).
female(lady_louise_windsor).

married(queen_elizabeth,prince_phillip).
married(diana,prince_charles).
married(camilla_parker_bowles,prince_charles).
married(prince_andrew,sarah_ferguson).
married(kate_middleton,prince_william).
married(meghan_markle,prince_harry).
married(princess_anne,mark_phillips).
married(princess_anne,timothy_laurence).
married(sophie_rhys_jones,prince_edward).
married(autumn_phillips,peter_phillips).
married(zara_tindall,mike_tindall).

divorced(diana,prince_charles).
divorced(prince_charles,diana).

divorced(princess_anne,mark_phillips).
divorced(mark_phillips,princess_anne).


parent(queen_elizabeth,prince_charles).
parent(queen_elizabeth,prince_andrew).
parent(queen_elizabeth,princess_anne).
parent(queen_elizabeth,prince_edward).
parent(prince_phillip,prince_charles).
parent(prince_phillip,prince_andrew).
parent(prince_phillip,princess_anne).
parent(prince_phillip,prince_edward).

parent(diana,prince_william).
parent(diana,prince_harry).
parent(prince_charles,prince_william).
parent(prince_charles,prince_harry).

parent(sarah_ferguson,princess_eugenie).
parent(sarah_ferguson,princess_beatrice).
parent(prince_andrew,princess_eugenie).
parent(prince_andrew,princess_beatrice).

parent(kate_middleton,prince_george).
parent(kate_middleton,princess_charlotte).
parent(kate_middleton,prince_louis).
parent(prince_william,prince_george).
parent(prince_william,princess_charlotte).
parent(prince_william,prince_louis).

parent(meghan_markle,archie_harrison).
parent(prince_harry,archie_harrison).

parent(princess_anne,peter_phillips).
parent(princess_anne,zara_tindall).
parent(mark_phillips,peter_phillips).
parent(mark_phillips,zara_tindall).

parent(sophie_rhys_jones,lady_louise_windsor).
parent(sophie_rhys_jones,james).
parent(prince_edward,lady_louise_windsor).
parent(prince_edward,james).















%rule
married(Person1,Person2) :- married(Person2,Person3), Person1 = Person3, !.
divorced(Person1,Person2) :- divorced(Person2,Person3), Person1 = Person3, !.
husband(Person,Wife):-
	(married(Person,Wife);married(Wife,Person)),
	male(Person),
	not(divorced(Person,Wife)).
wife(Person,Husband):-
	(married(Person,Husband);married(Husband,Person)),
	not(divorced(Person,Husband)),
	female(Person).
father(Parent,Child):-
	parent(Parent,Child),
	male(Parent).
mother(Parent,Child):-
	parent(Parent,Child),
	female(Parent).
child(Child,Parent):-
	parent(Parent,Child).
son(Child,Parent):-
	parent(Parent,Child),
	male(Child).
daughter(Child,Parent):-
	parent(Parent,Child),
	female(Child).
grandparent(GP,GC):-
	parent(GP,X),
	parent(X,GC).
grandmother(GM,GC) :-
	parent(GM,X),
	parent(X,GC),
	female(GM).
grandfather(GF,GC) :-
	parent(GF,X),parent(X,GC),
	male(GF).
grandson(GS,GP) :-
	parent(GP,X),
	parent(X,GS),
	male(GS).
granddaughter(GD,GP) :-
	parent(GP,X),
	parent(X,GD),
	female(GD).
:- table sibling/2.
sibling(Person1,Person2):-
	parent(X,Person1),
	parent(X,Person2),
	Person1\=Person2.
brother(Person,Sibling):-
	male(Person),
	father(Father,Person),
	father(Father,Sibling),
	mother(Mother,Person),
	mother(Mother,Sibling),
	Person\=Sibling.
sister(Person,Sibling):-
	female(Person),
	father(Father,Person),
	father(Father,Sibling),
	mother(Mother,Person),
	mother(Mother,Sibling),
	Person\=Sibling.
aunt(Person,NieceNephew) :-
	female(Person),
	sister(Person,X),
	mother(X,NieceNephew).
aunt(Person,NieceNephew) :-
	female(Person),
	sister(Person,X),
	father(X,NieceNephew).
uncle(Person,NieceNephew):-
	parent(X,NieceNephew),
	sibling(Person,X),
	male(Person).
niece(Person,AuntUncle):-
	female(Person),
	parent(Parent,Person),
	sibling(Parent,AuntUncle),
	AuntUncle \= Parent.
nephew(Person,AuntUncle):-
	male(Person),
	parent(Parent,Person),
	sibling(Parent,AuntUncle),
	AuntUncle \= Parent.

