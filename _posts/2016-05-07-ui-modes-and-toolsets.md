---
layout: post
title: UI Concepts—Modes and Toolsets
category: article
author: Eli Heuer
---

Sugar activities are intended to be "low floor, no ceiling". The [HIG](http://wiki.laptop.org/go/OLPC_Human_Interface_Guidelines) explains:

>"Low floor, no ceiling: this mantra should guide your development efforts for OLPC. All activities and interfaces should be designed in such a way as to be simple and intuitive to users of all age groups, nationalities, and levels of computer experience. At the same time, we don't wish to impose unnecessary limitations on the software either. Instead, we hope to create a platform suitable for all kinds of creative expression which provides a low floor to the inexperienced, but doesn't impose a ceiling upon those who are. This is a worthy goal, but will require a genuine effort on the part of developers, who must take many aspects of design into account."

There are some activities for Sugar that I feel succeed in the LF,NC goal, particularly I like:

* Colors
* TamTamJam

Beyond the OLPC/Sugar project, there are two drawing  programs I would like to look at and borrow UI patterns from, they are:

* MarioPaint (SNES)
* Kid Pix (Mac Plus)

Both programs use a UI design pattern I'll refer to as mode/toolset strategy. Software that uses this pattern will have two toolbars or sets of icons, usually at opposite ends of the screen. One toolbar sets the 'mode' and the other toolbar changes to only give you tools you need to accomplish the task at hand in the selected mode. This has many advantages, mainly:

* New Users only see a small number of tools on screen and aren't overwhelmed by choice. 
* The default mode can be carefully designed to get users seeing results right away. 
* Because the tools on the screen only relate to the task at hand, the user will be less likely to select a tool that doesn't work and gives them no result.
* By grouping tools into modes it's easier for the user to guess what a tool does. 

Let's look at MarioPaint, note that the mode tool bar is on the bottom and the toolset toolbar is on the top. Also, some items on the mode toolbar are single purpose and only do one thing without having a toolset:

<iframe width="420" height="315" src="https://www.youtube.com/embed/z99vk2qB-lo" frameborder="0" allowfullscreen></iframe>

[Kid Pix](https://jamesfriend.com.au/pce-js/) is similar to MarioPaint but has the mode toolbar on the left and the toolset toolbar on the bottom of the screen. 

![Kid Pix!](http://i.imgur.com/jF1CZJf.jpg)

So, here is a UI wireframe of what that could look like for a Sugar font editor activity. I'll expand on this idea more in my next blog post. 

![wireframe of the 'Workspaces and Toolsets' UI concept ](files/img/wireframe_concept_01_basic.svg)
