# RPG_with_OOP

This semester (Fall 2021), I completed a course in Object-Oriented Programming. The topics I had a chance to explore range from basic paradigms of OOP and abstract classes to advanced design patterns. I expect that this experience will make my future code far more functional, reliable, practical, efficient, maintainable, and hopefully eye-pleasing.

## Instructions

1. You play as a medieval knight traveling through a multi-level dungeon full of dreadful enemies and occasionally helpful allies.
2. Run the `Main.py` file to launch the game.
3. Press `H` to see the help window.
4. Press `P` to pause the game.
5. And more importantly, have fun!

## Project History and Goals

The project I worked on included refactoring the provided code in accordance with the SOLID principles of OOP and significantly extending the interface of the program. Overall, I wrote more than 1000 code lines to create this relatively simple game.

<p align="center">
  <img src="https://user-images.githubusercontent.com/42875258/146490592-fccd13f0-51bb-4def-a7a6-bdd764a0b179.gif" width="525">
</p>

Although the visual component of this project might lack certain finesse, the structure of the underlying code was scrupulously fitted to satisfy the conventions of the Object-Oriented Design. 

## Design patterns
To demonstrate what I have learned this semester, I aimed for my program to exploit several design patterns. 

**1. Chain of responsibility** 

<p align="center">
  <img src="https://user-images.githubusercontent.com/42875258/146488334-5443a975-abf7-47e5-9d87-5eb0da7995ea.png" width="700">
</p>
 
ScreenEngine.py contains all visual elements of the game, including GameSurface, ProgressBar (at the bottom), InfoWindow (on the left), MiniMap, and interface for HelpWindow and StatusWindow. In Main.py, they are sequenced into the *Chain of Responsibility* which handles the drawing aspect.
  
**2. Observer**

Logic.py contains GameEngine, which handles the game session and acts as an *Observer*, which can be notified to update the InfoWindow.
  
**3. Abstract factory**

<p align="center">
  <img src="https://user-images.githubusercontent.com/42875258/146493778-8317a41e-7cb2-46fb-b0b4-38e7a94b21bf.png" width="525">
</p>
  
Service.py contains MapFactory class which supports several map classes as an *Abstract Factory*.
  
**4. Decorator** 

<p align="center">
  <img src="https://user-images.githubusercontent.com/42875258/146488326-e8a6937a-06d5-443e-a067-3c87e78d0111.png" width="525">
</p>
  
*Decorator* pattern is used to implement Effects (Pickpocket, Blessing, MagicBow, Weakness, Berserk) that can be applied on Hero and removed by Allies and Enemies.
  
## Other improvements

There are numerous details I added to my project. The most notable features are *smooth zoom* and a *mini-map*. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/42875258/146489050-659ef3d0-e2de-4a65-ae3f-e449afbe2c5d.gif" width="300">
  <img src="https://user-images.githubusercontent.com/42875258/146492106-53e4b4e7-1f66-4e3e-a3a0-dd8dc397081b.gif" width="300">
</p>

In conclusion, I experienced that within the paradigms of the OOP there is almost nothing I could not achieve in a reasonable time. Thus, correct Object-Oriented Design is a powerful tool that supports stable and robust coding practices.
