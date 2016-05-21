import os
from defcon import Font

#load the font
path = "sample"

#TODO: put this inside a try/except
font = Font(path)

print("This font has " + str(len(font)) + " glyphs");

for glyph in font:
	#just trying out some stuff on the glyphs
	#print(glyph.representationKeys());
	#print(glyph.drawPoints());
	#p=glyph.getRepresentation('NZBezierPath');
	#drawPath(p);

	print(glyph.name);
	
	

