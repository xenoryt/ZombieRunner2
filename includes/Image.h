#ifndef IMAGEHANDLER
#define IMAGEHANDLER

#include "SDL/SDL.h"
#include "Misc.h"


//namespace imgsource is NOT meant to be used by other developers and should remain hidden
namespace imgsource
{
	/* struct ImageSource contains all the information of a loaded image
	 * 
	 * this struct stores information such as the the SDL_Surface*, 
	 * number of frames and where each frame is on the surface
	 * */
	 //TODO: Add in option to rotate images by cropping the image
	struct ImageSource {
	private:
		vector< SDL_Rect > frames;
		bool rotated;
		
	public:
		SDL_Surface *source;
		string file;
		int defDelay; //default delay between frames for animation
		bool rotated; //true if the source has been pre-rotated (to save cpu usage)
		
		ImageSource()
		{
			source = NULL;
			file = "";
			rotated = false;
			defDelay = 0;
		}
		ImageSource(string sourceFile, SDL_Surface *surface, int framew = -1, int frameh = -1, int nframes = -1, int delay = 0)
		{
			source = surface;
			file = sourceFile;
			rotated = false;
			if (framew > 0 && frameh > 0)
			{
				LoadSheet(source, framew, frameh, nframes, true);
				defDelay = delay;
			}
		}
		
		inline int Frames()
		{
			return frames.size();
		}
		
		inline SDL_Rect *Clip(int index)
		{
			return (index < frames.size()) ? &frames[index] : NULL;
		}
		inline void Draw(SDL_Surface *dst, SDL_Rect dstrect, int frame)
		{
			SDL_Blitsurface(source, Clip(frame), dst, dstrect); 
		}
		
		//use SourceImages::GetSource() to load sheet
		bool LoadSheet(SDL_Surface *sheet, int framew = -1, int frameh = -1, int nframes = -1, bool rotate = false, bool overwrite = false)
		{
			if (frames.size() > 0)
			{
				if (overwrite)
					Clear();
				else
					return false;
			}
			
			if (sheet->w % framew != 0 && sheet->h % frameh != 0)
				return false;
			
			for(int y = 0; y < sheet->h / frameh; y++)
				for(int x = 0; x < sheet->w / framew; x++)
				{
					if (nframes-- == 0)
						break;
						
					frames.push_back(GetRect(x*framew, y*frameh, framew, frameh);
				}
			
			return true;
		}
	};
	
	
	/* ImageSourcesClass handles loading all the images
	 * This is meant to be a singleton 
	 * 
	 * Using GetSource(string sourceFile) will first search through all the
	 * images that have already been loaded and return the loaded image if
	 * sourceFile has been loaded before. If not, it will load image and
	 * return that
	 * */
	class ImageSourcesClass {
	public:
		static vector<ImageSource> sources;
		
		bool isSourced(string sourceFile, ImageSource *out = NULL)
		{
			//TODO: omp this for
			for (int i = 0; i < sources.size(); i++)
				if (sources[i].file == sourceFile)
				{
					out = out ? &sources[i];
					return true;
				}
			
			out = NULL;
			return false;
		}
		//Unnecessary?
		//bool isSourced(SDL_Surface *sourceImage, ImageSource *out = NULL)
		//{
		//	//TODO: omp this for
		//	for (int i = 0; i < sources.size(); i++)
		//		if (sources[i].source == sourceImage)
		//		{
		//			out = out ? &sources[i];
		//			return true;
		//		}
		//	
		//	out = NULL;
		//	return false;
		//}
		
		bool AddSource(string sourceFile, int framew = -1, int frameh = -1, int nframes = -1)
		{
			if (isSourced(sourceFile))
				return true;
			
			//load source
			SDL_Surface *surface = LoadImage(sourceFile);
			
			if (surface != NULL)
			{
				sources.push_back(Source(surface, framew, frameh, nframes));
				return true;
			}	
			
			return false;
		}
		
