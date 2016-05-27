---
layout: post
title: My Progess so far
category: article
author: Yash Agarwal
---

As Thomas Edison once said:

> I have not failed. 
> I've just found 10,000 ways that won't work.

Well, I haven't tried it 10,000 times, but have definitely found a lot of ways that things didn't work as I expected, during this community bonding phase.

I have read through the following links relevant to this GSoC - and more! 
As this not an exhaustive list, because I changed my machine recently... 
As a history dump it contains some less-relevant and not-project-specific links that I found relevant in some way:

* <https://guides.github.com/features/mastering-markdown/>
* <https://python-gtk-3-tutorial.readthedocs.io/en/latest/>
* <http://www.robodocs.info/roboFabDocs/source/index.html>
* <http://stackoverflow.com/questions/29866592/draw-a-plot-of-glyphs-in-matplotlib>
* <http://www.drawbot.com/>
* <https://github.com/mlagerberg/FindThatFont->
* <http://lib.ufojs.org/>
* <http://unifiedfontobject.org/versions/ufo3/index.html>
* <https://blog.codinghorror.com/learn-to-read-the-source-luke/>
* <http://www.glyphrstudio.com/online/>
* <https://github.com/mattlag/Glyphr-Studio>
* <http://ts-defcon.readthedocs.io/en/latest/index.html>
* <https://github.com/adrientetar/defconQt>
* <https://trufont.github.io/>
* <http://victorlin.me/posts/2013/09/19/fall-in-love-with-continuous-testing-and-integration-travis-ci>
* <https://wiki.sugarlabs.org/go/Activity_Team/Sample_code/Ruler>
* <http://git.sugarlabs.org/projects/hello-world>
* <http://wiki.laptop.org/go/Developers/FAQ>
* <http://wiki.laptop.org/go/Sugar_Activity_Tutorial>
* <http://en.flossmanuals.net/make-your-own-sugar-activities/>
* <https://wiki.sugarlabs.org/go/Development_Team/Almanac>
* <http://www.tortall.net/mu/wiki/CairoTutorial>
* <https://wiki.sugarlabs.org/go/Activity_Team/Creating_a_New_Activity>
* <https://wiki.sugarlabs.org/go/Activity_Team/Modifing_an_Activity>
* <http://activities.sugarlabs.org/en-US/sugar/addon/4050>

As you may have noticed that there is debate going on the #sugar-meeting chanel on whether to use JS/HTML or Python/GTK to develop this activity. 
Also a 3rd way is to use Python Backend with Web UI suggested, by Dave.

The following is a try of the JS/HTML version of the app I started going through, with [ufoJS](http://lib.ufojs.org/) where I tried implementing the sample [glif-renderer](http://lib.ufojs.org/env/glif-renderer.xhtml) in hopes that I can hack it and make it display a Character Map. 
I faced some [issues](https://github.com/graphicore/ufoJS/issues/67) with **require.js** which were later solved with [Lasse Fister's](https://github.com/graphicore) help. 
The Character Map is still to be checked into Github. 

Then I tried making a Python/GTK stand-alone verision of the same character map, and ran into issues in drawing the glyphs with defcon. 
I emailed [Adrién Tetar](https://github.com/adrientetar) regarding it, but I'm yet to receive a reply.
This is what I have made so far:
[Python/GTK Mock](https://github.com/sugarlabs/edit-fonts-activity/tree/gh-pages/mockups/pyGtkMock)

Here is a screenshot for it:

![screenshot of pyGtkMokc](mockups/pyGtkMock/pic.png)

In the last IRC meeting we discussed the platform issue, and figured out the right way to move forward is with Sugar Desktop.
