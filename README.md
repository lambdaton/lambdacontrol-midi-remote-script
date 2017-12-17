# LambdaControl - MIDI Remote Script (Ableton Live)

<img src="https://www.lambdaton.de/images/github/lambdacontrol.jpg" alt="Picture of LambdaControl" width="420">

This repository contains the MIDI Remote Script for my DIY MIDI controller project [LambdaControl](https://www.lambdaton.de/diy-hardware/lambda-control/). 

I designed and build LambdaControl for my upcoming live performance and decided to release all components under open source licenses, such that other artists can use my project as they like.

A complete documentation of the project can be found on my [website](https://www.lambdaton.de/diy-hardware/lambda-control/).

## Project Overview
LambdaControl is based on the [MIDIbox project](http://www.ucapps.de/), which provides a complete solution for basic tasks like reading analog and digital inputs (faders, knobs and encoders). However, the RGB button matrix of LambdaControl, which works like the matrix of a Novation Launchpad, required a complete custom development.

LambdaControl consists of the following parts: components from the MIDIbox project for the basic I/O and USB MIDI connection, separate microcontroller which controls the RGB matrix, and a MIDI Remote Script that connects the controller with Ableton Live over USB (this repository). Additionally, I created a repository for the hardware parts like the RGB button matrix PCB or the 3D printable case.

## Ableton Live Integration

Simple mappings like connecting changes to the linear fader of a channel to the volume of the corresponding track inside Live is really easy with Ableton Live's MIDI mapping feature. However, more complex tasks like using the clip view of Ableton Live inside a custom MIDI controller is not that easy, since Ableton do not support an official way to do this. Hence, we need a mechanism that allows us to control the clip view via MIDI messages from the controller. Moreover, the mechanism needs to send changes to the clip view like creating a clip or changing a color to the controller, such that we can adjust correspondingly. In the following section I explain why the internally used MIDI Remote Scripts of Live allow us to fully support these features with LambdaControl.

## MIDI Remote Script

Thanks to [Julien Bayle](http://julienbayle.net/ableton-live-9-midi-remote-scripts/), I know that Live internally uses python scripts to integrate MIDI controllers like Ableton Push or the Novation Launchpad into Live. The python interface can be used to control the clip launcher, sent our color changes to the MIDI controller, or access for example the drum pad mode/synthesizer mode of Ableton Push. It is really interesting to see how they implemented these functions. Hence, the MIDI remote scripts provide a way to access the "hidden" functionality in our own MIDI controllers.

Therefore, I implemented an own MIDI remote script for LambdaControl, which can be found inside this repository. This script tells Live that LambdaControl has a 10x6 grid control that it should map to the clip view. Moreover, the script configures the encoder of the master channel as a scene selection control, such that we can use it to scroll up and down inside the clip grid.

The following screenshot shows the red grid that Live uses to visualize the current position of the clip grid.

<img src="https://www.lambdaton.de/images/github/lambdacontrol-clip-view.png" alt="LambdaControl inside Live">

I decided to configure the other functionality like volume changes, send/return-pots, and so on via the classical MIDI mapping of Ableton Live, since this allows to quickly change things without touching the MIDI remote script.

My script is based on code that Ableton has written for the first version of Push. Sadly (or not), they have rewritten their complete python code base with the introduction of Ableton Push 2, such that I need to include their old Colors and ConfigurableButtonElement classes as compiled python files to get the script working. If you are interested in this part of the code just search here on GitHub for older decompiled versions of these scripts.

## Installation

Just copy the content of this repository into a newly created LambdaControl folder inside the MIDI remote scripts folder of Ableton Live. For example, C:\ProgramData\Ableton\Live 9 Suite\Resources\MIDI Remote Scripts\LambdaControl on my Windows machine. Live automatically scans the folder at the next startup and if necessary compiles the script. After that you can select the script as every other script inside the settings menu. The name of the control surface script inside the list actually comes form the folder names inside the MIDI remote script folder, so in my case the script will be shown as LambdaControl.

<img src="https://www.lambdaton.de/images/github/ableton-lambdacontrol-settings.png" alt="LambdaControl setup inside the Live preferences">

## Author

2017 - LambdaTon 
  