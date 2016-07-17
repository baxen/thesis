# A Search for Long-Lived, Charged, Supersymmetric Particles using Ionization with the ATLAS Detector

Summary of four years on ATLAS, primarily a measurement of calorimeter response and a search for long-lived, massive, charged particles.

## Progress
<p align="center">
<img src="/figures/progress.png">
</p>

## Organization

- `chapters/` actual content in chapters
  - `ch01_introduction.tex` for a chapter
  - `app0A_dummy.tex` for an appendix
- `frontback/` stuff that surrounds the content, such as the acknowledgments
- `figures/` plots and images for all chapters
- `bibliography.bib`: the BibTex database for references
- `classicthesis.sty`: style definitions
- `axen_thesis.tex`: the main filewhere all the content gets bundled together
- `classicthesis-config.tex`: a central place to load packages
  - Changes and adjustments to the style or mostly controlled here

## Style Considerations

### Colors

Using a basic color scheme that vaguely fits with UC Berkeley colors

![Color Scheme](/figures/scheme.png?raw=true)

### Font Choices

The template used Palatino with a lot of small caps to handle titles and headings. I added xelatex support and moved to Crimson for a nicer font option, with Julius Sans One for all headings. (Merriweather is another option if Julius end up being too light for real printouts.)

### From the template: 
>Some things of this style might look unusual at first glance, many people feel so in the beginning. However, all things are intentionally designed to be as they are, especially these:
>- No bold fonts are used. Italics or spaced small caps do the job quite well.
>- The size of the text body is intentionally shaped like it is. It supports both legibility and allows a reasonable amount of information to be on a page. And, no: the lines are not too short.
>- The tables intentionally do not use vertical or double rules. See the documentation for the `booktabs` package for a nice discussion of this topic.
>- To provide the reader with a way easier access to page numbers in the table of contents, the page numbers are right behind the titles. Yes, they are **not** neatly aligned at the right side and they are **not** connected with dots that help the eye to bridge a distance that is not necessary

