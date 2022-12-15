import argparse
from io import BytesIO
import os


def main():
    parser = argparse.ArgumentParser(description='Export music file artworks')
    parser.add_argument('-d', '--music-dir', required=True, help='Music file directory')
    parser.add_argument('-f', '--artwork-filename', default='Folder.jpg', required=False, help='Artrwork file name')
    parser.add_argument('-F', '--force-export', action='store_true', help='Overwrite existing artwork files')

    args = parser.parse_args()

    print(f'Music file directory : {args.music_dir}')
    print(f'Music Artrwork file name : {args.artwork_filename}')

    export(args.music_dir, args.artwork_filename, args.force_export)


def export(dir, artwork_filename, force_export):
    print(f'export at {dir}')
    exported = False
    for f in os.listdir(dir):
        file_path = os.path.join(dir, f)
        if os.path.isdir(file_path):
            export(file_path, artwork_filename, force_export)
        else:
            if exported:
                continue

            artwork_filepath = os.path.join(os.path.dirname(file_path), artwork_filename)
            if (not force_export) \
                    and os.path.exists(artwork_filepath):
                print(f'{artwork_filepath} : already exists')
                exported = True
                continue

            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.mp3':
                export_mp3_artwork(file_path, artwork_filepath)
                exported = True
            elif ext == '.m4a':
                export_mp4_artwork(file_path, artwork_filepath)
                exported = True


def export_mp3_artwork(file_path, artwork_filepath):
    import mutagen.mp3
    from PIL import Image

    id3 = mutagen.mp3.MP3(file_path)
    artwork = id3.get("APIC:")
    if artwork:
        print(f'{file_path} : exists artwork')
        img = Image.open(BytesIO(artwork.data))
        img.save(artwork_filepath)
    else:
        print(f'{file_path} : not exists artwork')


def export_mp4_artwork(file_path, artwork_filepath):
    import mutagen.mp4

    mp4 = mutagen.mp4.MP4(file_path)
    artwork = mp4.get("covr")
    if artwork:
        print(f'{file_path} : exists artwork')
        with open(artwork_filepath, mode='wb') as f:
            f.write(artwork[0])
    else:
        print(f'{file_path} : not exists artwork')


if __name__ == "__main__":
    print(os.getcwd())
    main()
