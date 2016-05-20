---
layout: post
title: My Progess so far
category: article
author: Yash Agarwal
---

As Thomas Edison once said:

> I have not failed. 
> I've just found 10,000 ways that won't work.

Well I haven't tried it 10000 times but have definitely found 'a lot' ways things *don't work* during this community bonding phase.

I have read through the following links relevant to this GSoC (not an exhaustive list as I changed my machine recently):
This is my history dump and so may contain some irrelevant/not project specific links

* https://guides.github.com/features/mastering-markdown/
* https://python-gtk-3-tutorial.readthedocs.io/en/latest/
* http://www.robodocs.info/roboFabDocs/source/index.html
* http://stackoverflow.com/questions/29866592/draw-a-plot-of-glyphs-in-matplotlib
* http://www.drawbot.com/
* https://github.com/mlagerberg/FindThatFont-
* http://lib.ufojs.org/
* http://unifiedfontobject.org/versions/ufo3/index.html
* https://blog.codinghorror.com/learn-to-read-the-source-luke/
* http://www.glyphrstudio.com/online/
* https://github.com/mattlag/Glyphr-Studio
* http://ts-defcon.readthedocs.io/en/latest/index.html
* https://github.com/adrientetar/defconQt
* https://trufont.github.io/
* http://victorlin.me/posts/2013/09/19/fall-in-love-with-continuous-testing-and-integration-travis-ci
* https://wiki.sugarlabs.org/go/Activity_Team/Sample_code/Ruler
* http://git.sugarlabs.org/projects/hello-world
* http://wiki.laptop.org/go/Developers/FAQ
* http://wiki.laptop.org/go/Sugar_Activity_Tutorial
* http://en.flossmanuals.net/make-your-own-sugar-activities/
* https://wiki.sugarlabs.org/go/Development_Team/Almanac
* http://www.tortall.net/mu/wiki/CairoTutorial ----imp
* https://wiki.sugarlabs.org/go/Activity_Team/Creating_a_New_Activity
* https://wiki.sugarlabs.org/go/Activity_Team/Modifing_an_Activity
* http://activities.sugarlabs.org/en-US/sugar/addon/4050

As you may have noticed that there is debate going on the #sugar-meeting chanel on whether to use JS/HTML or Python/GTK to develop this activity (also a 3rd way is to use Python Backend with Web UI suggested by Dave Crossland)

The following is a try of the JS/HTML version of the app
I started going through [ufoJS](http://lib.ufojs.org/) and tried implementing the sample [glif-renderer](http://lib.ufojs.org/env/glif-renderer.xhtml) in hopes that I can hack it and make it display character Map. I faced some [issues](https://github.com/graphicore/ufoJS/issues/67) with **require.js** which were later solved with [Lasse Fister's](https://github.com/graphicore) help. The character map is still to be made. 

Then I tried making a Python/GTK stanalone verision of the same character map and ran into issues in drawing the glyphs with defcon and have mailed [Adrien Teter](https://github.com/adrientetar) regarding it.(I'm yet to receive a reply)
this is what I have made so far:
[Python/GTK Mock](https://github.com/YashAgarwal/Python-GTK-Mock)

here is a screenshot for it:
![screenshot](https://raw.githubusercontent.com/YashAgarwal/Python-GTK-Mock/master/pic.png)

I Hope we can discuss this platform issue today and figure out the right way to move forward with this. 




