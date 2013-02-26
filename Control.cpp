#include "Control.h"

Control::Control()
{
	Data = NULL;
	parent = NULL;
	tag = "";
	
	onHover = NULL;
	onClick = NULL;
	onLeave = NULL;
	
	Anchor(NOPNT);
	anchorPoint = Pos(0,0);
	
	
	//set defaults
	type = CON;
	state = NOCHANGE;
	prevState = NOCHANGE;
	fill = false;
}

void Control::Width(int newW)
{
	if (w != newW)
	{
		w = newW;
		if (parent != NULL)
			parent->Resized();
	}
}
void Control::Height(int newH)
{
	if (h != newH)
	{
		h = newH;
		if (parent != NULL)
			parent->Resized();
	}
}


int Control::CheckMouse(Mouse *mouse)
{
	if (type == LBL)
		return 0;
	
	SDL_Rect button = GetRect();
	if ((mouse->pos.x < button.x) ||
		(mouse->pos.x > button.x+button.w)||
		(mouse->pos.y < button.y) ||
		(mouse->pos.y > button.y + button.h))
	{
		if (prevState != NOCHANGE)
			Leave();
		
		//mouse not over button
		prevState = state;
		state = NOCHANGE;
		return 0;
	}

	//reaching here means mouse is above button
	prevState = state;
	state = (mouse->leftbtn.pressed) ? MOUSEDOWN : HOVER;
	
	Hover();
	
	if (!mouse->leftbtn.handled)
		if (state == HOVER && prevState == MOUSEDOWN)
		{
			mouse->leftbtn.handled = true;
			return Click();
		}
	
	return 0;
}

void Control::Anchor()
{
	if (AnchorFunc != NULL)
		(this->*AnchorFunc)(anchorPoint);
}

void Control::Anchor(PNT dir)
{
	anchor = dir;
	switch(anchor)
	{
		case TOPLEFT:
			AnchorFunc = &Control::TopLeft;
			anchorPoint = TopLeft();
			break;
		case TOPMID:
			AnchorFunc = &Control::TopMid;
			anchorPoint = TopMid();
			break;
		case TOPRIGHT:
			AnchorFunc = &Control::TopRight;
			anchorPoint = TopRight();
			break;
		
		case MIDLEFT:
			AnchorFunc = &Control::MidLeft;
			anchorPoint = MidLeft();
			break;
		case CENTER:
			AnchorFunc = &Control::Center;
			anchorPoint = Center();
			break;
		case MIDRIGHT:
			AnchorFunc = &Control::MidRight;
			anchorPoint = MidRight();
			break;
		
		case BOTLEFT:
			AnchorFunc = &Control::BotLeft;
			anchorPoint = BotLeft();
			break;
		case BOTMID:
			AnchorFunc = &Control::BotMid;
			anchorPoint = BotMid();
			break;
		case BOTRIGHT:
			AnchorFunc = &Control::BotRight;
			anchorPoint = BotRight();
			break;
		
		default:
			AnchorFunc = NULL;
			break;
	}
}

void Control::MoveAnchor(Pos amt)
{
	truex += amt.x;
	truey += amt.y;
	Anchor(); 
	Update(); //this uses the derived class's Update() since it is virtual
}