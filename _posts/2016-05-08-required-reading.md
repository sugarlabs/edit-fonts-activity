---
layout: post
title: Required Reading for Writing a Modern Font Editor
category: article
author: Dave Crossland
---

I thought I'd put together a short introduction to the most relevant resources that anyone who wants to write a font editing program ought to become familiar with.

Any font editing program must be able to read and write fonts in at least 2 formats, a source format for editing, and a binary format for use.
Today the most common source and binary formats are UFO and OpenType. 

#### 1. The "UFO" Format

<http://unifiedfontobject.org>

The UFO format is a source format that is written to disk with the [XML](https://en.wikipedia.org/wiki/XML) and [p-list](https://en.wikipedia.org/wiki/Property_list) markup standards.  
XML probably needs no introduction, but the p-list format might be unfamiliar. 
It originated at Steve Jobs' NeXTStep company, and the NeXT operating system was rebranded as Mac OS X when Jobs returned to Apple in the late 90s. 
To become familiar with it, Apple's introduction is probably the best place to start: 

<https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/PropertyLists/Introduction/Introduction.html>

It is now at version 3, and the full details are here: 

UFOv3 Specification: <http://unifiedfontobject.org/versions/ufo3/>

The [UFO Authoring Tool Guidelines](http://unifiedfontobject.org/atguidelines) are also short but essential guidance for font editor authors. 

The format was initiated as a way of persisting data in the [RoboFab object model](http://robofab.org/objects/model.html) to disk, so reading the RoboFab documentation is well worth your time:

[![robofab objects map](files/third_party/robofab-objects.png)](http://robofab.org/objects/model.html)

#### 2. The defcon Library

However the RoboFab library is somewhat deprecated by modern font tool developers, because it was made to increase productivity when using proprietary font editors, and inherited some of their object models, and is also rather slow. 
The defcon library lacks the fancy diagrams but it is well documented code that was written from scratch to be a fast and solid foundation for modern Python font editors.

defcon Code: <https://github.com/typesupply/defcon/tree/ufo3>

defcon Docs: <http://ts-defcon.readthedocs.io/en/ufo3/>

#### 2.1 The defconQt Library

The [RoboFont](http://robofont.com) editor is a mature but proprietary general purpose font editor built on the foundation of defcon's master branch, supporting the UFOv2 format. 
There are many other font editor applications with specialist purposes, such as [Prepolator and Metrics Machine](http://tools.typesupply.com), [Superpolator](http://superpolator.com), and [RoundingUFO and ufoStretch](http://typemytype.com/tag/scripting/).
These all use [defconAppkit](https://github.com/typesupply/defconAppKit), a bridge between defcon and the [PyObjC](https://en.wikipedia.org/wiki/PyObjC) Python-ObjectiveC wrapper. 
Objective C was the object orientated programming language developed at NeXTStep, and the Cocoa API is the backbone of Mac OS X.

The TruFont editor is a new (at the time of writing) but libre general purpose font editor built on the foundation of defcon's ufo3 branch, supporting the UFOv3 format. 
The foundation of TruFont is defconQt, a bridge between defcon and the [PyQt](https://riverbankcomputing.com/software/pyqt/intro) Python-Qt (C++) wrapper. 

A Sugar Activity can't use the defconQt library because Qt and PyQt are not part of Sugar.
However, reading the defconQt source code will be very instructive for how to construct a font editor.

defconQt Code: <https://github.com/adrientetar/defconQt>

#### 3. The fontTools library (and TTX format)

The [OpenType](https://en.wikipedia.org/wiki/OpenType) format is the most widespread font end-user format in the world, fully supporting Unicode, almost all the world's writing systems, and supported by almost all the world's computer operating systems. 
The best way to become familiar with the format is by reading Microsoft's copy of the specification.

OpenType Specification: <https://www.microsoft.com/en-us/Typography/OpenTypeSpecification.aspx>

As a binary format, it isn't easy for humans to read or make simple scripting tools to operate on. 
The fontTools library was initiated to solve this, by reading and writing the binary format into Python objects, and persisting them to disk in an XML format, "TTX."

fontTools Code: <https://github.com/behdad/fonttools>

#### 4. The fontMake toolchain

An obvious requirement of any font editor is to support the export or generation of UFO source files to OpenType binary files, and a set of Python libraries has been developed to make this possible that are tied together by the fontMake project. 

fontmake Code: <https://github.com/googlei18n/fontmake>

#### Final Note

Since these libraries have been developed over many years, there is a lot of old information about them, so watch out that what you read is up to date.
And on the other hand, because they are all under active development, the documentation may be inherently out of date or incomplete.

For example, all the documentation for many of the libraries was handily maintained in a single site, but it is now a little out of date: <http://robodocs.readthedocs.io>

However, the beauty of working on libre software is that there is an active and friendly community of developers who will be happy to discuss your ideas and provide answers to smart questions, as explained here: 

<http://www.catb.org/esr/faqs/smart-questions.html>
