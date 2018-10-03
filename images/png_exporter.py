import os
import subprocess

def make_icon_dirs(root, icon_sizes):
    if not os.path.isdir(root):
        print('root={}'.format(root))
        try:
            os.mkdir(root)
        except OSError:  
            print ("Creation of the directory '{}' failed!".format(root))
            raise
                    
    for svgSize in icon_sizes:
        pngSize_l = icon_sizes[svgSize]
        for pS in pngSize_l:
            dirName = str(pS) + 'x' + str(pS)
            dirName_full = os.path.join(root, dirName)
            
            if not os.path.isdir(dirName_full):
                try:
                    os.mkdir(dirName_full)
                except OSError:  
                    print ("Creation of the directory '{}' failed!".format(dirName_full))

def export_png_images(startpath):
    icon_sizes = {20 : [20, 40],
                   24 : [24, 48],
                   28 : [28, 56],
                   32 : [32, 64, 96, 128],
                   }
                   
    svg_dir_path = os.path.join(startpath, 'svg')
    for root, dirs, files in os.walk(svg_dir_path):
        print("root={}".format(root))
        print("dirs={}".format(dirs))
        
        svg_dir = root[len(svg_dir_path)+1:]
        print('startpath=<{}>'.format(startpath))
        icon_dir = os.path.join(startpath,svg_dir)
        print('icon_dir=<{}>'.format(icon_dir))
        make_icon_dirs(icon_dir, icon_sizes)
        
        for f in files:
            if f.endswith(".svg"):
                fs = f[:-4]
                idx = fs.rfind('_')
                if idx == -1:
                    raise ValueError("Can't find '_' in filename '{}'".format(f))
                
                png_fn = fs[:idx]
                svg_size = int(fs[idx+1:])
                if not icon_sizes.has_key(svg_size):
                    #raise ValueError("Unhandled svg size: {}".format(f))
                    print("Unhandled svg size: {}".format(f))
                    continue
                
                full_svg_fn = os.path.join(root,f)
                ts_svg = os.path.getmtime(full_svg_fn)
                png_sizes = icon_sizes[svg_size]
                for ps in png_sizes:
                    dirn = str(ps) + 'x' + str(ps)
                    dirn = os.path.join(icon_dir, dirn)
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
                                '--export-width={}'.format(ps),
                                '--export-height={}'.format(ps),
                                ]
                        subprocess.call(args)
                        print('Exported={}'.format(full_png_fn))
                        

if __name__ == "__main__":
    export_png_images(".")
