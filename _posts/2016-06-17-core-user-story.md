---
layout: post
title: The core Font Editor User Story
category: article
author: Dave Crossland
---

(Reposted from the sugar-devel list)

I think Yash's main job for the next week is to make the core methods work: new, load, save, import, export. 
These are around 90% at this moment and I expect Yash will nail them this weekend. 

Once they are working well, then I suggest Yash moves on to the core methods needed to edit a glyph: 
editing the points is half of that, and editing the sidebearings is the other half. 
Probably sidebearings is the easier one!

For editing points, there is

1. adding new points to make a new contour (a "pen tool")
2. repositioning existing points
3. adding new points to existing contours
4. removing points from a contour that 'breaks' an closed contour into an open one
5. 'merging' points, where they are removed from a closed contour without breaking it open
 
Imagine you are using it for the first time... 
What are the essential things that you do?
That is the "core" [User Story](https://en.wikipedia.org/wiki/User_story)...
Something like this:
 
* You need to make a new font, 
* add some glyphs, 
* add some contours to those glyphs, 
* move their points around and set their sidebearings, 
* save your work in a UFO, 
* export your font as a OTF, 
* install the OTF in the system, 
* and use it in another activity. 

When you can do that, you'll have a v1.0 :)
