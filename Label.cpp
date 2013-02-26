#include "Label.h"
#include <iostream>


SDL_Color Label::Invert(SDL_Color c)
{
	SDL_Color ret;
	ret.r = 255-c.r;
	ret.g = 255-c.g;
	ret.b = 255-c.b;
	return ret;
}


Label::Label( string message) : Control()
{
	hasColor = false;
	hasText = false;
	
	textSurface = NULL;
	type = LBL;
	
	truex = 0;
	truey = 0;
	Width(DEFAULT_WIDTH);
	Height(DEFAULT_HEIGHT);
	font = NULL;

	//set texts
	text = message;

	Color();
	Font();
	//Text(message);
}/*ATTN: Can remove if not needed
Label::Label( string message, SDL_Color tColor, SDL_Color bColor ) : Label(message)
{
	Color(tColor, bColor);
}*/

void Label::Font(string f, int size)
{
	//f = "data/fonts/" + f;
	font = TTF_OpenFont(f.c_str(),size);
	if (font == NULL)
	{
		cout << "- Error loading font: "<<f<<", "<<size<<endl;
		return;
	}
	
	//redraw the text with new font
	//Text(text);
}

void Label::Color(SDL_Color btncolor, SDL_Color txtcolor)
{
	bgColor = btncolor;
	textColor = txtcolor;
	hasColor = true;
	
	type = LBL;
	
	if (hasText)
		Text(text); //recolor text
}



void Label::Text (string newText)
{
	//makes sure not to redraw null text (since rendering "" returns NULL)
	if (text == newText && text == "")
		return;
	
	if (text != newText || prevState != state || textSurface == NULL)
	{
		SDL_FreeSurface(textSurface);
		cout << "Drawing new textSurface\n";
		text = newText;
	
		if (!hasColor)
			Color(); //get color (or else it will error)
		
		SDL_Color curTextColor = (state == HOVER) ? Invert(textColor) : textColor;
		textSurface = TTF_RenderText_Solid( font, text.c_str(), curTextColor );
		
		
		SDL_Rect textRect = GetTextRect();

		//make sure text fits inside button
		Width(textRect.w + PADDING);
		Height(textRect.h + PADDING);
		
		hasText = (text != "") ? true : false;
		
		//Anchor the control
		Anchor();
	}
}

void Label::Draw(SDL_Surface *surface)
{
	Text(text); //redraw text
	SDL_Rect textRect = GetTextRect();

	SDL_Rect button = GetRect();
	//draw the rect
	SDL_Color curColor = (state == HOVER) ? Invert(bgColor) : bgColor;
	SDL_FillRect(surface,&button, SDL_MapRGB(surface->format,curColor.r,curColor.g,curColor.b));

	//center text on button
	textRect.x = Centerx() - textRect.w/2;
	textRect.y = Centery() - textRect.h/2;
	
	//draw the text
	SDL_BlitSurface(textSurface, NULL, surface, &textRect );
}

//gets rect of textSurface (assuming x and y is center)
SDL_Rect Label::GetTextRect()
{
	SDL_Rect r;
	r.x = truex;
	r.y = truey;
	if (textSurface != NULL)
	{
		r.w = textSurface->w;
		r.h = textSurface->h;
	}
	else
	{
		r.w = 0;
		r.h = 0;
	}
	return r;
}
