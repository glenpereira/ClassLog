import os

def remove_extension(filename):
    
    clean = [x for x in filename if x is not None]
    
    for index, file in enumerate(clean):

        filename_wo_ext = os.path.splitext(file)[0]
        filenames_stripped = filename_wo_ext.replace("_", " ")
        clean[index] = filenames_stripped
    
    return clean