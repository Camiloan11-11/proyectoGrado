import os
from moviepy import VideoFileClip

def convert_mov_to_mp4(mov_file_path, output_file_path):
    """
    Convierte un archivo MOV a MP4.
    
    Args:
        mov_file_path (str): Ruta del archivo MOV de entrada.
        output_file_path (str): Ruta del archivo MP4 de salida.
    """
    try:
        # Cargar el archivo MOV
        video_clip = VideoFileClip(mov_file_path)
        
        # Convertir y guardar como MP4
        video_clip.write_videofile(output_file_path, codec='libx264', audio_codec='aac')
        print(f"Conversión exitosa: {output_file_path}")
    except Exception as e:
        print(f"Error al convertir el archivo {mov_file_path}: {e}")

def convert_all_mov_in_directory(directory):
    """
    Convierte todos los archivos MOV en un directorio a MP4.
    
    Args:
        directory (str): Ruta del directorio que contiene los archivos MOV.
    """
    for filename in os.listdir(directory):
        if filename.lower().endswith('.mov'):
            mov_file_path = os.path.join(directory, filename)
            output_file_path = os.path.join(directory, os.path.splitext(filename)[0] + '.mp4')
            convert_mov_to_mp4(mov_file_path, output_file_path)

if __name__ == "__main__":
    # Directorio que contiene los archivos MOV
    videos_directory = r'C:\pryDballTrainer\Videos'
    convert_all_mov_in_directory(videos_directory)