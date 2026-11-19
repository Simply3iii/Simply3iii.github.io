---
title: Sizing 3D-printed prosthetic hands automatically
summary: My undergraduate dissertation. A desktop app that scales a printable hand to fit a person.
when: 2025
where: Heriot-Watt University, BSc Computer Science dissertation
where_short: Heriot-Watt BSc
tags: [software, hardware, AI & ML]
cover: /static/img/prosthetic/4-outline.jpg
show_cover: false
featured: true
order: 3
gallery:
  - src: /static/img/prosthetic/1-first-try.jpg
    caption: "1. Early on: picking out the hand against grid paper"
  - src: /static/img/prosthetic/2-finding-the-hand.jpg
    caption: "2. Finding the hand and cropping to it"
  - src: /static/img/prosthetic/3-grid-corners.jpg
    caption: "3. Detecting the grid's corners to get real-world scale"
  - src: /static/img/prosthetic/4-outline.jpg
    caption: "4. A clean outline of the hand, ready to measure"
---

3D-printed prosthetic hands are cheap, but fitting one to a person still needs someone who
knows CAD. For my undergraduate dissertation I built a desktop app that does the resizing:
you put in hand measurements, it reshapes the model in FreeCAD, and you get files ready to print.

## What I built

- A scaling algorithm in Python that works out ratios from the measurements
- Scripts that drive FreeCAD's Python API to reshape the model
- A PyQt5 interface with a live 3D preview (VTK)
- Packaged as a Windows app and as a Docker container

*Supervised by Prof. Alistair McConnell.*

![My poster for the dissertation](/static/img/prosthetic/poster.jpg)

## Measuring a hand from a photo

The part I enjoyed most was trying to measure a hand from a photo taken on grid paper, so
nobody would need a tape measure. It was still early when the project ended. These are the
versions in order, from wrong to less wrong:

