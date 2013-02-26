/* Control Class
 *	Purpose:
 *		To create an object which is able to interact
 *		with a mouse. This is meant to be a base class
 *		which buttons or units will inherit.
 *		
 *	Uses:
 *		To form the basic base class which the units and
 *		buttons will use.
 *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

#ifndef CONTROL
#define CONTROL

#include <string>
#include "Base.h"
#include "Direction.h"

class Control : public Base {
protected:
	//event functions
	virtual int Hover () { return (onHover != NULL) ? onHover(this,Data) : 0; }	//mouse is over control
	virtual int Click () { return (onClick != NULL) ? onClick(this,Data) : 0; }	//mouse clicked control (press and release)
	virtual int Leave () { return (onLeave != NULL) ? onLeave(this,Data) : 0; }	//mouse leaves control
	
	//true: tries to fill as much space in container as possible
	//false: uses static w/h
	bool fill;
	
	//which point to anchor
	PNT anchor;
	Pos anchorPoint;
	
public:
	//the control that contains/owns this control
	Control *parent;
	
	//data that this control holds and passed onto the event functions
	void *Data;
	
	//a string to distinguish this control from others
	string tag;
	
	enum Types {CON,BTN,LBL,GRP, UNT,BLD} type;
	enum State {NOCHANGE,HOVER,MOUSEDOWN} state, prevState;
	
	//returns whether control is set to fill
	bool Fill() {return fill;}
	void Fill(Control *container);
	
	//anchors control to a certain location
	void Anchor (PNT aln);
	virtual void Anchor ();
	//move anchor point by relative amount
	void MoveAnchor (Pos amt);
	
	
	BaseFncPnt AnchorFunc;
	
	//event functions (that are custom for each control)
	int (*onClick) (Control *, void *);
	int (*onHover) (Control *, void *);
	int (*onLeave) (Control *, void *);
	
	//handles resize event
	virtual void Resized () 
	{
		//alert the parent control (a container) that there has been a resize
		if (parent != NULL)
			parent->Resized();
	}
	
	//constructor
	Control();
	
	//Functions to set private variables
	virtual void Width(int newW);
	virtual void Height(int newH);
	
	//Function to check for mouse events and calls even functions accordingly
	virtual int CheckMouse(Mouse *mouse);
	
	//some functions derived classes will use
	virtual Control *Find(string id) { return NULL; }
	virtual void Update() {};
	virtual void Remove(Control *c) {};
	virtual void Clear() {};
	virtual void Draw(SDL_Surface *screen) {}
	
	virtual ~Control() {}
};
#endif
