import os
from defcon import Font

# loop through all .UFO files in the same directory as this script
# print glyph count and glyph names
for ufo_input_filename in os.listdir('.'):
    if not ufo_input_filename.endswith('.ufo'):
        continue # skip non-ufo files
    font = Font(ufo_input_filename)
    print ''
    print 'Processing -- ' + ufo_input_filename + '...'
    print(ufo_input_filename + " has " + str(len(font)) + " glyphs");

    for glyph in font:
        print(glyph.name);
