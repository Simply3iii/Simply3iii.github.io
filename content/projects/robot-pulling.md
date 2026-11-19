---
title: How hard is the robot pulling?
summary: Group coursework. Could a small robot tell what it's dragging from how hard its motors work?
when: 2025
where: University of Bristol, Robotics Science and Systems (group coursework)
where_short: Bristol MSc
tags: [robotics, hardware, group project]
cover: /static/img/robot/pwm-vs-mass.jpg
featured: true
order: 4
gallery:
  - src: /static/img/robot/pwm-vs-mass.jpg
    caption: Motor effort (PWM) needed to pull boxes of different masses at a constant speed
  - src: /static/img/robot/predicted-vs-actual.jpg
    caption: What a simple linear model predicted against what we measured
---

With my group, I worked on a Pololu 3pi+ robot: a small wheeled robot you program in C++ on
an Arduino-style microcontroller. We had it pull boxes of different masses at a constant speed,
with PID control keeping the speed steady, and recorded how much motor power (PWM) that took.

The question was whether the robot could estimate the load it was dragging just from its own
motor effort. A straight-line fit explained about three-quarters of the variation
(R² ≈ 0.76 over 21 measurements). Good enough to tell light from heavy, not to weigh things.
