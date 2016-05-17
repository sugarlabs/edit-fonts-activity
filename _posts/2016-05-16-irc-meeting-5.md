---
layout: post
title: IRC Meeting 5, Python or JavaScript revisited
category: article
author: Dave Crossland
---

Today Dave, Eli, and Yash met on Google Hangouts On Air, and the video is at <http://youtu.be/CGc12VmPZps> and here:

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/CGc12VmPZps" frameborder="0" allowfullscreen></iframe>

The main topic of conversation was if we would indeed use Python to write a Sugar Desktop Activity, as I proposed in my [Python or JavaScript?](python-or-javascript-discussion) blog post.
We are still undecided about this. 

Last week this was the agenda:

* Go through [Dave's reading list](required-reading)
* Making a detailed task list for Milestone 1 in the [issue tracker](https://github.com/sugarlabs/edit-fonts-activity/milestones)
* Making a mock UI in PyGTK

Yash and Eli have been reading some of the things on the list, and both took a first attempt to make a mock UI with PyGTK. 
But both found it quite frustrating, and haven't posted anything yet. 

Meanwhile, over the last 8 weeks or so, there have been some exciting developments in the Glyphr Studio project. 
This project is a classical font editor, made in HTML/CSS/JS. 
The awesome UX designer-developer founder, Matt LaGrandeur, opened an issue announcing his intention to start a complete from-scratch rewrite, "Glyphr Studio 2," at <https://github.com/mattlag/Glyphr-Studio/issues/234>

Soon after, Matt and contributor Mateusz Zawartka started a "version 2 specifications" repo, <https://github.com/glyphr-studio/glyphr-studio-2-specs>, which I have been submitting comments to.
This progressed into a UI framework repo for prototyping in, <https://github.com/glyphr-studio/glyphr-studio-2-ui-framework>, and the current results can be played with here:

* <https://davelab6.github.io/glyphr-studio-2-ui-framework/dist/glyphedit.htm>
* <https://davelab6.github.io/glyphr-studio-2-ui-framework/dist/openproject.htm>
* <https://davelab6.github.io/glyphr-studio-2-ui-framework/dist/progress_spinner.htm>
* <https://davelab6.github.io/glyphr-studio-2-ui-framework/dist/settings.htm>

Coincidentally this topic was raised again in the [[GSOC] Font Editor Next Steps](http://lists.sugarlabs.org/archive/sugar-devel/2016-May/thread.html#52630) thread, by the excellent Sugarizer founder and OLPC France member Lionel Laské. 
[My reply](http://lists.sugarlabs.org/archive/sugar-devel/2016-May/052630.html) noted that both Eli and Yash already have web development skills, and with [sugar-web](https://github.com/sugarlabs/sugar-web) JS based activities can be distributed to Sugar Desktop users. 

Since the development of JS font editor libraries now matches the level of the python libraries (eg, for sources defcon is comparable to ufoJS, and for binaries fontTools is comparable to OpenType.js) then I don't see any strong reasons to prefer one technology or the other. 

My main concern is about the performance of sugar-web apps, especially on XO-1s. 

So Yash and Eli agreed to attempt to write an essential font editor widget (a glyph table) in both PyGTK3 and JS and then compare the experience, so we can make a decision based on his actual experience rather than a priori assumptions :)

I'm looking forward to trying the PyGTK widget out in the coming days :)
