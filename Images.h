#ifndef IMAGES
#define IMAGES

#include "Misc.h"

class Image {
private:
	struct Surface {
		SDL_Surface *surface;
		
		SDL_Color color;
		int alpha;
		
	}
	
public:
	
	
	void Draw(SDL_Surface *screen);
};

#endif