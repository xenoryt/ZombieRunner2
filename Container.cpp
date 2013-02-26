#include "Container.h"
#include <iostream> //ATTN: remove after done debugging

Container::Container(DIR dir) : Control()
{
	type = GRP;
	alignment = dir;
	bgColor = GetColor(0,0,0);
	
	cell_width = -1;
	cell_height = -1;
	PADDING = 4;
	
	h = PADDING*2;
	w = h;
}

void Container::Color(SDL_Color c)
{
	bgColor = c;
}
void Container::Cell(int cellw, int cellh, int padding)
{
	cell_width = cellw;
	cell_height = cellh;
	PADDING = padding;
}
void Container::Width(int newW)
{
	if (w != newW)
	{
		w = newW;
		for(int i = 0; i < controls.size(); i++)
		{
			controls[i]->Centerx(Centerx());
		}
		
		//Update();
		if (parent != NULL)
			parent->Resized();
	}
}
void Container::Height(int newH)
{
	if (h != newH)
	{
		h = newH;
		for(int i = 0; i < controls.size(); i++)
		{
			controls[i]->Centery(Centery());
		}
	}
}

void Container::Add(Control *ctrl, bool fill)
{
	if (ctrl == NULL)
		return;
	
	//add the control and set this as the control's parent
	ctrl->parent = this;
	controls.push_back(ctrl);
	
	//Update and notify parent of update
	Resized();
}

void Container::Remove(Control *ctrl)
{
	if (ctrl == NULL)
		return;
	
	ctrl->parent = NULL;
	ctrl->Clear(); //incase it is a Container
	for (int i = 0; i < controls.size(); i++)
	{
		if (controls[i] == ctrl)
		{
			if (alignment == TOP || alignment == BOTTOM)
				Height(h - ctrl->Base::Height());
			else
				Width(w - ctrl->Base::Width());
				
			controls.erase(controls.begin()+i);
			delete ctrl;
			break;
		}
	}
	
	Resized();
}

void Container::Remove(int index)
{
	if (index >= Size() || index < 0)
		return;
	
	controls[index]->parent = NULL;
	if (alignment == TOP || alignment == BOTTOM)
		Height(h - controls[index]->Base::Height());
	else
		Width(w - controls[index]->Base::Width());
	
	delete controls[index];
	controls.erase(controls.begin()+index);
	
	//updates the size of the container
	Resized();
}

void Container::Clear()
{
	for(int i = 0; i<controls.size(); i++)
		controls[i]->Clear(); //incase it is a Container
	controls.clear();
}

Control *Container::Find(string id)
{
	//can't search for empty string
	if (id == "")
		return NULL;
	
	//if the id is this control
	if (id == tag)
		return this;
	
	//search within the container for the control
	for (int i = 0; i < controls.size(); i++)
		if (controls[i]->tag == id)
			return controls[i];
	
	//not found
	return NULL;
}



void Container::Anchor()
{
	if (anchor == NOPNT)
		return;
	
	Pos pos = TopLeft();
	(this->*AnchorFunc)(anchorPoint);
	
	Pos movedAmt = TopLeft() - pos;
	
	for (int i = 0; i < controls.size(); i++)
	{
		controls[i]->MoveAnchor(movedAmt);
	}
}

//Update checks for the width and height of all the controls and resizes accordingly
void Container::Update()
{
	cout << "Updating " << tag << "\n";
	//TODO: Update size 
	if (alignment == TOP || alignment == BOTTOM)
	{
		//Check if the width is right
		int widest = cell_width;
		if (cell_width == -1)
			for (int i = 0; i < controls.size(); i++)
			{
				if (controls[i]->Base::Width() > widest)
					widest = controls[i]->Base::Width();
			}
		w = widest; //using Width() will create recursive effect ( == not good )
		
		int lowest = Top()+PADDING;
		//move all controls into place
		for (int i = 0; i < controls.size(); i++)
		{
			controls[i]->Centerx(Centerx());
			
			int height = (cell_height != -1) ? cell_height : 0;
			int prevheight = Top() + height + PADDING + (PADDING + height)*i;
			if (cell_height == -1)
			{
				if (i != 0)
					prevheight = controls[i-1]->Bottom() + PADDING;
			}
			
			//move control into place
			controls[i]->Top(prevheight);
			//update that control
			controls[i]->Update();
			
			lowest = controls[i]->Bottom();
		}
		h = (lowest+PADDING) - Top();
	}
	else
	{
		int highest = cell_height;
		if (highest == -1)
			for (int i = 0; i < controls.size(); i++)
			{
				if (controls[i]->Base::Height() > highest)
					highest = controls[i]->Base::Height();
			}
		h = highest+PADDING*2;
		
		int widest = Left() + PADDING;
		//move all controls into place
		for (int i = 0; i < controls.size(); i++)
		{
			controls[i]->Centery(Centery());
			
			int prevwidth = Left()+ PADDING+(PADDING + cell_width)*i;
			if (cell_width == -1)
			{
				if (i!=0)
					prevwidth = controls[i-1]->Right() + PADDING;
			}
			controls[i]->Left(prevwidth);
			controls[i]->Update();
			
			widest = controls[i]->Right();
		}
		w = (widest+PADDING) - Left();
	}
	
	Anchor();
}

//Draw the container and all the controls it contains
void Container::Draw(SDL_Surface *screen)
{
	DrawRect(screen, GetRect(), bgColor, 255);
	for (int i = 0; i < controls.size(); i++)
	{
		controls[i]->Draw(screen);
	}
}


int Container::CheckMouse(Mouse* mouse)
{
	int ret = 0;
	SDL_Rect container = GetRect();
	if ((mouse->pos.x < container.x) ||
		(mouse->pos.x > container.x+container.w)||
		(mouse->pos.y < container.y) ||
		(mouse->pos.y > container.y + container.h))
	{
		if (prevState != NOCHANGE)
			Leave();
		
		//mouse not over button
		prevState = state;
		state = NOCHANGE;
		//return 0;
	}
	else
	{
		//reaching here means mouse is above button
		prevState = state;
		state = (mouse->leftbtn.pressed) ? MOUSEDOWN : HOVER;
		
		Hover();
	}
	for (int i = 0; i < controls.size(); i++)
	{
		if (controls[i] == NULL)
			continue;
		
		ret = controls[i]->CheckMouse(mouse);
		if (ret != 0)
			break;
	}
	
	//check for mouse clicks, however after checking the controls within the container first
	if (!mouse->leftbtn.handled && ret == 0)
		if (state == HOVER && prevState == MOUSEDOWN)
		{
			mouse->leftbtn.handled = true;
			return Click();
		}
	
	return ret;
}
