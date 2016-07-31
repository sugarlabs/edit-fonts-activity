---
layout: post
title: Welcome Page UX Concept
category: article
author: Eli Heuer
---
This is just an idea I had last night for improving the welcome screen UX, if it's too much work or Dave and Yash don't like it I understand. However, I may try to code it myself for fun if Yash doesn't have time. :-)

My fear is that when users start the Edit Fonts activity for the first time they will be be lost and not understand what to do. Some users might not even have a basic understand of what vector drawing is or how a font is made. This welcome screen will at least give the users a basic idea about how to use the activity. Most importantly, this makes the first screen visualy interesting, interactive and fun. Many users may not continue with the activity if the first page is dull and boring.

I'm proposing that the welcome screen have 4 options, represented by icons and text, plus an editable .glyph that reads "Edit Fonts" in the Geo typeface. The Edit-Fonts logotype will be one .glyph file that is only loaded and never saved. see below:

![UX concept 01](files/img/wireframe_concept_01_welcome_page.svg)
![UX concept 02](files/img/wireframe_concept_02_welcome_page.svg)

I have added a Geo-Regular.ufo file to the gh-pages repo with a special "editfonts.glyph" logotype:

[https://github.com/sugarlabs/edit-fonts-activity/tree/gh-pages/files/fonts/Geo-Regular.ufo](https://github.com/sugarlabs/edit-fonts-activity/tree/gh-pages/files/fonts/Geo-Regular.ufo)

![editfonts.glyph](files/img/wireframe_concept_welcome_page_03.png)

There are two neat things about this approach. First, it uses components we already have, the only work will be laying out the page, which Dave or I can attempt if Yash is too busy. Second, if the user never realizes that the edit fonts logotype is editable, it still functions as a logotype. A similar UX design pattern was used for the start screen of the game Super Mario 64, see below:

<iframe src="https://player.vimeo.com/video/74943170?title=0&byline=0&portrait=0" width="640" height="360" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>

[Mario 64 easter-egg](https://youtu.be/eBotFor1Xlw)
