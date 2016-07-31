from ufoLib.plistlib import PlistParser
"""
Small helper module to parse Plist-formatted data from trees as created
by xmlTreeBuilder.
"""

__all__ = "readPlistFromTree"

def readPlistFromTree(tree):
	"""
	Given a (sub)tree created by xmlTreeBuilder, interpret it
	as Plist-formatted data, and return the root object.
	"""
	parser = PlistTreeParser()
	return parser.parseTree(tree)


class PlistTreeParser(PlistParser):

	def parseTree(self, tree):
		element, attributes, children = tree
		self.parseElement(element, attributes, children)
		return self.root

	def parseElement(self, element, attributes, children):
		self.handleBeginElement(element, attributes)
		for child in children:
			if isinstance(child, tuple):
				self.parseElement(child[0], child[1], child[2])
			else:
				self.handleData(child)
		self.handleEndElement(element)


if __name__ == "__main__":
	from ufoLib.xmlTreeBuilder import buildTree
	tree = buildTree("xxx.plist", stripData=0)
	print(readPlistFromTree(tree))
