#include "Misc.h"

SDL_Surface *LoadImage(string imageFile)
{
	//The image that's loaded
    SDL_Surface* loadedImage = NULL;
    
    //The optimized image that will be used
    SDL_Surface* optimizedImage = NULL;
    
    //Load the image using SDL_image
    loadedImage = IMG_Load( filename.c_str() );
    
    //If the image loaded
    if( loadedImage != NULL )
    {
        //Create an optimized image
        optimizedImage = SDL_DisplayFormat( loadedImage );
        
        //Free the old image
        SDL_FreeSurface( loadedImage );
    }
    
    //Return the optimized image
    return optimizedImage;
}

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


SDL_Surface* CreateSurface(int width, int height)
{
	// We acquire the settings in our return surface
    SDL_Surface *basis = SDL_GetVideoSurface();

    // create the new surface using the Right-To_Left principle
    basis = SDL_CreateRGBSurface ( basis->flags, width, height,
                                     basis->format->BitsPerPixel,
                                     basis->format->Rmask,
                                     basis->format->Gmask,
                                     basis->format->Bmask,
                                     basis->format->Amask);
    return basis;
}
void DrawSurface(Pos pos, SDL_Surface *image, SDL_Surface *dest, SDL_Rect *clip = NULL)
{
	SDL_Rect offset = GetRect(pos);
	SDL_BlitSurface( image, clip, dest, &offset);
}