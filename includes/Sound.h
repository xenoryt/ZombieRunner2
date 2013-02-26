#ifndef SOUND
#define SOUND

namespace Xenogine
{	
	class Sound	{
		
		public:
		enum SoundType {bgm,sfx} type;
		
		void LoadMusic()
		{
			type = bgm;
		}
		void LoadSound();
		
		void PlaySound();
		void PlayMusic();
	};
	
	
	
	/* SoundHandler handles all background music and sound effects
	 * when a play function is called, it look if that file has been loaded before and play that file
	 * if it has never been loaded before, it will load it
	 * */
	
	class SoundHandler {
	private:
		vector<SDL_Chunk*> effects;
		vector<SDL_Music*> musics;
		
	public:
		void PlaySound(string soundfile);
		void PlayMusic(string musicfile);
		
		void LoadMusic(string musicfile);
		void LoadSound(string soundfile);
	}
	
}