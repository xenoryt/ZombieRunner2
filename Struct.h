#ifndef STRUCT
#define STRUCT

struct Pos {
	int x,y;
	Pos ()
	{x = 0; y = 0;}

	Pos(int a, int b)
	{
		x = a;
		y = b;
	}
	
	void operator= (Pos p)
	{
		x = p.x;
		y = p.y;
	}
	
	//math with positions
	Pos operator+ (Pos p)
	{
		Pos newPos;
		newPos.x = x + p.x;
		newPos.y = y + p.y;
		return newPos;
	}
	Pos operator- (Pos p)
	{
		Pos newPos;
		newPos.x = x - p.x;
		newPos.y = y - p.y;
		return newPos;
	}
	Pos operator+= (Pos p)
	{
		*this = *this + p;
		return *this;
	}
	Pos operator-= (Pos p)
	{
		*this = *this - p;
		return *this;
	}

	bool operator== (Pos p)
	{
		if (p.x != x || p.y != y)
			return false;
		return true;
	}
	bool operator!= (Pos p)
	{
		if (p.x != x || p.y != y)
			return true;
		return false;
	}
};


struct fPos {
	float x,y;
	
	fPos()
	{
		x = 0;
		y = 0;
	}
	
	fPos(int newx, int newy)
	{
		x = newx;
		y = newy;
	}
};

struct Mouse {
	//position of mouse
	Pos pos;
	
	//contains variables on the mouse buttons
	struct Buttons {
		bool pressed; //whether mouse button is pressed
		bool handled; //whether the event is handled TODO: make sure handled does not stay true
	} leftbtn, rightbtn;
	
	//constructor
	Mouse()
	{
		pos.x = 0;
		pos.y = 0;
		leftbtn.pressed = false;
		leftbtn.handled = false;
		rightbtn.pressed = false;
		rightbtn.handled = false;
	}
	
	Buttons* operator[] (int type)
	{
		if (type == 0)
			return &leftbtn;
		return &rightbtn;
	}
};

/* create Image class
class Image {
	vector<SDL_Surface*> imgs;
	int curimg, delay, curdelay;
	
	Image()
	{
		curimg = -1;
		delay = 0;
		curdelay = 0;
	}
	
	SDL_Surface *Next()
	{
		if (--curdelay <= 0)
		{
			curdelay = delay;
			curimg++;	
		}
		
		if (curimg >= imgs.size())
			curimg = 0;
		
		if (curimg < imgs.size())
			return curimg;
		
		return NULL;
	}
}*/

#endif