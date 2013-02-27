#ifndef FORMS
#define FORMS

#include "Container.h"
#include "Button.h"

vector<Control*> forms;


//function to find a control in forms
Control *Find(string id)
{
	for (int i = 0; i < forms.size(); i++)
	{
		Control *ctrl = NULL;
		if ((ctrl = forms[i]->Find(id)) != NULL)
			return ctrl;
	}
	
	cout << "Error: did not find control '" << id <<"'\n";
	return NULL;
}



/*

void Init_Forms()
{
	lblTitle = new Label("Game Name");
	
	btnSingle = new Button("Singleplayer");
	btnMulti = new Button("Multiplayer");
	btnOption = new Button("Settings");
	btnExit = new Button("Exit");
	
	
}
*/


//Functions buttons call when clicked
int NewLabel(Control *sender, void *data)
{
	if (data == NULL)
		return 0;
	
	Container *c = (Container*)data;
	c->Add(new Label("Test"));
}
int RemLabel(Control *sender, void *data)
{
	if (data == NULL)
		return 0;
	
	Container *c = (Container*)data;
	c->Remove(c->Size()-1);
}
int DelCol(Control *sender, void *data)
{
	if (data != NULL)
	{
		Container *c = (Container*)data;
		Container *parent = (Container*)c->parent;
		Container *sParent = (Container*)sender->parent->parent;
		parent->Remove(c);
		
		sParent->Remove(sender->parent);
	}
	else
	{
		Container *c = (Container*)Find("new list");
		c->Remove(c->Size()-1);
		
		c = (Container*)Find("new btns");
		c->Remove(c->Size()-1);
	}
}

int AddCol(Control *sender, void *data = NULL)
{
	static int count = 0;
	Control *ctrl = Find("new list");
	
	if (ctrl != NULL)
	{
		Container *box = (Container*)ctrl;
		
		if (box->Size() < 5)
		{
			Container *c = new Container(BOTTOM);
			box->Add(c);
			c->tag = "box " + ToString(++count);
		}
		else
			return 0;
	}
	else 
		return 0;
	ctrl = Find("new btns");
	if (ctrl != NULL)
	{
		Container *box = (Container*)ctrl;
		
		Container *c = new Container(BOTTOM);
		c->Add(new Button("Add", "Adds new label", NewLabel, NULL,NULL, Find("box " + ToString(count))));
		c->Add(new Button("Remove", "Removes the last label", RemLabel, NULL,NULL, Find("box " + ToString(count))));
		c->Add(new Button("Delete", "Deletes this column", DelCol, NULL,NULL, Find("box " + ToString(count))));
		
		box->Add(c);
	}
}

//int main calls this to initialize all forms
void Init_Forms()
{
	Button *Add = new Button("New", "Add new column", AddCol);
	Button *Del = new Button("Del", "Delete last column", DelCol);
	
	Container *a = new Container(TOP);
	Container *b = new Container(LEFT);
	Container *c = new Container(LEFT);
	
	a->tag = "grpBtn";
	b->tag = "new list";
	c->tag = "new btns";
	/* creates static cell sizes (buggy)
	b->Cell(50,50,4);
	c->Cell(50,50,4);
	*/
	a->TopLeft(Pos(50, 100));
	b->TopMid(Pos(SCREEN_WIDTH/2-100, 100));
	b->Control::Anchor(TOPLEFT);
	c->BotMid(Pos(SCREEN_WIDTH/2-100, SCREEN_HEIGHT-100));
	c->Control::Anchor(TOPLEFT);
	
	a->Add(Add);
	a->Add(Del);
	
	forms.push_back(a);
	forms.push_back(b);
	forms.push_back(c);
}
#endif
