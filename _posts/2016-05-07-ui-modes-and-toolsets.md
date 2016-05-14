---
layout: post
title: UI Concepts—Modes and Toolsets
category: article
author: Eli Heuer
---

Sugar Activities are intended to be "low floor, no ceiling". 
The [Sugar Human Interface Guidelines](https://wiki.sugarlabs.org/go/Human_Interface_Guidelines) explain this principle:

> "Low floor, no ceiling: this mantra should guide your development efforts for OLPC. 
> All activities and interfaces should be designed in such a way as to be simple and intuitive to users of all age groups, nationalities, and levels of computer experience. 
> At the same time, we don't wish to impose unnecessary limitations on the software either. 
> Instead, we hope to create a platform suitable for all kinds of creative expression which provides a low floor to the inexperienced, but doesn't impose a ceiling upon those who are. 
> This is a worthy goal, but will require a genuine effort on the part of developers, who must take many aspects of design into account."

There are some activities for Sugar that I feel succeed in the LF/NC goal. 
Particularly I like:

* [Colors](http://activities.sugarlabs.org/en-US/sugar/addon/4050)
* [TamTamJam](http://activities.sugarlabs.org/en-US/sugar/addon/4060)

Beyond Sugar, there are two drawing programs I would like to look at and borrow UI patterns from, because I feel they are very LF/NC:

* [MarioPaint](https://en.wikipedia.org/wiki/Mario_Paint), for SNES (with a [live Flash version](http://www.playretrogames.com/3031-super-mario-paint)
* [Kid Pix](https://en.wikipedia.org/wiki/Kid_Pix), for Mac Plus (with a [live JS version](https://jamesfriend.com.au/pce-js/))

Both programs use a UI design pattern I'll refer to as "mode/toolset." 
Software that uses this pattern have two toolbars, sets of icons at opposite ends or along different edges of the screen. 
One toolbar sets the mode and the other toolbar changes to only give you tools you need to accomplish the task at hand in the selected mode. 
The advantages include:

* New users only see a small number of tools on screen, so they are not overwhelmed by choice;
* The default mode can be carefully designed to get users seeing results right away;
* Users are less likely to select a tool that doesn't work and gives them no result, because the tools available within 1 click all relate to the task at hand and only that task;
* By grouping tools into modes, users can accurately guess what a tool does.

Let's look at MarioPaint.
I note that the mode toolbar is on the bottom and the toolset toolbar is on the top of the screen. 
Also, some items on the mode toolbar are single purpose and only do one thing without having a toolset:

<iframe width="420" height="315" src="https://www.youtube-nocookie.com/embed/z99vk2qB-lo" frameborder="0" allowfullscreen></iframe>

Kid Pix instead has the mode toolbar on the left and the toolset toolbar on the bottom.
Here is v2, with color and sound:

<iframe width="420" height="315" src="https://www.youtube-nocookie.com/embed/bJnelIxC6gM" frameborder="0" allowfullscreen></iframe>

Here is a UI wireframe of what mode/toolset could look like for a font editing Sugar Activity.
This is made with Inkscape and is the source SVG if you want to make your own versions :) 
I'll expand on this idea more in my next blog post. 

![wireframe of the 'Workspaces and Toolsets' UI concept ](files/img/wireframe_concept_01_basic.svg)
