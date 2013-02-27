#ifndef LABEL
#define LABEL

#include "SDL/SDL.h"
#include "SDL/SDL_ttf.h"

#include "Control.h"

class Label : public Control {
protected:
	static const int DEFAULT_WIDTH = 80;
	static const int DEFAULT_HEIGHT = 25;
	
	static const int PADDING = 2;
	
	bool hasColor;
	bool hasText;
	
	SDL_Surface *textSurface;
	SDL_Surface *tipSurface;
	
	string text;
	
	//Function to invert colors (used when mouse hovers)
	SDL_Color Invert(SDL_Color c);

public: 
	SDL_Color bgColor;
	SDL_Color textColor;
	TTF_Font *font;
	
	Label(string message = "");
	//Label(string message, SDL_Color t, SDL_Color b = GetColor(0,0,0));
	
	string Text()	{ return text; }
	
	void Text (string newText);

	virtual void Font(string f = "pix.ttf", int size = 12);
	virtual void Color(SDL_Color btncolor = GetColor(0,0,0), SDL_Color txtcolor = GetColor(0,255,0));
	
	virtual void Draw(SDL_Surface *surface);

	//gets rect of textSurface (assuming x and y is center)
	SDL_Rect GetTextRect();
	
	~Label()
	{
		//BUG: causes error upon exiting
		//SDL_FreeSurface(textSurface);
	}
};
#endif
