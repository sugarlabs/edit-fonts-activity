[![Build Status](https://travis-ci.org/sugarlabs/edit-fonts-activity.svg?branch=master)](https://travis-ci.org/sugarlabs/edit-fonts-activity)

# Sugar Activity: Edit Fonts Activity

Live Site: <http://sugarlabs.github.io/edit-fonts-activity/>

Typeface design is a cornerstone of literate cultures, with subliminal power: Typefaces carry the emotions of texts, from formal designs that speak with authority to fun designs that are silly or military or ornate. They are both artistic and functional works, and our ability to share and modify them is important for the same reasons as for software programs.

Sugar is a learning platform that reinvents how computers are used for education. Collaboration, reflection, and discovery are integrated directly into the user interface, and “studio thinking” and “reflective practice” are promoted through Sugar’s clarity of design. Sugar was initially developed by Red Hat and Pentagram with One Laptop per Child, and today is developed by the Sugar Labs community. It now has over 1M users, including every child in Uruguay.

Fonts are fun to make, and Sugar needs a font editor activity so learners can make and modify them for their own tastes and needs.


## To keep up with latest updates check out the following:

* [Week 1 Work](https://sugarlabs.github.io/edit-fonts-activity/week-1-work)
* [Week 2+3 Work](https://sugarlabs.github.io/edit-fonts-activity/week-3-work)
* [Week 4 Work](https://sugarlabs.github.io/edit-fonts-activity/week-4-work)
* [Week 5 Work](https://sugarlabs.github.io/edit-fonts-activity/week-5-work)
* [Week 6 Work](https://sugarlabs.github.io/edit-fonts-activity/week-6-work)


## Following is the feature list of the application:

### Font Manager
---
* [ ] Convert .ttf to .ufo
	*	[x] Load a ttf file if file path is hardcoded
	*	[x] Load a ttf using the Object Chooser Dialog
	*	[ ] Load a ttf using font description from Gtk Pango Context
* [ ] Convert .ufo to .ttf using fontmake
	* [x] test this outside sugar
	* [ ] working inside sugar
* [ ] export .ttf file
	* requires conversion of .ufo to .ttf
	* [ ] save the file as a user given path
* [x] Show all the available fonts found in the system font directory
* [ ] Allow the user to Activate/Deactivate fonts
	* [x] Build Activate/Deactivate/Lock buttons
	* [x] enable state change of click
	* [x] show the buttons only if the font is selected in the font manager
	* [ ] update the installed fonts list after the activation or deactivation of a font (issue)
	* [x] Add attribute to font object stating Deactivated or Activated
	* [ ] Write provisions that a font cannot be Deactivated and Favorite simultanously
	* [ ] Mark the font as *DISABLED*
* [x] General text string preview for all fonts
  * [x] Add a text box in the top center where the user can write a text and all the fonts will render that particular string --No button click needed
    * [x] Take and store the text string every time the textbox text is changed
	* [x] Update the fontList view with the new string
* [x] Allow the user to mark certain fonts as Favorites
	* [x] Add attribute to font object stating favorite
	* [x] Mark the star next to the font as *COLORED*
	  * [x] when the font_star is clicked
	    * [x] Add the font to the favorite list
		* [x] Save the changes to the main file
	* [ ] Make a favorite/all switcher button
      * [x] Figure out the UI/UX
      * [ ] when clicked this will be toggle the font filter in the fontList View
* [ ] Allow to user to make 'collections' within the library
	* [ ] Add attribute to font object stating collection name
* [ ] Convert .ufo to .otf and viceversa
	* done when the .ttf version is done
* [ ] save .otf file
	* done when the .ttf version is done

### A Glyph Editing interface together with text preview
---

* [ ] Load a .ufo file
	* [x] can do so if the ufo file path is hardcoded
	* [ ] can do so if the ufo file path is choosen by the Object Chooser Dialog
* [ ] Save .ufo file
	* [x] plainly save the .ufo file at a hardcoded position
	* [ ] exporting a journal entry with a file_path to the saved ufo
* [x] Character Map
	* [x] Display the font info button (i)
		* [x] clicking on this opens the font info page
	* [x] Make a grid dipslay that makes a required number of boxes and is scrollable
	* [x] Make the Glyph Rendering class that shows the glyphs in these boxes
	* [x] if the glyphs are clicked open the glyph editing interface
	* [ ] add glyph button
* [ ] Basic Glyph editing interface
	* [ ] Make a drawing canvas on which the Glyph will be displayed as an outline
		* [x] Display the points and offcurve points
		* [x] User can move around points
			* [x] How can the user move around small circles ?
		* [ ] The offcurve points for a curve with the smooth set as yes will stay collinear
* [ ] Font Info Page
	* [x] Define the main info which will be in scope of this activity
	* [ ] Allow the user to edit this info
* [ ] Multi Glyph editing interface
* [ ] Basic Curve Offsetting- Glyph editing interface
* [ ] Caps Curve Offsetting- Glyph editing interface

### A Testing interface for the Font Manager
---
* [ ] A separate more functional testing screen will be made apart from the live preview box.
* [ ] A textbox in which the text is rendered using the font, to get visual feedback.
* [ ] Provide predefined text templates eg. "the quick brown fox jumps over the lazy dog," and
* [ ] Export image button, to save an image of the rendered textbox


