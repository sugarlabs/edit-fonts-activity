---
layout: post
title: Drawing UFO GLIF outlines with Cairo
category: article
author: Dave Crossland
---

Yash has already got glyph rendering going!

![contour](files/img/2016-05-23-0.png)

However, when filling the glyph, it isn't rendering the "counter" or white-shape:

![contour](files/img/2016-05-23-1.png)

The reason is that the default "fill rule" is using the "winding directions" of the contours. 
The pycairo documentation explains,

> Whether or not a point is included in the fill is determined by taking a ray from that point to infinity and looking at intersections with the path. 
> The ray can be in any direction, as long as it doesn’t pass through the end point of a segment or have a tricky intersection such as intersecting tangent to the path. 
> (Note that filling is not actually implemented in this way. This is just a description of the rule that is applied.)

The default fill rule is `FILL_RULE_WINDING`:

    cairo.FILL_RULE_WINDING
    If the path crosses the ray from left-to-right, counts +1. 
    If the path crosses the ray from right to left, counts -1. 
    (Left and right are determined from the perspective of 
      looking along the ray from the starting point.) 
    If the total count is non-zero, the point will be filled.

But there is another fill rule:

    cairo.FILL_RULE_EVEN_ODD
    Counts the total number of intersections, without regard 
      to the orientation of the contour. 
    If the total number of intersections is odd, the point 
      will be filled.

<https://cairographics.org/documentation/pycairo/2/reference/constants.html#constants-fill-rule>

While FILL_RULE_WINDING is the rule used for PostScript, a simplified editor for kids should use FILL_RULE_EVEN_ODD and a 'correct directions' method should be auto-applied, so that kids don't have to think about winding directions.
