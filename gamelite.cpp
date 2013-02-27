#ifndef __cplusplus
#error Requires C++ Compiler!
#endif

#include<iostream>
#include<string>
#include<vector>
#include<time.h>

#ifdef __WINDOWS__
	#include <windows.h>
#endif

#include "SDL/SDL.h"
#include "SDL/SDL_ttf.h"
#include "GL/glu.h"

#define forr(a,b,c,d) for(a=b;a c;a d)
#define RenderText TTF_RenderText_Solid

using namespace std;


#include "Base.h"
#include "Misc.h"
#include "Struct.h"
#include "Button.h"
#include "Pathfinding.h"

//Screen attributes
const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;
const int SCREEN_BPP = 32;

SDL_Surface *screen = NULL;

vector<Button> buttons;

Mouse mouse;

//The event structure
SDL_Event event;

bool init()
{
    //Initialize all SDL subsystems
    if( SDL_Init( SDL_INIT_EVERYTHING ) == -1 )
    {
        return false;
    }

    //Set up the screen
    screen = SDL_SetVideoMode( SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_BPP, SDL_SWSURFACE );

    //If there was an error in setting up the screen
    if( screen == NULL )
    {
        return false;
    }

    //Initialize SDL_ttf
    if( TTF_Init() == -1 )
    {
        return false;
    }

    //Set the window caption
    SDL_WM_SetCaption( "Testing GUI", NULL );

    //If everything initialized fine
    return true;
}


//Includes all the forms/menus that the game will use
#include "Forms.h"

int main(int argc, char *argv[])
{
	cout << "Starting main thread\n";
    //Quit flag
    bool quit = false;

    //Initialize
    if( init() == false )
    {
        return 1;
    }
	
	srand(time(NULL));
	Init_Forms();
	
	//While the user hasn't quit
    while( quit == false )
    {
		SDL_GetMouseState(&mouse.pos.x, &mouse.pos.y);
		
		for (int i = 0; i < 2; i++)
			mouse[i]->handled = false;
		
		while (SDL_PollEvent(&event))
		{
			//If the user has Xed out the window
			if( event.type == SDL_QUIT )
			{
				//Quit the program
				quit = true;
			}
			if (event.type == SDL_KEYDOWN)
			{
				if (event.key.keysym.sym == SDLK_ESCAPE)
					quit = true;
			}
			//mouse keypresses
			if ( event.type == SDL_MOUSEBUTTONDOWN )
			{
				if (event.button.button == SDL_BUTTON_LEFT)
					mouse.leftbtn.pressed = true;
			}
			if ( event.type == SDL_MOUSEBUTTONUP )
				if (event.button.button == SDL_BUTTON_LEFT)
					mouse.leftbtn.pressed = false;
		}
		
		int i;
		forr (i,0,<forms.size(),++)
		{
			if (forms[i]->CheckMouse(&mouse) != 0)
			{
				break;
			}
		}
		
		//Show the background
		SDL_FillRect( screen, &screen->clip_rect, SDL_MapRGB( screen->format, 80,50,55 ) );
		
		//draw each button
		for(int i = 0; i < forms.size(); i++)
		{
			forms[i]->Draw(screen);
		}

		SDL_Delay(50);
		
		SDL_Flip(screen);
    }
	
	SDL_Quit();
	
	return 0;
}
