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
  * 3 states to each attack: 1 - telegraph, 2 - attack, 3 - recovery
  * introduce death animation


enemy handling, fight handling
------------------------------

Enemy handling
- Enemies live in an enemy handler. This holds 3 lists: dead enemies, non-fghting enemies, and fighting enemies.
- The handler is responsible for transferring enemies between these 3 lists (each enemy can only be part of 1 list), and evaluating the fights between the player and the fighting enemies.
- Fighting enemies are defined as being within a given distance to the player. Dead enemies are the ones that are dead and don't need updating. Non-fighting enemies can have some other behavior, like patrolling or guarding or whatnot.

Resolving fights
- Each fight is between 2 fighters: the player and an enemy npc.
- Each fighter receives control inputs, which get converted to a state. The state then determines the animation.
- The conversion of control inputs -> state (i.e. the update_state function) should be split into two.
  * If the fighter is not currently in a fight, it works as it's implemented in the Fighter class (maybe rename to update_state_no_fight, and introduce a flag 'fighting' or sg).
  * If the fighter is in a fight, then the state update is delegated to the fight handler, which also takes into consideration the actions of the enemy (it's a funciton of self.control_inputs and enemy.state). The update can favor the player, i.e. start with their update first.
- The attacking state should have 3 possible values: "telegraph", "attack", "recovery" (instead of a boolean). These need to be frame indexes, and the dictionaries should be filled up when initializing the player. I need to be able to parse csv files for this...
- The logic for updating the state in a fight is a rock-paper-scissors system:
  * self.control_input == "attack_*" and (not enemy.state == "attack_*"): as currently
  * self.control_input == "attack_low" and enemy.state == "attack_low": self.state = "block"
  * self.control_input == "attack_mid" and enemy.state == "attack_low": self.state = "block" followed immediately by an "attack_mid". The attack should start right when the recovery of the attacker starts.
HOW WILL I MAKE SURE THAT THE BLOCK LENGTH IS CORRECT?
  * self.control_input == "attack_high" and enemy.state == "attack_low": self.state = "idle" - MAYBE NEED A SPECIAL STATE FOR THIS? (MAYBE DO ATTACK LOW)
  * So basically, we have attack_high < attack_low < attack_mid, and we just repeat the pattern to resolve the other combinations...

