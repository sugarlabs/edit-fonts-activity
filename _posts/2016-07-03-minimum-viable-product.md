---
layout: post
title: Redefining a Minimum Viable Product
category: article
author: Dave Crossland
---

I spoke to Yash on IM and he's suffered a hardware failure over the weekend so he's slipped a few days. 

Going into Week 7 today, I am worried that we now have a bunch of stuff that is half done, but the [core user story](core-user-story) still isn't realised. 

I want to get the development to the point where users can actually do something useful - even if it is very simple and limited - and then have the development structured for iteratation. We can make the product definition smaller and smaller but still wide enough to cover the core user story process. Then when we have something people can use productively, we can survey the whole project and look at the weakest parts and decide on priorities. 

I suggest Yash focuses on the early part of core user story process: we need to be able to make a new font, add glyphs to it, and then add contours to those glyphs, and set their sidebearings. 

* To simplify creating a new font, hardcode it with [these 101 glyphs](https://github.com/google/fonts/blob/master/tools/encodings/latin_unique-glyphs.nam#L3-L103) and forget about adding arbitrary new glyphs. 

* To simplify the add contours part, let's forget curves for now, and just allow for straight lines only; then we can make fonts likehttp://fonts.google.com/specimen/Geo

* To simplify sidebearings just set them all to 600, and forget about editing them. 

Then, the user can make a new font, draw a some squarish letters in a monospaced design, and use their font in the write activity. 

Once that works, I suggest to halt writing new code and work on the code documentation, and the .xo packaging, the travis build checking, and other 'non code' development tasks. 
