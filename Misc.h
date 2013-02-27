#ifndef MISC
#define MISC

#include <math.h>
#include <sstream>
#include <string>
#include "SDL/SDL.h"
#include "Struct.h"

//prototypes
SDL_Color GetColor(int r, int g, int b);
int GetDist(Pos a, Pos b);
std::string ToString(int i);


//inlines need to be declared in header

//make a color transparent on surface
inline void setcolorkey(SDL_Surface *surface, int r, int g, int b)
{
	SDL_SetColorKey(surface,SDL_SRCCOLORKEY,SDL_MapRGB(surface->format, r, g, b));
}
//make the entire partially transparent
inline void setalpha(SDL_Surface *surface, int alpha)
{
	SDL_SetAlpha(surface, SDL_SRCALPHA, alpha);
}

inline int round(float f)
{
	return (f >= 0) ? floor(f+0.5) : floor(f-0.5);
}


//Draw shapes
inline void DrawRect(SDL_Surface *dest, SDL_Rect rect, SDL_Color c, int alpha = 255)
{
	SDL_FillRect( dest, &rect, SDL_MapRGBA(dest->format, c.r, c.g, c.b, alpha) );
}
/* ATTN: Commented out until needed: DrawCircle
int DrawCircle(SDL_Surface*dest, Pos pos, int rad, SDL_Color c, int alpha = 255)
{
	return filledEllipseRGBA(dest, pos.x, pos.y,	//destination surface and position
                       rad,rad,						//radius x and radius y (circle uses same length for both)
                       c.r, c.g, c.b, alpha);		//colour and alpha
}
*/
#endif
