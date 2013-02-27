/* Base Class
 *	Purpose:
 *		Store all the basic information regarding location
 *		of the object. Also contains functions to get and 
 *		set locations based on side or center. Can also 
 *		return a SDL_Rect (which contains x,y,w,h) struct 
 *		that represents the object.
 *
 *	Uses:
 *		Inherited by any object that should appear or is 
 *		located somewhere on screen.
 *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

#ifndef BASE
#define BASE

#include "SDL/SDL.h"
#include "Misc.h"
#include <math.h>

using namespace std;

extern const int SCREEN_WIDTH;
extern const int SCREEN_HEIGHT;
extern Mouse mouse;

class Base {
protected:
	int w,h;
	float truex,truey;

public:
	
	Base(float newX = 0, float newY = 0, int newW = -1, int newH = -1)
	{
		truex = newX;
		truey = newY;
		w = newW;
		h = newH;
	}
	
	//set positions
	inline void SetPos(int newx, int newy) {truex = newx; truey = newy;}
	inline void SetPos(Pos p) { truex = p.x; truey = p.y; }
	
	inline void Left(int a)		{truex = a;}  
	inline void Right(int a)	{truex = a-w;}
	inline void Top(int b)		{truey = b;}  
	inline void Bottom(int b)	{truey = b-h;}
	
	void Center(int a,int b);
	void Center(Pos p);
	void Center(fPos p);
	
	void TopLeft(Pos p);
	void TopMid(Pos p);
	void TopRight(Pos p);
	
	void MidLeft(Pos p);
	void MidRight(Pos p);
	
	void BotLeft(Pos p);
	void BotMid(Pos p);
	void BotRight(Pos p);
	
	//declare a type to point to a base function
	typedef void (Base::*BaseFncPnt) (Pos);
	
	inline void Centerx(int x){truex = x - w/2;}
	inline void Centery(int y){truey = y - h/2;}

	//return positions;
	inline int Left()  	{ return round(truex);		}
	inline int Right() 	{ return round(truex)+w;	}
	inline int Top()	{ return round(truey);		}
	inline int Bottom()	{ return round(truey)+h;	}
	
	inline int Centerx()	{ return round(truex)+w/2;	}
	inline int Centery()	{ return round(truey)+h/2;	}
	
	inline Pos Center()		{ return Pos(round(truex+w/2),round(truey+h/2)); }
	inline fPos fCenter()	{ return fPos(truex+w/2,truey+h/2); }
	
	inline Pos TopLeft()	{ return Pos(truex, truey);		}
	inline Pos TopMid()		{ return Pos(Centerx(), truey); }
	inline Pos TopRight()	{ return Pos(truex, Right());	}
	
	inline Pos MidLeft()	{ return Pos(truex, Centery());	}
	inline Pos MidRight()	{ return Pos(Right(), Centery()); }
	
	inline Pos BotLeft()	{ return Pos(truex, Bottom());	}
	inline Pos BotMid()		{ return Pos(Centerx(), Bottom()); }
	inline Pos BotRight()	{ return Pos(Right(), Bottom());}
	
	
	//Set dimensions
	virtual inline void Width(int newW) { w = newW; }
	virtual inline void Height(int newH){ h = newH; }
	
	//Return dimensions
	inline int Width() { return w; }
	inline int Height(){ return h; }
	
	virtual SDL_Rect GetRect ()
	{
		SDL_Rect r = {truex, truey, w, h};
		return r;
	}
};
#endif
