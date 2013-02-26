#ifndef GAMESTATE
#define GAMESTATE

#include "Container.h"

namespace Xenogine
{
	//Create a GameState using "new GateState()" for each state in the game and assign an updater to it
	class GameState {
	private:
		vector<Container> Forms;
		
	public:
		GameState *prevState;
		
		Action (*Updater) ();
		void (*FormInitializer) (vector<Container>);
		
		GameState( void (*FInit)(vector<Container>) = NULL )
		{
			prevState = NULL;
			FormInitializer = FInit;
			Updater = NULL;
		}
		
		void Init()
		{
			if (FormInitializer != NULL)
				FormInitializer(Forms);
		}
		
		Action Update()
		{
			return Updater();
		}
		
		
		//Close shutsdown this state (but does not delete) and cuts links to other states
		void Close()
		{
			for (int i = 0; i < Forms.size(); i++)
			{
				if (Forms[i] != NULL)
					delete Forms[i];
			}
			
			prevState = NULL;
			
		}
		
		//Terminate deletes this state and all the linked states as well
		void Terminate()
		{
			if (prevState != NULL)
				delete prevState;
			delete this;
		}
		
		
		~GameState()
		{
			Close();
			delete this;
		}
	};
}
#endif