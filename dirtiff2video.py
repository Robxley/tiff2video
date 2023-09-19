from pathlib import Path
from shutil import ExecError
import cv2

# Exemple commande 
# python tiff2video.py -in "./dossier_images" -out "./videos" -fps 15       

def main():
    #os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # too remove tensorflow info and warning msg
    import argparse
    parser = argparse.ArgumentParser(description="CNN Inference.")
    parser.add_argument("-in", "--input_dir", metavar="path", required=True, type=str,
                        help="Path of directory containing the image list (tiff format)")
    parser.add_argument("-out", "--output_dir", metavar="path", required=False, type=str,
                        help="Directory path where to save the video files")
    parser.add_argument("-fps", "--image_rate", metavar="integer", required=False, type=int,
                        help="Frame per second. Video speed")
    parser.add_argument("-v", "--verbose", metavar="integer", required=False, type=int,
                        help="Frame per second. Video speed")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    verbose = args.verbose
    fps = args.image_rate

    def _vprint(*args, **kwargs):
        vprint(verbose,*args, **kwargs)

    def _eprint(*args,**kwargs):
        eprint(verbose,*args, **kwargs)

    if verbose is None:
        verbose = 1

    if fps is None:
        fps = 24
        _vprint("Default video speed (FPS) set as: {}".format(fps))
    else:
        _vprint("Video speed (FPS): {}".format(fps))

    if input_dir is None:
        _vprint("Input directory is not defined. The current directory is used")
        input_dir = Path(".").resolve()
    else:
        input_dir = Path(input_dir)

    if output_dir is None:
        _vprint("Output directory is not set. The input directory is used by default")
        output_dir = input_dir if input_dir.is_dir() else input_dir.parent
    output_dir = Path(output_dir)
        
    if input_dir.is_dir():
        _vprint("Input directory: {}".format(input_dir))
        _vprint("Output directory or file: {}".format(output_dir))
        dirtiff2video(input_dir, output_dir, fps, verbose)
    else:
        _vprint("Input is not a directory: {}".format(input_dir))

    _vprint("done")


# verbose print
def vprint(verbose, *args, **kwargs):
    if verbose == 1 or verbose == True:
        print(*args, **kwargs)

# error/exception print
def eprint(verbose, *args, **kwargs):
    if verbose > 1 or verbose == True:
        print(*args, **kwargs)

#%%
# Get the file list of the folder.
# a extension filter can be used
def glob_files(dir_path, file_exts=None, verbose=False):

    if(file_exts is None):
        file_exts = [".tif*",".png",".jpg",".bmp", ".gif", ".jepg", ".webp", ".hdr"]

    if not Path(dir_path).exists():
        return None
    
    if(isinstance(file_exts, str)):
        file_exts = [file_exts]
    
    files = []
    for ext in file_exts:
        files += [str(f) for f in Path(dir_path).glob("**/*"+ext)]

    if(verbose):
        lenght = len(dir_path)
        if(dir_path[-1] != '\\' or dir_path[-1] != '/'):
            lenght+=1
        print("Files :")
        [print(str(i)[lenght:]) for i in files]
    return files




def dirtiff2video(input_dir, dst_video = None, fps = 24, verbose = 0):
    
    def _vprint(*args, **kwargs):
        vprint(verbose,"\t", *args, **kwargs)

    def _eprint(*args,**kwargs):
        eprint(verbose,"\t", *args, **kwargs)

    video_ext = ".mp4"

    if fps is None:
        fps = 24

    if not Path(input_dir).is_dir():
        _eprint("input_dir is not a directory")
    
    files_list = glob_files(input_dir, ".tif*")
    if files_list is None or len(files_list) == 0:
        _eprint("dirtiff2video - directory input is empty")
        return False
    
    number_of_tiff = len(files_list)
    
    _vprint("Number of TIFF files:", number_of_tiff)

    dst_video = Path(dst_video)

    if dst_video is None:
        dst_video = input_dir / (Path(files_list[0]).stem + video_ext)
    elif dst_video.is_dir() or (not dst_video.exists() and len(dst_video.suffix)==0):
        Path(dst_video).mkdir(parents=True,exist_ok=True)
        dst_video = Path(dst_video) / (Path(files_list[0]).stem + video_ext)
        
    _vprint("Video destination path:", dst_video)

    img_shape = None
    video_out = None
    count = 0
    
    for img_path in files_list:
        try:
            count+=1
            img = cv2.imread(img_path)
            if img is None:
                _eprint("Can't read the image: {}".format(img_path))
                continue
                
            if img_shape is None:
                img_shape = img.shape
                height = img_shape[0]
                width  = img_shape[1]
                isColor = len(img_shape) > 2
                dst_video.with_suffix(video_ext)
                # Define the codec and create VideoWriter object
                #fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
                fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
                video_out = cv2.VideoWriter(str(dst_video), fourcc, fps, (width, height), isColor)
            elif img.shape != img_shape:
                _eprint("Image shape don't match with the previous images: {}".format(img_path))
                continue
            
            _vprint("{}/{} - Fill the video with: {}".format(count, number_of_tiff, img_path))
            
            video_out.write(img) # Write out frame to video

        except Exception as e:
            _eprint("Exception: {} - {}".format(e, img_path))

        
    if video_out is not None:    
        video_out.release()

    _vprint("dirtiff2video ->: {}".format(dst_video))



if __name__ == "__main__":
    main()