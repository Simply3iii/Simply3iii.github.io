---
title: HeroBot and the maze dungeon
summary: Coursework. A robot in a maze that can only see a tiny camera view, and two ways to read it.
when: 2026
where: University of Bristol, AI for Robotics coursework
where_short: Bristol MSc
tags: [AI & ML]
cover: /static/img/maze/accuracy-vs-time.jpg
featured: false
order: 5
gallery:
  - src: /static/img/maze/accuracy-vs-time.jpg
    caption: Accuracy against training time, random forest vs CNN
  - src: /static/img/maze/loss-curve.jpg
    caption: The CNN's training loss over 30 epochs
---

The robot lives in a gridworld maze, built on Gymnasium, and sees only a 20 × 20 greyscale
camera view. Part of the coursework was classifying those camera views, and I compared a random
forest with a small convolutional neural network.

The CNN got the highest accuracy, about 99% after 30 epochs. The random forest got 98.7% and
trained almost instantly. For a robot with limited compute, that trade-off matters more than
the last 0.4%.
