#ifndef ACTION
#define ACTION

//The different actions that can be sent to game engine to handle
enum Actions {	ACT_NOACTION, 
				ACT_PAUSE, 
				ACT_STARTSELECT, 
				ACT_STOPSELECT, 
				ACT_MOVEUNITS, 
				ACT_PRODUCEUNITS, 
				ACT_EXITSTATE, 
				ACT_EXITGAME };

struct Action {
	Actions action;
	void *data;
};



//To be used to send information on a unit

//The different unit types
enum UnitType {	UNT_MARINE, 
				UNT_TERRATRON,
				UNT_TANK,
				UNT_HVYTANK };
enum UnitAction{UNT_MOVE,
				UNT_ATTACK,
				UNT_SPECIAL };

struct UnitData {
	UnitType type;
	UnitAction action;
	Pos location;
};

#endif