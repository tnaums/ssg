import os
import shutil

def empty_public():
    target = 'public'
    try:
        shutil.rmtree(target)
    except FileNotFoundError:
        pass
    os.mkdir(target)

def copy_to_public(source_dir, target_dir):
    contents = os.listdir(source_dir)
    for content in contents:
        path = os.path.join(source_dir, content)
        if os.path.isfile(path):
            shutil.copy(path, target_dir)
        elif os.path.isdir(path):
            new_dir = os.path.join("public", content)
            os.mkdir(new_dir)
            copy_to_public(path, new_dir)
    
    
def main():
    empty_public()
    copy_to_public('static', 'public')

if __name__ == "__main__":
    main()
    
