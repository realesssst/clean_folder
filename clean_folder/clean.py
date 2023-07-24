from pathlib import Path
import shutil
import re
import sys

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    path = Path(name)
    t_name = path.stem
    extension = path.suffix

    if extension:
        t_name = t_name.translate(TRANS)
        t_name = re.sub(r'\W', '_', t_name)
        return f"{t_name}{extension}"
    else:
        return name

JPEG_IMAGES = []
PNG_IMAGES = []
JPG_IMAGES = []
SVG_IMAGES = []

AVI_VIDEOS = []
MP4_VIDEOS = []
MOV_VIDEOS = []
MKV_VIDEOS = []

DOC_DOCS = []
DOCX_DOCS = []
TXT_DOCS = []
PDF_DOCS = []
XLSX_DOCS = []
PPTX_DOCS = []

MP3_AUDIOS = []
OGG_AUDIOS = []
WAV_AUDIOS = []
AMR_AUDIOS = []

ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []

MY_OTHER = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,

    'AVI': AVI_VIDEOS,
    'MP4': MP4_VIDEOS,
    'MOV': MOV_VIDEOS,
    'MKV': MKV_VIDEOS,

    'DOC': DOC_DOCS,
    'DOCX': DOCX_DOCS,
    'TXT': TXT_DOCS,
    'PDF': PDF_DOCS,
    'XLSX': XLSX_DOCS,
    'PPTX': PPTX_DOCS,

    'MP3': MP3_AUDIOS,
    'OGG': OGG_AUDIOS,
    'WAV': WAV_AUDIOS,
    'AMR': AMR_AUDIOS,
 
    'ZIP': ZIP_ARCHIVES,
    'GZ': GZ_ARCHIVES,
    'TAR': TAR_ARCHIVES,
}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()

def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()  # перетворюємо розширення файлу на назву папки jpg -> JPG

def scan(folder: Path) -> None:
    for item in folder.iterdir():
        # Якщо це папка то додаємо її до списку FOLDERS і переходимо до наступного елемента папки
        if item.is_dir():
            # перевіряємо, щоб папка не була тією в яку ми складаємо вже файли
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                # скануємо вкладену папку
                scan(item)  # рекурсія
            continue  # переходимо до наступного елементу в сканованій папці

        #  Робота з файлом
        ext = get_extension(item.name)  # беремо розширення файлу
        fullname = folder / item.name  # беремо шлях до файлу
        if not ext:  # якщо файл немає розширення то додаєм до невідомих
            MY_OTHER.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                # Якщо ми не зареєстрували розширення у REGISTER_EXTENSION, то додаємо до невідомих
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)

def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)  # робимо папку для архіва
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file)  # TODO: Check!
    except shutil.ReadError:
        print('It is not archive')
        folder_for_file.rmdir()
    filename.unlink()

def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")

def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')

    for file in AVI_VIDEOS:
        handle_media(file, folder / 'video' / 'AVI')
    for file in MP4_VIDEOS:
        handle_media(file, folder / 'video' / 'MP4')
    for file in MOV_VIDEOS:
        handle_media(file, folder / 'video' / 'MOV')
    for file in MKV_VIDEOS:
        handle_media(file, folder / 'video' / 'MKV')

    for file in DOC_DOCS:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in DOCX_DOCS:
        handle_media(file, folder / 'documents' / 'DOCX')
    for file in TXT_DOCS:
        handle_media(file, folder / 'documents' / 'TXT')
    for file in PDF_DOCS:
        handle_media(file, folder / 'documents' / 'PDF')
    for file in XLSX_DOCS:
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in PPTX_DOCS:
        handle_media(file, folder / 'documents' / 'PPTX')

    for file in MP3_AUDIOS:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in OGG_AUDIOS:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in WAV_AUDIOS:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in AMR_AUDIOS:
        handle_media(file, folder / 'audio' / 'AMR')

    for file in ZIP_ARCHIVES:
        handle_archive(file, folder / 'archives' / 'ZIP')
    for file in GZ_ARCHIVES:
        handle_archive(file, folder / 'archives' / 'GZ')
    for file in TAR_ARCHIVES:
        handle_archive(file, folder / 'archives' / 'TAR')
    
    for file in MY_OTHER:
        handle_other(file, folder / 'MY_OTHER')

    for folder in FOLDERS[::-1]:
        handle_folder(folder)

if __name__ == "__main__":
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder: {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())
