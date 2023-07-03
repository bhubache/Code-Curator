- Timing intervals from forced alignment that don't map to a word should be created as implicit Wait animations.

- Move the update of DataStructureAnimation timings to be before running the scheduling methods inside SceneScheduler.

- Fix animation of temporary submobjects! For example, when adding a node to the end of a singly linked list and animating a pointer, if we decide to center the sll before fading out the temp pointer, we want to center the whole structure as if the temporary pointer isn't there!