		ImageSource* GetSource(string sourceFile)
		{
			ImageSource *ret = NULL;
			isSourced(sourceFile, ret);
			return ret;
		}
		
		
		//methods to remove images 
		void Clear()
		{
			//clear everything 
			for (int i = 0; i < sources.size(); i++)
				SDL_FreeSurface(sources[i]);
		}
		void Clear(SDL_Surface *source)
		{
			for (int i = 0; i < sources.size(); i++)
			{
				if (source == sources[i])
					sources.erase(sources.begin() + i);
			}
			SDL_FreeSurface(source);
		}
		void Clear(string file)
		{
			for (int i = 0; i < sources.size(); i++)
			{
				if (sources[i].file == file)
				{
					SDL_FreeSurface(sources[i].source);
					sources.erase(sources.begin() + i);
				}
			}
		}
	};
}


namespace Xenogine
{
	using namespace imgsource
	{
		//create singleton
		ImageSourcesClass *ImageSources = new ImageSourcesClass();
		
		class Image
		{
			/*TODO:
			 * add way to store dstrect in Image class
			 * */
		private:
			ImageSource *source;
			int curDelay, orgDelay; //current delay and original delay
			
		public:
			int zindex;
			int curFrame;
			SDL_Rect (*GetRect) ();
			
			Image(SDL_Rect (*RectFunc) ())
			{
				source = NULL;
				curDelay = 0;
				orgDelay = 0;
				curFrame = 0;
				GetRect = RectFunc;
			}
			Image(string sourcefile, SDL_Rect (*RectFunc) ())
			{
				source = ImageSources->GetSource(sourcefile);
				curDelay = 0;
				orgDelay = source->defDelay;
				curFrame = 0;
				GetRect = RectFunc;
			}
			Image(ImageSource is, SDL_Rect (*RectFunc) ())
			{
				source = is;
				curDelay = 0;
				orgDelay = source->defDelay;
				curFrame = 0;
				GetRect = RectFunc;
			}
			
			void Delay(int newDelay)
			{
				orgDelay = newDelay;
				curDelay = 0;
			}
			inline int Delay()
			{
				return orgDelay;
			}
			
			void Draw(SDL_Surface *dst)
			{
				SDL_Rect rect = GetRect();
				source->Draw(dst, &rect, curFrame);
			}
			
			
			//updates the animation
			void Update()
			{
				if (source->Frames() < 1)
					return;
				
				if (++curDelay > orgDelay)
				{
					if (++curFrame > source->Frames() - 1)
						curFrame = 0;
				}
			}
			
			void Clear(bool permanent = false)
			{
				//permanently clearing prevents image from being used again
				if (permanent)
					SDL_FreeSurface(source);
				
				source = NULL;
				frames.clear();
			}
			
			~Image()
			{
				Clear();
			}
		};
	}
	
	struct ImageIndex
	{
		vector<Image*> list;
		int zindex;
		
		ImageIndex(int index)
		{
			zindex = index;
		}
		
		void Add(Image *newImage)
		{
			list.push_back(newImage);
		}
		bool Remove(Image *oldImage)
		{
			for (int i = 0; i < list.size(); i++)
				if (list[i] == oldImage)
				{
					list.erase(list.begin() + i);
					return true;
				}
			return false;
		}
		
		void Update()
		{
			for (int i = 0; i < list.size(); i++)
				list[i]->Update();
		}
		
		void Draw(SDL_Surface *screen)
		{
			for (int i = 0; i < list.size(); i++)
				list[i]->Draw(screen);
		}
	};
	
	class ImageHandler
	{
	private:
		static vector< ImageIndex* > Index;
		
	public:
		void Add(Image *newImage, int zindex = -1)
		{
			if (zindex != -1)
				newImage->zindex = zindex;
			
			//TODO: omp?
			for(int i = 0; i < Index.size(); i++)
			{
				if (Index[i]->zindex == newImage->zindex)
				{
					Index[i]->Add(newImage);
					return;
				}
				else if (Index[i]->zindex > newImage->zindex)
				{
					Index.insert(Index.begin()+i, new ImageIndex(newImage->zindex));
					Index[i]->Add(newImage);
					return;
				}
			}
			Index.push_back(new ImageIndex(newImage->zindex));
			Index[i]->Add(newImage);
		}
		void Remove(Image *image)
		{
			//TODO: omp
			for (int i = 0; i < Index.size(); i++)
				if (Index[i]->Remove(image))
					break;
		}
		
		void Update()
		{
			for (int i = 0; i < Index.size(); i++)
			{
				Index[i]->Update();
			}
		}
		
		void DrawAll(SDL_Surface *screen)
		{
			for (int i = 0; i < Index.size(); i++)
			{
				Index[i]->Draw(screen);
			}
		}
	};
}