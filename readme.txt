Design doc
----------

Basis for puzzle platformer or combat adventure game?
For now focus on the fighting, keeping in mind that it would be nice if it were extendible. Sg like Golden Axe?

I think at first go, just try to implement the simple stuff:
3 attacks: high/low/stab. Maybe bind? Goal is to imbalance the opponent, then 1 more successful attack kills them. They recover their posture when not pressured. Timing/rhythm combat.

Have a BPM variable, and only accept fighting inputs on the beat? Maybe not great UX, as you don't know the beat unless you are cued. 
If there is no global bpm, we still need sg like this to enforce the rhythm part of combat. So fighters must have a state marking whetner they're accepting input or not.

Try to build a prototype fast!


Implementation
--------------

- Add NPC attacking (to test if attacks resolve well on that side also)
- Place fighters into a "fighter handler" class, for easier resolution of shit? Also with an eye toward making this a Castlevantia type shit?
- Add proper attack resolution (i.e. hit/block/reposte/counter):
  * introduce telegraphing state, and animation & state depends on whether input arrives when opponent is telegraphing
  * upon collision - i.e. no explicit telegraphing state for attacks, animations are always the same. Still need cue as to what is happening, and animation can change after... not sure if this is such a good idea.