#include "Button.h"
#include <iostream>

Button::Button( string message, string tip, eventFunc click, eventFunc hover, eventFunc leave, void*data) : Label(message)
{
	type = BTN;
	tooltip.Text(tip);
	
	onClick = click;
	onHover = hover;
	onLeave = leave;
	Data = data;
	
	Color();
}


//Events
int Button::Hover()
{
	Tip(tooltip.Text());
	return (onHover != NULL) ? onHover(this,Data) : 0;
}

int Button::Click()
{//ATTN: may not be required
	return (onClick != NULL) ? onClick(this,Data) : 0;
}

void Button::Color(SDL_Color btncolor, SDL_Color txtcolor)
{
	bgColor = btncolor;
	textColor = txtcolor;
	hasColor = true;
	
	if (hasText)
		Text(text); //recolor text
}

void Button::Tip(string newTip)
{
	if (tooltip.Text() != newTip || tipSurface == NULL)
	{
		tooltip.Text(newTip);
	}
	
	tooltip.SetPos(mouse.pos);
	if (tooltip.Right() > SCREEN_WIDTH)
	{
		tooltip.Right(mouse.pos.x);
		if (tooltip.Left() < 0)
			tooltip.Right(SCREEN_WIDTH);
	}
	if (tooltip.Bottom() > SCREEN_HEIGHT)
		tooltip.Bottom(mouse.pos.y);
}

void Button::Draw(SDL_Surface *surface)
{
	if (state == MOUSEDOWN)
	{
		//temporarily move the button (for a click effect)
		truex+=2;
		truey+=2;
	}
	
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
	
	//draw tooltip
	if (tooltip.Text() != "" && (state == HOVER || state == MOUSEDOWN))
		tooltip.Draw(surface);
	
	if (state == MOUSEDOWN)
	{
		//revert location back after drawing
		truex -= 2;
		truey -= 2;
	}	
}