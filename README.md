# RPG_with_OOP

This semester (Fall 2021) I completed a course in Object Oriented Programming. The topics I had a chance to explore range from basic paradigms of OOP and abstract classes to advanced design patterns. I feel that this experience will make my future code far more functional, reliable, practical, efficient, maintainable, and hopefully eye-pleasing.

## The project itself

The project I worked on included refactoring the provided code in accordance with the SOLID principles of OOP and singnificantly extending interface of the program. Overall, I wrote more than 1000 lines of code to create this relatively simple game. Although, the presentation of this project might lack visual finess, the structure of underlying code was scrupolously fitted to satisfy the conventions of the Object Oriented Design. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/42875258/146490592-fccd13f0-51bb-4def-a7a6-bdd764a0b179.gif" width="525">
</p>
 
To demonstrate what I have learned this semester, I aimed for my program to include several of the design patterns. 

## Design paterns
**1. Chain of responsibility** 

<p align="center">
  <img src="https://user-images.githubusercontent.com/42875258/146488334-5443a975-abf7-47e5-9d87-5eb0da7995ea.png" width="700">
</p>
 
ScreenEngine.py contains all visual elements of the game including: GameSurface, ProgressBar (at the bottom), InfoWindow (on the left), MiniMap, and interface for HelpWindow and StatusWindow. In Main.py they are organised into the Chain of responsibility which handles the drawing.
  
**2. Abstract factory**

<p align="center">
  <img src="https://user-images.githubusercontent.com/42875258/146488338-7a09af3e-abbb-4f6e-9e15-19b749345429.png" width="525">
</p>
  
 Service.py contains MapFactory class which supports several map classes as an abstract factory.
  
**3. Observer**

<p align="center">
  <img src="https://user-images.githubusercontent.com/42875258/146488322-15748c58-9e4c-4023-b538-0325d3e3d035.png" width="200">
</p>
  
Logic.py contains GameEngine which handles the game session and acts as an Observer, notifying the InfoWindow on the left.
  
**4. Decorator** 

<p align="center">
  <img src="https://user-images.githubusercontent.com/42875258/146488326-e8a6937a-06d5-443e-a067-3c87e78d0111.png" width="525">
</p>
  
Decorator pattern is used to implement Effects that are applied and can be removed by Allies and Enemies.
  
## Other improvements

<p align="center">
  <img src="https://user-images.githubusercontent.com/42875258/146489050-659ef3d0-e2de-4a65-ae3f-e449afbe2c5d.gif" width="300">
  <img src="https://user-images.githubusercontent.com/42875258/146492106-53e4b4e7-1f66-4e3e-a3a0-dd8dc397081b.gif" width="300">
</p>
