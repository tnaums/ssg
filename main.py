import os
import shutil

def copy_to_public():
    target = 'public'
    shutil.rmtree(target)
    os.mkdir(target_dir)

def main():
    print('Hello there!')

if __name__ == "__main__":
    main()
