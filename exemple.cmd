SET mypath=%~dp0
cd %mypath%

@rem FPS: Framerate per second - Nombre d'image par second de la video
@rem Exemple pour un ensemble d'image tiff contenu dans le "images" et sauvegarde dans le dossier "video"
python tiff2video.py -in "images" -out "videos" -fps 15
pause

@rem Exemple pour une image tiff et sauvegarde dans le dossier "video" (avec le même nom, ici oeuf2.mp4)
python tiff2video.py -in "images/oeuf2.tif" -out "videos" -fps 15

pause
@rem Exemple pour une image tiff et sauvegarde video
python tiff2video.py -in "images/oeuf2.tif" -out "videos/nom_de_loeuf_video.mp4" -fps 15


