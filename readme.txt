Design doc
----------

Basis for puzzle platformer or combat adventure game?
For now focus on the fighting, keeping in mind that it would be nice if it were extendible. Sg like Golden Axe?

I think at first go, just try to implement the simple stuff:
3 attacks: high/low/stab. Maybe bind? Goal is to imbalance the opponent, then 1 more successful attack kills them. They recover their posture when not pressured. Timing/rhythm combat.

Have a BPM variable, and only accept fighting inputs on the beat? Maybe not great UX, as you don't know the beat unless you are cued. 
If there is no global bpm, we still need sg like this to enforce the rhythm part of combat. So fighters must have a state marking whetner they're accepting input or not.

Try to build a prototype fast!