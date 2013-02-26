//Main game engine

#ifndef GAMEENGINE
#define GAMEENGINE

#include <iostream>
#include "GraphicHandler.h"
#include "SoundHandler.h"
#include "GameActions.h"
#include "GameState.h"

namespace Xenogine 
{
	class Engine{
	private:
		vector<Control*> units1, units2, neutral;
		SDL_Event events;
		
		//Classes
		class EventManager {
		private:
			//stores mouse info
			struct MouseInfo {
				Pos pos;
				bool handled;
				bool leftclick;
				bool rightclick;
			};
			
			//this points to a function that contains instructions on how events are handled
			Action (*Handler) (SDL_Event);
			
		public:
			
			MouseInfo mouse;
			
			inline void operator= (void (*newHandler) (SDL_Event))
			{
				Handler = newHandler;
			}
			
			void Handle()
			{
				SDL_GetMouseState(&mouse.pos.x, &mouse.pos.y);
				while (SDL_PollEvent(&event))
				{
					Handler(event, &mouse);
				}
			}
		};
		
		
		
		
		//GameStateManager is used in the engine only to switch between GameStates using GameState's prevState
		//it also calls all the GameState functions such as Update()
		class GameStateManager {
		private:
			GameState *state; 
			
		public:
			void operator= (GameState *newState, bool overlay = false)
			{
				if (state == newState)
					return;
				
				if (overlay)
					newState->prevState = state;
				else
					state->Terminate();
				
				state = newState;
			}
			
			bool InitState()
			{
				if (state != NULL)
				{
					state->Init();
					return true;
				}
				
				return false;
			}
			
			bool ExitState()
			{
				if (state != NULL && state->prevState != NULL)
				{
					GameState *oldState = state->prevState;
					state->Close();
					state = oldState;
					return true;
				}
				
				//Error: cannot exit state
				return false;
			}
			
			void Update()
			{
				Action action = state.Update();
				switch (action.action)
				{
					case ACT_EXITSTATE:
						state = state.prevState;
						break;
				};
			}
		};
		
	public:
		//GraphicManager	*Graphics;
		//SoundManager	*Sound;
		StateManager	*State;
		EventManager	*Event;
		
		SDL_Surface *screen;
		
		Engine()
		{
			State = new StateManager();
			Event = new EventManager();
		}
		
		void MessageBox(string message, string caption = "", bool shutdown = false); //display error message (and closes program)
		
		void Init(string GameTitle) //initializes all services
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

			//Set the window caption
			SDL_WM_SetCaption( GameTitle, NULL ); //TODO: icon

			//If everything initialized fine
			return true;
		}
		void Shutdown() //shuts down all services
		{
			cout << "Shutting Down..." <<endl;
			/* TODO for shutting down
			 * close connection to server?
			 * exit sdl
			 * exit opengl (if used)
			 * free surfaces and sounds
			 * clear memory 
			 * */
			 SDL_Quit();
		}
		void Exit() //Safely exits program
		{
			cout << "Initializing Shutdown Procedures..."<endl;
			Stop();
			Shutdown();
			cout << "Exited Gracefully"<<endl;
			exit(0);
		}
		
		
		void Start(); //Starts game
		void Pause(); //Pauses game
		void Stop()  //Stops game
		{
			cout << "Stopping Game..." <<endl;
			/* TODO for stopping game
			 * send packet to end game (if networked)
			 * stop ai (if any)
			 * */
		}
		
		void SetState(GameState *state) //Set the state (and the event) 
		{
			if (state != NULL)
			{
				State = state;
				State->InitState();
			}
			
		}
		void SetEvent(GameEvent *event)
		{
			if (event != NULL)
				Event = event;
		}
		
		/* ExitState:
		 * Leaves the current state and returns to the previous one
		 * If there is no previous state, it exits the program
		 * */
		void ExitState()
		{
			//if exit state is not possible because there is no state to revert back to
			if (!State->ExitState())
				Exit();
		}
	};
}

/* TODO: 
 * Create MessageBox(string message) function that switches to 
 * EventManager Message which displays message
 * */

#endif