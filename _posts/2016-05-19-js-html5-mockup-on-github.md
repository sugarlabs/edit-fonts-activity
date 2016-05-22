---
layout: post
title: My JS/HTML5 Mock-up is on GitHub
category: article
author: Eli Heuer
---

The JS/HTML5 mock-up I'm working on is now [live on GitHub here,](https://sugarlabs.github.io/edit-fonts-activity/mockups/EditFontsMockUpJS.activity/) screenshot of my GNOME/Fedora development workspace below:

![Eli's JS Mockup WIP 001](files/img/elis_js_mockup_wip_001.png)

I'll be updating this until our next meeting on Friday, trying out different layouts and doing some basic interactivity/animation.

To run the mock-up, clone Sugarizer like so:

`git clone https://github.com/llaske/sugarizer.git`

Then clone my mock-up into the Sugarizer activities folder:

`cd ~/path/to/sugarizer/activities/`

`git clone https://github.com/eliheuer/EditFontsMockUpJS.activity.git`

Update the file activities.json of the Sugarizer directory: add a new line for your activity. Update id, name and directory values on this new line:

`{"id": "org.sugarlabs.EditFontsMockUpJS", "name": "Edit Fonts Mock Up JS", "version": 1, "directory": "activities/EditFontsMockUpJS.activity", "icon": "activity/activity-icon.svg", "favorite": true, "activityId": null},`

To run Sugarizer on your PC (GNU Linux/Mac OS/Windows), close any running instances of Chrome and re-launch it using the command line:

`chrome --allow-file-access-from-files index.html`

In the below screenshot(GNU Nano on the right) I have set a bash alias so I just type `xo` from anywhere in the terminal to launch sugarizer:

`alias xo="google-chrome --allow-file-access-from-files ~/gsoc/sugarizer/index.html"`

![Eli's bashrc setup](files/img/elis_sugarizer_setup.png)
