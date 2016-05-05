---
layout: post
title: Current Feature List and the Timeline
category: article
author: Yash Agarwal
---

Eli, Dave and I decided to move forwards with an Activity for the Sugar Desktop (in Python) because it has many more users today than Sugarizer. 
Using Python allows me to take advantage of the libraries that [Trufont](https://github.com/trufont/trufont/) uses.

This font editor Activity is planned to include the following features and follow the [Sugar Human Interface Guidelines](https://wiki.sugarlabs.org/go/Human_Interface_Guidelines):

1: Font Manager

* Show all the available fonts found in the system font directory
* Allow the user to install/uninstall fonts,  make 'collections' within the library.

Related pages:  
<https://wiki.sugarlabs.org/go/The_Undiscoverable/Fonts>  
<http://wiki.laptop.org/go/Font_considerations>

2: A glyph drawing interface similar to the one found proposed by Mark Simonson and available in FontForge and Glyphs: edit several glyph outlines side by side, allowing to draw and space them in the same window.

![Image of Glyph Editing Interface](https://raw.githubusercontent.com/sugarlabs/font-editor-activity/gh-pages/files/img/1.png)

3: A Testing interface

* A textbox in which the text is rendered using the font, to get visual feedback. 
* Provide predefined text templates eg. "the quick brown fox jumps over the lazy dog," and 
* Export image button, to save an image of the rendered textbox
* All this will be accompanied with thorough documentation, and...
* code commenting, which will be done hand in hand with development as we develope a better idea of the end goals        

### Timeline

I have divided the project into measurable milestones, with 12 weeks at 40 hours a week becoming 6 milestones of 2 weeks each:

#### Milestone 1: Font Manager

I wll use the [Sugar Human Interface Guidelines](https://wiki.sugarlabs.org/go/Human_Interface_Guidelines) to build basic GUI functionality like Toolbar(s), Navbar , Work Space, etc.

The entire activity will be made as a Sugar Activity in Python.

![Image of Activity Interface](https://raw.githubusercontent.com/sugarlabs/font-editor-activity/gh-pages/files/img/2.PNG)

1.0 Activate/Deactivate: Build an interactive grid display for showing all fonts in the system, a button to activate/deactivate them, and allow the user to create 'collections' within the library (like playlists in a music player) 

1.1 Scan for .otf/.ttf type font files in the filesystem and add them to the library

1.2 Import/Export: open .ufo.zip files using python and defcon and export/generate .otf and .ttf files with fontmake

1.3 Complete documentation and organising code if needed according to sugar labs Activity Teams mentioned specification 

Mock:

![Image of Complete Font display](https://raw.githubusercontent.com/sugarlabs/font-editor-activity/gh-pages/files/img/3.png)

#### Milestone 2: Glyph Editor Basic Version

2.0 Build the glyph picker class, to select which glyphs to edit

2.1 Build the glyph class and the methods required for manipulating it 

2.2 Implement PostScript bezier outline editing feature which will be similar to the Glyph editor currently found in [Trufont](https://github.com/trufont/trufont/releases/tag/0.2.0)

![Image of Glyph Editing Interface](https://raw.githubusercontent.com/sugarlabs/font-editor-activity/gh-pages/files/img/4.png)

#### Milestone 3: Metrics Integrated Glyph Editing View

3.0 A view as mentioned above which allow us to adjust spacing while in glyph edit mode 

3.1 Testing Stage/Paragraph View

3.2 This module will only show a text box in which the written text is rendered in the font currently being edited/created

3.3 There will not be any editing option in this module- this is just to get a visual feedback of the font in question

3.4 This module will also contain predefined text templates eg. "the quick brown fox jumps over the lazy dog"  and a export image button to save a image of the rendered font  

#### Milestone 4: Glyph Editor with Added Functionality 1

4.0 Implement spiro spline curve fitting as can be done with inkscape

#### Milestone 5: Glyph Editor with Added Functionality 2

5.0 Implement curve offsetting that will be used in skeleton based glyph design 

#### Milestone 6: Packaging

6.0 Get the code integrated in the main sugar distribution
