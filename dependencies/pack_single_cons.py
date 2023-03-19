from pathlib import Path
from distutils.dir_util import copy_tree, remove_tree
import sys
import pprint
import subprocess
  
def onyx_extract_con_files(con_name):
    # cmd_extract = f"C:/Program Files/OnyxToolkit/onyx extract {con_name}".split()
    cmd_extract = f"./dependencies/onyx-20230130-linux-x64.AppImage extract {con_name}".split()
    subprocess.run(cmd_extract)

def onyx_pack_files_into_con(folder_name, new_con_name):
    # cmd_pack = f"C:/Program Files/OnyxToolkit/onyx stfs {folder_name} --to {new_con_name} --game rb2".split()
    cmd_pack = f"./dependencies/onyx-20230130-linux-x64.AppImage stfs {folder_name} --to {new_con_name} --game rb2".split()
    subprocess.run(cmd_pack)

def remove_spaces():
    # get the current working directory
    cwd = Path().absolute()
    print(cwd)

    # remove spaces from all CON names before we begin processing
    for song_folder in cwd.glob("*"):
        if "RB4-to-RB2" in song_folder.name:
            print(song_folder.name)
            for song_con in song_folder.glob("*"):
                p = Path(song_con)
                p.rename(Path(p.parent, song_con.name.replace(" ","")))

def build_packed_con_from_folder(folder_name):
    # get the current working directory
    cwd = Path().absolute()
    print(cwd)

    # for each RB4-to-RB2-* folder in the root directory of the repo
    for song_folder in cwd.glob("*"):
        if "RB4-to-RB2" in song_folder.name:
            # print(song_folder.name)
            
            if song_folder.name == folder_name:
                # create temp folder for the songs data to go
                cwd.joinpath("tmp/songs").mkdir(parents=True, exist_ok=True)
                temp_song_path = cwd.joinpath("tmp/songs")
                mega_song_dta = []
                # for each single CON in the RB4-to-RB2-* folder
                for song_con in song_folder.glob("*"):
                    onyx_extract_con_files(song_con)
                    print(song_con.name)
                    # in the *_extract/songs folder
                    for extracted in song_folder.joinpath(f"{song_con.name}_extract/songs").glob("*"):
                        if extracted.name == "songs.dta":
                            mega_song_dta.extend([line for line in open(extracted, "r")])
                            mega_song_dta.append("\n")
                        elif extracted.is_dir():
                            copy_tree(str(extracted), str(temp_song_path.joinpath(extracted.name)))
                    remove_tree(str(song_folder.joinpath(f"{song_con.name}_extract")))
                    
                with open(temp_song_path.joinpath("songs.dta"), "w") as oof:
                    oof.writelines(mega_song_dta)

                onyx_pack_files_into_con(cwd.joinpath("tmp"), f"{song_folder.name}_RB2con")
                remove_tree(str(cwd.joinpath("tmp")))

def main():

    if len(sys.argv) != 2:
        print("no folder name provided")
        exit()
    else:
        remove_spaces()
        build_packed_con_from_folder(sys.argv[1])

if __name__ == "__main__":
    main()