---
layout: post
title: Latest Proposal and Timeline
category: article
author: Yash Agarwal
---

This a tentative copy and will be revised over the weekend

So we have finally decided to move on with the work and use Python/Gtk 3 for making this font editor activity.
Now using Python allows me to take advantage of libraries like [defcon](https://github.com/typesupply/defcon), [glyphLib](https://github.com/googlei18n/glyphsLib) and many more mentioned here in [Dave's Reading List](https://sugarlabs.github.io/edit-fonts-activity/required-reading) 
One great example is [Trufont](https://github.com/trufont/trufont/), a python based libre font editor, which harnesses some of the above mentioned Libraries.

### Feature List

This font editor Activity is planned to include the following features and follow the [Sugar Human Interface Guidelines](https://wiki.sugarlabs.org/go/Human_Interface_Guidelines):
The activity will be following the mode/toolbar UX design as summarized by Dave [here](https://sugarlabs.github.io/edit-fonts-activity/ui-modes-and-toolsets). Here a primary toolbar will show the different modes and changing the mode will switch the workspace and the secondary toolbar accordingly.

#### 1: Font Manager

* Show all the available fonts found in the system font directory
* Allow the user to install/uninstall fonts
* Allow to user to make 'collections' within the library
* * **TODO:** a bit more discussion is required on this front in defining what unistalling/installing fonts and making the 'collections' mean*

#### 2: A glyph editing interface together with text preview

* a canvas where the user can insert glyphs in the editing workspace by selecting the glyphs from a character tool bar, here is a UI mockup for it made by Dave and Eli
* ![UI Mockup](files/img/wireframe_concept_01_basic_icons.svg)
* * **TODO:** The features/functionality of the glyph editing interface have to discussed upon in greater detail keeping the mind the scope and the target audience of this project*
* as it can be seen in the Mock-UI(above) this window will also contain a live preview box for live testing the font. 

#### 3: A Testing interface

* A separate more functional testing screen will be made apart from the live preview box.
* A textbox in which the text is rendered using the font, to get visual feedback. 
* Provide predefined text templates eg. "the quick brown fox jumps over the lazy dog," and 
* Export image button, to save an image of the rendered textbox
* *All this will be accompanied with thorough documentation, and...*
* *code commenting, which will be done hand in hand with development as we develope a better idea of the end goals*

### Timeline

I have divided the project into measurable milestones, with 12 weeks at 40 hours a week becoming 6 milestones of 2 weeks each:

#### Milestone 1: Font Manager

I will use the [Sugar Human Interface Guidelines](https://wiki.sugarlabs.org/go/Human_Interface_Guidelines) to build basic GUI functionality like Toolbar(s), Navbar , Work Space, etc.

The entire activity will be made as a Sugar Activity in Python.

Here a few more Mock-UI for the different screens/workspaces
![eli's mocks](files/img/wireframe_concept_01_modes.svg)

1.0 Activate/Deactivate: Build an interactive grid display for showing all fonts in the system, a button to activate/deactivate them, and allow the user to create 'collections' within the library (like playlists in a music player) 

1.1 Scan for .otf/.ttf type font files in the filesystem and add them to the library

1.2 Import/Export: open .ufo.zip files using python and defcon and export/generate .otf and .ttf files with fontmake

1.3 Complete documentation and organising code if needed according to sugar labs Activity Teams mentioned specification 

_**TODO:** Make a Mock-UI for this mode_
#### Milestone 2: Glyph Editor Basic Version

2.0 Build the glyph picker class, to select which glyphs to edit

2.1 Build the glyph class and the methods required for manipulating it 

2.2 Implement PostScript bezier outline editing feature which will be similar to the Glyph editor currently found in [Trufont](https://github.com/trufont/trufont/releases/tag/0.2.0)

![Image of Glyph Editing Interface](files/img/4.png)

*Time for mid way evaluation: I will finish the above 2 mentioned Milestones before the midway evaluation deadline 27th June. I may be requiring 4-5 days off(weekends are considered as regular working days) in between due to some unavoidable Academic Work during that period. This will not in anyway affect the project completion and the lost time will be compensated for in the weeks after it.* 

#### Milestone 3: The Multi Glyph editing screen together with an live preview feature (also an detailed testing mode)

3.0 This will include a canvas where the user can insert glyphs in the editing workspace by selecting the glyphs from a character tool bar, here is a UI mockup for it made by Dave and Eli
![UI Mockup](files/img/wireframe_concept_01_basic_icons.svg)

3.1 Detailed Testing Stage/Paragraph View

3.1.1 This module will only show a text box in which the written text is rendered in the font currently being edited/created

3.1.2 There will not be any editing option in this module- this is just to get a visual feedback of the font in question

3.1.3 This module will also contain predefined text templates eg. "the quick brown fox jumps over the lazy dog"  and a export image button to save a image of the rendered font 

#### Milestone 4: Glyph Editor with Added Functionality 1 + Packaging

4.0 Implement spiro spline curve fitting as can be done with inkscape

4.1 Get the code integrated in the main sugar distribution

#### Milestone 5: Glyph Editor with Added Functionality 2

5.0 Implement curve offsetting that will be used in skeleton based glyph design
here is [link](https://pomax.github.io/bezierinfo/#offsetting) describing this 

#### Milestone 6: Packing up things/Catching up with Backlogs/Detailed Documentation 

6.0 This period will act as a buffer time to manage any spillovers from the previous Milestones and for more detailed documentation.
