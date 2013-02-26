#ifndef BUTTON
#define BUTTON

#include "SDL/SDL.h"
#include "SDL/SDL_ttf.h"
#include "Label.h"

class Button : public Label {
private:
	static const int DEFAULT_WIDTH = 80;
	static const int DEFAULT_HEIGHT = 25;
	
	int Hover();
	int Click();
	
public: 
	Label tooltip;
	
	typedef int (*eventFunc) (Control *, void *);
	Button(string message = "", string tip = "", eventFunc click = NULL, eventFunc hover = NULL, eventFunc leave = NULL, void* data = NULL);
	
	string Tip() { return tooltip.Text(); }
	void Tip(string tip);
	
	virtual void Color(SDL_Color btncolor = GetColor(255,0,0), SDL_Color txtcolor = GetColor(0,0,0));
	void Draw(SDL_Surface *surface);

	~Button()
	{
		SDL_FreeSurface(textSurface);
	}
};
#endif
