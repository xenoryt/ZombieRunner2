#include "Base.h"

void Base::Center(int a,int b)
{
	a -= (w/2);
	b -= (h/2);
	SetPos(a,b);
}
void Base::Center(Pos p)
{
	p.x -= (w/2);
	p.y -= (h/2);
	SetPos(p.x,p.y);
}
void Base::Center(fPos p)
{
	p.x -= (w/2);
	p.y -= (h/2);
	SetPos(round(p.x),round(p.y));
}

void Base::TopLeft(Pos p)
{
	SetPos(p);
}
void Base::TopMid(Pos p)
{
	p.x -= w/2;
	SetPos(p.x, p.y);
}
void Base::TopRight(Pos p)
{
	p.x -= w;
	SetPos(p);
}

void Base::MidLeft(Pos p)	
{
	p.y -= h/2;
	SetPos(p.x, p.y);
}

void Base::MidRight(Pos p)	
{
	p.x -= w;
	p.y -= h/2;
	SetPos(p.x, p.y);
}

void Base::BotLeft(Pos p)
{
	p.y -= h;
	SetPos(p);
}
void Base::BotMid(Pos p)	
{
	p.x -= w/2;
	p.y -= h;
	SetPos(p.x, p.y);
}
void Base::BotRight(Pos p)
{
	p.x -= w;
	p.y -= h;
	SetPos(p);
}