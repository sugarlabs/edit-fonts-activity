# Edit Fonts Activity

A font editor Activity, for GSoC16 project: https://github.com/sugarlabs/edit-fonts-activity

##New Features

* Normalised the glyph drawing code
* Made a renderGlyph Class for drawing the glyph inside a specified box size
* Made a glyphGridInstance Class for drawing a grid of glyph from a given list
* Glyph aspect ratio problem solved
* Character Map class added

##Character Map Class
This class makes a character map of the specified font
the following are the ways to use it

#Multi Row Button Type Navigation

you can use it like this `#CharacterMap = characterMap(font, 15, 10, 'BUTTON')` where `15` is the number of **Columns** and `10` is the number of **Rows**

![pic](button_demo.gif)

#Single Row Button Type Navigation

you can use it like this `#CharacterMap = characterMap(font, 15, 1, 'BUTTON')` by just putting number of Rows to `1` 

![pic](button_singleline_demo.gif)

#Multi Row Scroll Type Navigation

you can use it like this `#CharacterMap = characterMap(font, 15, 10, 'SCROLL')` where `15` is the number of **Columns** and the number of **Rows** is ignored and all the available vertical space is given to the widget

![pic](scroll_demo.gif)
