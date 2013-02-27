#ifndef PATHFINDING
#define PATHFINDING

#include <iostream>
#include <vector>

#include "Struct.h"
#include "Control.h"

using namespace std;

enum Terrain{ TDirt, TGrass, TFlower, TNull, TMountain, TWater, TBuildingTL, TBuildingTR, TBuildingBL, TBuildingBR };

class Location {
private:
	//the type of terrain located at this terrain
	Terrain type;
	
	//this points to the object that is above this location
	Control *object;
	
public:
	Location(Terrain terrain = TDirt, Control *obj = NULL)
	{
		object = obj;
		type = terrain;
	}
	
	//if there is an object above the terrain
	inline bool HasObject()
	{
		return (object != NULL) ? true : false;
	}
	
	//if an unit can move over this location
	inline bool Passable()
	{
		return (HasObject() || type >= TNull) ? false : true;
	}
};

class Map {
private:
	vector< vector<Location> > map;

public:
	Map();
	
	Location operator[] (Pos cell);
	
	
	inline int GridWidth()	{return map[0].size();}
	inline int GridHeight() {return map.size();}
	
	bool FindPath(vector<Pos> visited, vector<Pos> *path, Pos here, Pos goal, int cost_limit);
	
};



#endif