#ifndef CONTAINER
#define CONTAINER

#include <vector>
#include "Base.h"
#include "Control.h"

class Container : public Control {
private: 
	//Aligns all the controls according to the alignment (cannot be changed)
	DIR alignment;
	
	//Background color
	SDL_Color bgColor;
	
	vector<Control *> controls;
	int PADDING;
	
	//TODO: Add in static cell dimensions
	int cell_width, cell_height;
	bool flexible;
public:
	//used to update the size of the container
	void Update();
	
	//overrides the resize event in control
	void Resized() 
	{
		Update(); 
		if (parent != NULL)
			parent->Resized();
	}
	
	//constructor
	Container(DIR dir);
	
	//Functions to set private variables
	void Color(SDL_Color c);
	void Cell(int cellw, int cellh, int padding = 4);
	inline void Width(int newW);
	inline void Height(int newH);
	
	
	//Functions to handle the list of controls
	void Add(Control *ctrl, bool fill = true);
	void Remove(Control *ctrl);
	void Remove(int index);
	void Clear();
	
	int Size()
	{
		return controls.size();
	}
	
	//finds a control inside this container
	Control *Find(string id);
	
	void Anchor();
	void Draw(SDL_Surface *);
	
	//Override the checkmouse on the Control class
	int CheckMouse(Mouse *mouse);
	
	~Container()
	{
		for (int i = 0; i < controls.size(); i++)
			delete controls[i];
	}
};

#endif