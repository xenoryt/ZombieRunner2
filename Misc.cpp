#include "Misc.h"

SDL_Color GetColor(int r, int g, int b)
{
	SDL_Color c = {r,g,b};
	return c;
}

//returns distance given 2 points
int GetDist(Pos a, Pos b)
{
	float x = pow(a.x - b.x, 2.);
	float y = pow(a.y - b.y, 2.);
	return sqrt(x+y);
}

std::string ToString(int i)
{
	std::stringstream ss;
	std::string str;
	ss << i;
	ss >> str;
	return str;
}