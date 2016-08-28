[![Build Status](https://travis-ci.org/sugarlabs/edit-fonts-activity.svg?branch=master)](https://travis-ci.org/sugarlabs/edit-fonts-activity)

[![Documentation Status](https://readthedocs.org/projects/edit-fonts-activity/badge/?version=latest)](http://edit-fonts-activity.readthedocs.io/en/latest/?badge=latest)

# Sugar Activity: Edit Fonts Activity

Project Blog: <http://sugarlabs.github.io/edit-fonts-activity/>
Project Documentation: <http://edit-fonts-activity.rtfd.io>

Typeface design is a cornerstone of literate cultures, with subliminal power: 
Typefaces carry the emotions of texts, from formal designs that speak with authority to fun designs that are silly or military or ornate.
They are both artistic and functional works, and our ability to share and modify them is important for the same reasons as for software programs.

Sugar is a learning platform that reinvents how computers are used for education. 
Collaboration, reflection, and discovery are integrated directly into the user interface, and “studio thinking” and “reflective practice” are promoted through Sugar’s clarity of design. 
Sugar was initially developed by Red Hat and Pentagram with One Laptop per Child, and today is developed by the Sugar Labs community. 
It now has over 1M users, including every child in Uruguay.

Fonts are fun to make, and Sugar needs a font editor activity so learners can make and modify them for their own tastes and needs.

The feature list of the application is documented on the project blog. 

## Usage

Download this repo to a Sugar desktop and set it up, then launch it from the Home screen. 

    # boot Fedora-Live-SoaS-x86_64-23-10.iso
    sudo dnf install git -y;
    git clone https://github.com/sugarlabs/edit-fonts-activity.git;
    cd edit-fonts-activity;
    python setup.py dev
    # go to home, list view, search Fonts

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

[GPLv3](LICENSE.txt)
