# Sugar GSoC 2016 Proposal

*A complete end to end Font Editor Activity for Sugar*

### About Me

1. Name: Yash Agarwal
2. Email: [agrwal.ysh94@gmail.com](mailto:agrwal.ysh94@gmail.com), [yash.agarwal@iitb.ac.in](mailto:yash.agarwal@iitb.ac.in) 
3. Telephone: (+91) 9167470511
4. Country of Residence: India (GMT +0530)
5. IRC nickname: yagarwal (on [webchat.freenode.net](http://irc.freenode.net/))
6. Primary Language: English
7. Why Open Source: I am currently working on 2 projects that will be made open source on completion. I was initiated with FOSS development late last year when I started working on my Mtech thesis and am having an amazing time since then :-). 
8. *This line from [fsf](http://www.fsf.org/)* answers this better than anything I can write: *Free software developers guarantee everyone equal rights to their programs; any user can study the source code, modify it, and share the program. By contrast, most software carries fine print that denies users these basic rights, leaving them susceptible to the whims of its owners and vulnerable to surveillance.    
9. Github: [https://github.com/YashAgarwal/](https://github.com/YashAgarwal/)
10. My resume: [http://home.iitb.ac.in/~yash.agarwal/resume.pdf](http://home.iitb.ac.in/~yash.agarwal/resume.pdf) 

### About the project

Project Name: A complete end to end *Font Editor Activity* for Sugar	

Typeface design is a cornerstone of literate cultures, with subliminal power: Typefaces carry the emotions of texts, from formal designs that speak with authority to fun designs that are silly or military or ornate. They are both artistic and functional works, and our ability to share and modify them is important for the same reasons as for software programs. A Sugar font editor activity will empower users to create and modify fonts for their own tastes and needs. Fonts are fun to make, but we need an editor to do it.

This project's main goal is to develop an end to end font editor activity for Sugar with features/functions picked from the most popular tools in the market like [Glyphr](http://glyphrstudio.com/), [Trufont](https://github.com/trufont/trufont/releases/tag/0.2.0), [FontForge](https://fontforge.github.io/), etc.

Sugar allows us 2 ways of making a Activity. I can use either Python/GTK+ 3 or Sugarizer (HTML/Js) to create the activity. I am very comfortable with both the frameworks and can go ahead with any of them if the people at sugar have some preferences regarding the development environment. Currently this proposal is made choosing Sugarizer as the development environment as I consider myself to be more comfortable with Web based system than GTK.

You can check out the "Hello World" activity developed for both the frameworks [here](https://github.com/YashAgarwal/gsoc_sugarLabs) [a [sreenshot](https://drive.google.com/file/d/0B8JA87tMmJ87Zk5IVVRjbTRhZVk/view?usp=sharing) showing a sample web activity]. The font editor created in this will be very similar to [Trufont](https://github.com/trufont/trufont/releases/tag/0.2.0) plus/minus a few features explained below.

This Font editor will have the following features (planned as of now):	

1. [Sugar Human Interface Guidelines](https://wiki.sugarlabs.org/go/Human_Interface_Guidelines) based UI	
2. Font Manager Activity that will show all the available fonts found in the system font directory and allow the user to install/uninstall fonts [ref [#1](https://wiki.sugarlabs.org/go/The_Undiscoverable/Fonts),[#2](http://wiki.laptop.org/go/Font_considerations)]	
3. A glyph editing interface similar to the one found in [glyphsapp.com](https://glyphsapp.com/), so that you are editing glyph outlines in the same window as you space them.	
4. A Testing stage where we can show a textbox in which the written text is rendered in the loaded font to get a visual feedback of the font in question. This module will also contain predefined text templates eg. "the quick brown fox jumps over the lazy dog" and a export image button to save an image of the rendered font	
5. All this will be accompanied with thorough documentation and commenting which will be done hand in hand with development as it clarity in the end goals	
6. These 	are very broad descriptions of the major features and further details will be discussed with Dave Crossland

The project if made using Sugarizer will use HTML5/CSS3 and will have lot of dependencies on major JavaScript libraries

Dependencies:

1. [jQuery.js](https://jquery.com/download/)
2. [Angular.js](https://angularjs.org/)  &  [Angular-ui.js](https://angular-ui.github.io/)
3. [UFO.js](http://lib.ufojs.org/)
4. [opentype.js](https://github.com/nodebox/opentype.js)
5. [d3.js](https://d3js.org/) 	 		

### *Timeline* 	 	

___I have divided the project into measurable Milestones :12 weeks, 40 hours a week. 6 milestones of 2 weeks each.___

#### Milestone 1

1. Basic UI Boilerplate design
    1.  Will use the [Sugar Human Interface Guidelines](https://wiki.sugarlabs.org/go/Human_Interface_Guidelines) to build basic GUI functionality like:
        1. Toolbar(s)
        2. Navbar 
        3. Work Space, etc.
    2. The entire activity will be made as a [SPA](https://en.wikipedia.org/wiki/Single-page_application) (single page web app) using [Angular.js](https://angularjs.org/) in the Sugarizer DE which gives us browser like playfield 
2. Font Import/Export Library 
    1. The Activity will import .ufo.zip files using ufo playfieldJS, and as a stretch goal, .otf/.ttf type font file using  [opentype.js](https://github.com/nodebox/opentype.js)
    2. Convert to Postscript based bezier curve data
    3. The Activity will export .otf. This will be done using [opentype.js](https://github.com/nodebox/opentype.js)
    4. Build an interactive grid display for showing the loaded font data similar to the one displayed below from [Trufont](https://github.com/trufont/trufont/releases/tag/0.2.0) 
3. Font Manager Activity 
    1. The Activity will scan for and import all .otf/.ttf type font files from the font directory of the system  
    2. This will allow the user to add/delete font files from the system

#### Milestone 2

1. Glyph Editor Basic Version
    1. Build the glyph class and the methods required for manipulating it 
    2. Implement PostScript bezier outline editing feature which will be similar to the Glyph editor currently found in [Trufont](https://github.com/trufont/trufont/releases/tag/0.2.0)
    3. d3.js will be used for visualising the nodes and connections for the bezier curves

#### Milestone 3

1. Metrics Integrated Glyph Editing View
    1. A view as mentioned above which allow us to adjust spacing while in glyph edit mode 
2. Testing Stage/Paragraph View
    1. This module will only show a text box in which the written text is rendered in the font currently being edited/created
    2. There will not be any editing option in this module- this is just to get a visual feedback of the font in question
    3. This module will also contain predefined text templates eg. "the quick brown fox jumps over the lazy dog"  and a export image button to save a image of the rendered font  

#### Milestone 4 & Milestone 5

1. Glyph Editor with Added Functionality (this will be subject to the response of the community on the activity developed prior to this milestone)
    1. Implement spiro spline curve fitting as can be done with inkscape
    2. Implement curve offsetting that will be used in skeleton based glyph design 

#### Milestone 6

1. Complete documentation and organising code if needed according to sugar labs Activity Teams mentioned specification
2. Getting the code integrated in the main sugar distro

###Why me
I am a 4th year dual degree student pursuing B.Tech. + M.Tech. in Metallurgical Engineering & Material Engineering at Indian Institute of Technology, Bombay. My semester will end in late April leaving me enough time to get ready for my GSoC project. If I am selected, I shall be able to work around 40 hrs a week on the project, though I am open to putting in more effort if the work requires. My main Intrest in my major has been in Computational Material Science in which I have developed Simulations of numerous Phase field/Stochastic Models in C,C++ and Python ([git repo](https://github.com/YashAgarwal/Phase-Field-Theory)). MyMasters thesis involves the development of a Open Source library for Maximization of Corrosion Resistance for free form surfaces.

Since 7th standard, when my dad introduced to Photoshop I have been very interested in graphic design and I realise the role typefaces plays in any design process to convey the right message. Typeface design is specialised field in Graphic Design and has really aroused my interest in it. Human beings are expressive creatures and Typefaces are integral to a expressing our emotions in a written message as Tone and Pitch are in a Vocal message. I think working with sugar Labs this summer for creating a font editor will be great learning experience for me and a chance for contributing to a bigger cause (OLPC mission).

I am working on a Angular.js based web app which will also be made opensource ([git repo](https://github.com/YashAgarwal/tdsl-app)) as part of my elective course under CTARA, IITB ([ http://www.ctara.iitb.ac.in/](http://www.ctara.iitb.ac.in/) ). This application will be focusing on developing a data based platform to assist NGO workers in tackling the problem of Malnutrition in India. This web app will be compiled using Cordova ([ https://cordova.apache.org/](https://cordova.apache.org/) ) so that It can run on any mobile based platform. This app will be completed before April begins.

I became interested in Web tech about a year back and since then I have been tinkering with various open source technologies which has only led to increasing my interest in web tech. I have experience and a good working knowledge of all the js libraries mentioned in the dependencies except opentype.js and ufo.js which I went through briefly and will form a thorough understanding in early May when Summer vacation starts before the first phase begins. 

I am currently a part of AUV-IITB(auv-iitb.org) a student run organisation which is building an AUV, as a part of this project I have managed a team of 8 people for the development of the embedded software stack through which I have learnt a lot about version control, build systems, system administration, coding practices in the industry, as well as working in collaboration on an ill-defined goal and following tight deadlines.

I am at ease with Git and the Linux (only Ubuntu, Fedora) operating system which will be required for this project. I also understand the importance of giving testing and commenting a significant amount of time of the project.

I don't have a personal website, but I am ready to provide more details via any of the communication channels mentioned above.

###Me and the Community

In my 4 years at IIT, Bombay I have learned to tackle any problem/project systematically and plan it out in advance and using the resources in my hand effectively. I believe in trying and figuring things out on my own and true learning happens when you do something yourself. If Dave is not able to contribute due to some reason I will try to leverage the help from my wide network of colleagues in IITB and of course the vibrant and rich sugar community. I will work towards finishing the project based on the latest inputs I got from Dave and make necessary assumption intelligently.

I’ll keep all work done regarding this project on git and maintain a working copy of the code after every feature addition. Thus the community will be able to see a working activity of the at all major milestones and reach me using the above mentioned contact information or on github itself to notify me any suggestions, comments.

Apart from all this the sugar community believes that this activity should be developed using Python/GTK+ 3, I am willing to submit an additional proposal regarding giving alternatives for the Js dependencies I have mentioned above.

Category: 2016 GSoC applications

