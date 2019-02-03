import os
import subprocess

def make_icon_dirs(root, size_str):
    if not os.path.isdir(root):
        print('root={}'.format(root))
        try:
            os.mkdir(root)
        except OSError:  
            print ("Creation of the directory '{}' failed!".format(root))
            raise
                    
        for dirName in size_str:
            dirName_full = os.path.join(root, dirName)
            
            if not os.path.isdir(dirName_full):
                try:
                    os.mkdir(dirName_full)
                except OSError:  
                    print ("Creation of the directory '{}' failed!".format(dirName_full))

def export_png_images():
    size_str = ['x1', 'x1.25', 'x1.5', 'x1.75', 'x2', 'x2.5', 'x3']
    isizes = {
              16 : [16, 20, 24, 28, 32, 40, 48],
              48 : [48, 60, 72, 84, 96, 120, 144],
              }
    
    fl_48 = ['new.svg', 'open.svg', 'reopen.svg', 'tip.svg', 'www.svg']
    fl_16 = ['reopen_project.svg']
    
    root_svg = '.'    
    files = []
    for f in os.listdir(root_svg):
        if os.path.isfile(f):
            files.append(f)
            
    root_png = '../../start_here'
    make_icon_dirs(root_png, size_str)   
    
    for f in files:
        print("fn='{}'".format(f))
        if f.endswith(".svg"):
            
            if f in fl_48:
                sizel = isizes[48]
            elif f in fl_16:
                sizel = isizes[16]
            else:
                raise ValueError("Can't find filename '{}' between known files".format(f))
            
            png_fn = f[:-4]
            
            full_svg_fn = os.path.join(root_svg,f)
            ts_svg = os.path.getmtime(full_svg_fn)
            for (sstr,pngsize) in zip(size_str,sizel):
                dirn = os.path.join(root_png, sstr)
                full_png_fn = os.path.join(dirn, png_fn + '.png')
            
                if os.path.isfile(full_png_fn):
                    ts_png = os.path.getmtime(full_png_fn)
                else:
                    ts_png = 0.
                    
                if ts_svg > ts_png:
                    # svg is newer or no png yet
                    makeExport = True
                else:
                    makeExport = False
                    
                if makeExport:
                    args = ['inkscape',
                            '--file={}'.format(full_svg_fn),
                            '--export-png={}'.format(full_png_fn),
                            '--export-area-page',
                            '--export-width={}'.format(pngsize),
                            '--export-height={}'.format(pngsize),
                            ]
                    subprocess.call(args)
                    print('Exported={}'.format(full_png_fn))
                    

if __name__ == "__main__":
    export_png_images()
