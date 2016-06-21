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

1. repositioning existing points
2. adding new points to existing contours
3. removing points from a contour that 'breaks' an closed contour into an open one
4. 'merging' points, where they are removed from a closed contour without breaking it open
5. adding new points to make a new contour, a "pen tool." 

Perhaps the best primer on the 'pen tool' is the video made by John Warnock - one of the Adobe founders, who invented Adobe Illustrator 30 years ago - that was included in the very first version of Adobe Illustrator:

<iframe width="420" height="315" src="https://www.youtube-nocookie.com/embed/sAbjajnLZY0" frameborder="0" allowfullscreen></iframe>

<https://youtu.be/sAbjajnLZY0>

There are various ways of calculating Bezier splines, and some are much faster than others. 
[incolumitas.com/2013/10/06/plotting-bezier-curves](http://incolumitas.com/2013/10/06/plotting-bezier-curves) has sample Python code, [which is public domain](http://incolumitas.com/pages/impressum) and you can use freely. 

And of course the best resource for learning about Bezier code is [pomax.github.io/bezierinfo](http://pomax.github.io/bezierinfo/)

## What is needed for a v1.0 
 
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
