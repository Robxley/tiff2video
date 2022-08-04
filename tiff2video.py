from pathlib import Path
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
        
    if input_dir.is_file():
        _vprint("Input file: {}".format(input_dir))
        _vprint("Output directory or file: {}".format(output_dir))
        tiff2video(input_dir, output_dir, fps, verbose)
    else:
        if output_dir.is_file():
            output_dir = output_dir.parents
            _vprint("Output directory is a file. The parent folder is used instead : {}".format(output_dir))
        else:
            output_dir.mkdir(parents=True, exist_ok=True)

        files_list = glob_files(input_dir, ".tif*")

        _vprint("Input folder: {}".format(input_dir))
        _vprint("Images TIFF found: {}".format(len(files_list)))
        _vprint("Output folder: {}".format(output_dir))

        nb_file = len(files_list)
        for k, file in enumerate(files_list):
            try:
                _vprint("File ({}/{}): \"{}\"".format(k+1, nb_file, file))
                tiff2video(file, output_dir, fps, verbose)
            except Exception as e:
                _eprint(verbose, "Something wrong happen with the file ({})\n - Exception: {}".format(file, e))

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




def tiff2video(src_tiff_file, dst_video = None, fps = 24, verbose = 0):
    
    def _vprint(*args, **kwargs):
        vprint(verbose,"\t", *args, **kwargs)

    def _eprint(*args,**kwargs):
        eprint(verbose,"\t", *args, **kwargs)


    video_ext = ".mp4"


    if fps is None:
        fps = 24

    if src_tiff_file is None:
        _eprint("tiff2video - tiff source file is empty")
        return False

    src_tiff_file = Path(src_tiff_file)

    if not src_tiff_file.is_file():
        _eprint("tiff2video - source is not a file: {}".format(src_tiff_file))
        return False

    dst_video = Path(dst_video)

    if dst_video is None:
        dst_video = src_tiff_file.parent / (src_tiff_file.stem + video_ext)
    elif dst_video.is_dir() or (not dst_video.exists() and len(dst_video.suffix)==0):
        Path(dst_video).mkdir(parents=True,exist_ok=True)
        dst_video = Path(dst_video) / (src_tiff_file.stem + video_ext)

    is_ok, images = cv2.imreadmulti(str(src_tiff_file))
    if not is_ok:
        raise Exception("Can't read the image: {}".format(src_tiff_file))

    if len(images) <= 1:
        _vprint("{} is a single image. The video is not recorded".format(src_tiff_file))
        return

    height = images[0].shape[0]
    width  = images[0].shape[1]
    isColor = len(images[0].shape) > 2

    dst_video.with_suffix(video_ext)

    # Define the codec and create VideoWriter object
    #fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    out = cv2.VideoWriter(str(dst_video), fourcc, fps, (width, height), isColor)
    for image in images:
        out.write(image) # Write out frame to video
    out.release()

    _vprint("tiff2video ->: {}".format(dst_video))


    




if __name__ == "__main__":
    main()