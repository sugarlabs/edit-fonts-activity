# Sugar Font Editor Activity

Live Site: <http://sugarlabs.github.io/font-editor-activity/>

## How To Add New Posts

See Jekyll documentation at <https://jekyllrb.com/docs/frontmatter/> and <https://jekyllrb.com/docs/posts/>

### Local Editing

Install Jekyll and then from the root directory run

    jekyll serve  --incremental

If there are any errors with the Jeykll configuration, templates, etc, then you will read about them in the output. 

Then visit <http://127.0.0.1:4000/font-editor-activity/> and each time you save a file in the repo, the site will be rebuilt and you can hit refresh to see the results.

### Live Editing

* Visit <https://github.com/sugarlabs/font-editor-activity/new/gh-pages/_posts>
* Name the file `YYYY-MM-DD-short-page-url-name.md`
* Add a [frontmatter](https://jekyllrb.com/docs/frontmatter/) similar to:

```
---
layout: post
title: Blog Post Title in Camel Case
category: article
author: Your Name
---
```

* Author your content with markdown



## Licensing

This software is licensed under the GNU General Public License version 3.0, or any later version. 

Except where otherwise noted, website content on this site is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International](https://www.creativecommons.org/licenses/by-sa/4.0/) license.

For a list of copyright authors and human contributors, please see [AUTHORS.txt](AUTHORS.txt) and [CONTRIBUTORS.txt](CONTRIBUTORS.txt)

Some CSS and images are licensed under an MIT license.
