# Sugar Activity: Edit Fonts

Live Site: <http://sugarlabs.github.io/edit-fonts-activity/>

## How To Add New Posts

* Introduction to Jekyll posts: <https://jekyllrb.com/docs/posts/>
* Key concept: <https://jekyllrb.com/docs/frontmatter/>

### Live Editing

* Visit <https://github.com/sugarlabs/edit-fonts-activity/new/gh-pages/_posts> and click the `New File` button
* Name the file `YYYY-MM-DD-short-page-url-name.md`
* Author your content with markdown
* Add a [frontmatter](https://jekyllrb.com/docs/frontmatter/) similar to:

```yaml
---
layout: post
title: Blog Post Title in Camel Case
category: article
author: Your Name
---
```

### Local Editing

Install Jekyll: <https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/>

If there are any errors with the Jeykll configuration, templates, etc, then you will read about them in the output. 
To be sure you can run the following commands to ensure all packages are updated, and then run jeykll's checker:

    bundle update;
    jekyll hyde;

To run a local web server, from the root directory run:

    bundle exec jekyll serve  --incremental

Then visit <http://127.0.0.1:4000/edit-fonts-activity/> and each time you save a file in the repo, the site will be rebuilt and you can hit refresh to see the results.

## Licensing

This software is licensed under the GNU General Public License version 3.0, or any later version. 

Except where otherwise noted, website content on this site is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International](https://www.creativecommons.org/licenses/by-sa/4.0/) license.

For a list of copyright authors and human contributors, please see [AUTHORS.txt](AUTHORS.txt) and [CONTRIBUTORS.txt](CONTRIBUTORS.txt)

Some CSS and images are licensed under an MIT license.
