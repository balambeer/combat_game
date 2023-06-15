Design doc
----------

Basis for puzzle platformer or combat adventure game?
For now focus on the fighting, keeping in mind that it would be nice if it were extendible. Sg like Golden Axe?

I think at first go, just try to implement the simple stuff:
3 attacks: high/low/stab. Maybe bind? Goal is to imbalance the opponent, then 1 more successful attack kills them. They recover their posture when not pressured. Timing/rhythm combat.

Try to build a prototype fast!

Keep in mind: telegraph must be longer than recovery


Implementation
--------------

Preparation for adding maps and stuff:
- Flip sprites based on facing
- Scale and position enemies
- Add proper sprites
- Add NPC idle logic (like patrolling a corridor, searching for the PC or whatever)

Maps and stuff:
- Add game-world position representation & conversion to screen position (i.e. camera)
- Add map representation
- Add map generation logic