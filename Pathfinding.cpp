#include "Pathfinding.h"

Map::Map()
{
	
	
}

Location Map::operator[] (Pos cell)
{
	if (cell.x < 0 || cell.x > GridWidth() ||
		cell.y < 0 || cell.y > GridHeight())
	{
		return Location (TNull);
	}
		
	return map[cell.y][cell.x];
}



class Unit : public Control {
private:
	//the location of the unit
	Pos here;
	
public:
	Unit() {};
	
};

class Path {
private:

	struct PathCell {
		Pos loc;
		int f,g,h;
		
		//the object that is standing on the cell
		PathCell *parent;
		
		PathCell()
		{
			loc = Pos(0,0);
		}
		PathCell(Pos l) 
		{
			f = g = h = 0;
			parent = NULL;
			loc = l;
		}
		
		void operator= (Pos p)
		{
			loc = p;
		}
	};
	
	int step;
	vector <PathCell> path;
	
public:
	Path() { step = -1; }
	
	bool NextStep(Pos *unitLoc)
	{
		if (step + 1 < path.size())
		{
			*unitLoc = path[++step].loc;
			return true;
		}
		return false;
	}
	
	void AddNeighbours(Pos cell)
	{
		//create relative positions 
		Pos pTop(0,-1), pBottom(0,1), pLeft(-1,0), pRight(1,0);
		//add all cells adjacent to the given cell
		AddCell( cell+pTop );
		AddCell( cell+pBottom );
		AddCell( cell+pLeft );
		AddCell( cell+pRight );
	}
	
	//check if a cell is already in the path list
	bool inPath(Pos cell)
	{
		for(int i = 0; i < path.size(); i++)
			if (path[i].loc == cell)
				return true;
		
		return false;
	}
	
	//some basic functions to get besic values
	inline int size()
	{
		return path.size();
	}
	inline bool isEmpty()
	{
		return path.empty();
	}
	inline int curStep()
	{
		return step;
	}
	
	void AddCell(Pos p)
	{
		path.push_back(PathCell(p));
	}
	
	//clears and resets the path
	void Clear()
	{
		path.clear();
		step = -1;
	}
	
	
	
	//Some operator overrides
	
	//appends a path to this path
	void operator+= (Path p)
	{
		for (int i = 0; i < p.size(); i++)
			path.push_back(p[i]);
	}
	void operator+= (Pos p)
	{
		path.push_back(PathCell(p));
	}
	//gets the pathcell when given an index
	PathCell operator[] (int index)
	{
		return path[index];
	}
};

class AStar {
private:
	//contains cells that have already been searched
	Path cList;
	//contains potential path cells
	Path oList;
	
public:
	Path FindPath()
	{
		/*TODO: Find path*/
	}
};