---
layout: post
title: read_all.py
category: article
author: Eli Heuer
---
I checked a small Python script into [pyGtkMock](https://github.com/sugarlabs/edit-fonts-activity/tree/gh-pages/mockups/pyGtkMock), it's something I wrote while reviewing and experimenting with the work so far.

It just loops through all the .ufo files in a directory and replaces:

    #load the font
    path = "sample"

...which I was having trouble working with.

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
