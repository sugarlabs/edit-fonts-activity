---
layout: post
title: Detailed Feature and Task List
category: article
author: Yash Agarwal
---

* *This is a tentative list and will be updated regularly as more progress is made on the project*
* *This file contains elements like*

```
* Feature 1
	* mini feature
	* task 1 required to implement the feature
		* subtask 1  
	* task 2
* Feature 2
	* task 1
```

### A Glyph Editing interface together with text preview

##### Priority 1

* Load a .ufo file
* Save .ufo file
* Character Map
	* Display the font info button (i)
		* clicking on this opens the font info page
	* Make a grid dipslay that makes a required number of boxes and is scrollable
	* Make the Glyph Rendering class that shows the glyphs in these boxes
	* if the glyphs are clicked open the glyph editing interface
	* add glyph button
* Basic Glyph editing interface
	* Make a drawing canvas on which the Glyph will be displayed as an outline
		* Display the points and offcurve points
		* User can move around points
			* How can the user move around small circles ?
		* The offcurve points for a curve with the smooth set as yes will stay collinear    	 
* Font Info Page
	* Define the main info which will be in scope of this activity
	* Allow the user to edit this info	 


##### Priority 2
* Multi Glyph editing interface
* Basic Curve Offsetting- Glyph editing interface
* Caps Curve Offsetting- Glyph editing interface

### Font Manager

##### Priority 1

* Convert .ttf to .ufo
* Convert .ufo to .ttf
* save .ttf file
* Show all the available fonts found in the system font directory
* Allow the user to Activate/Deactivate fonts
* General text string preview for all fonts
  * Add a text box in the top center where the user can write a text and all the fonts will render that particular string --No button click needed
    * Take and store the text string every time the textbox text is changed
	* Update the fontList view with the new string  	 	
* Allow the user to mark certain fonts as Favorites
	* Add attribute to font object stating favorite
	* Mark the star next to the font as *COLORED*
	  * when the font_star is clicked
	    * Add the font to the favorite list
		* Save the changes to the main file
	* Make a favorite/all switcher button
      * Figure out the UI/UX
      * when clicked this will be toggle the font filter in the fontList View
* Deactivate/Activate fonts
	* Add attribute to font object stating Deactivated or Activated
	* Write provisions that a font cannot be Deactivated and Favorite simultanously
	* Mark the font as *DISABLED*
	  * Figure out the UI/UX
	* Make a deactivated/activated switcher button
      * Figure out the UI/UX
      * when clicked this will be toggle the font filter in the fontList View

##### Priority 2
* Allow to user to make 'collections' within the library
	* Add attribute to font object stating collection name
* Convert .ufo to .otf and viceversa
* save .otf file

### A Testing interface for the Font Manager

* A separate more functional testing screen will be made apart from the live preview box.
* A textbox in which the text is rendered using the font, to get visual feedback.
* Provide predefined text templates eg. "the quick brown fox jumps over the lazy dog," and
* Export image button, to save an image of the rendered textbox
