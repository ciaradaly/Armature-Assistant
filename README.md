
# Armature Assistant

## About

Blender Python plugin that assists with the rigging of simple single appendage objects. Designed as a project for Final Year in a multimedia, web and mobile degree. Written in Python.

* Project status: Prototype

## Installation Steps

1. Download the source code from https://github.com/ciaradaly/Armature-Assistant/releases/tag/v1.0.0 and extract it to some folder on your local device
2.	Copy the `/test` folder and prepare to move it to a new location
3.	Find your Blender `addons` folder. This generally follows the path `(where you installed blender)/Blender Foundation/Blender 2.75/2.75/scripts/addons`
4.	Copy the `/test` folder from Armature-Assistant to the addons folder
5.	Open the Blender application.
6.	On the Top Left, select `Edit` and then `Preferences` (at the bottom)
7.	On Interface, tick `Developer Extras` and `Python Tooltips`
8.	Select the tab `Add-ons`
![image](https://user-images.githubusercontent.com/72494811/157926159-c778d571-2b6d-491b-9f33-3d6e3f9defbc.png)

9.	Press `Install` and find the addons folder (`(where you installed blender)/Blender Foundation/Blender 2.75/2.75/scripts/addons)` from step 1). Double click to install the `__init__.py` file in the test folder.
10.	On the top right corner of the preferences window search `Armature Plugin`. Press the checkmark on the plugin to install. (You may need to restart Blender or press Refresh)
![image](https://user-images.githubusercontent.com/72494811/157926194-3dc81ded-c3dc-42dc-85d5-f333c278d548.png)

11.  Verify you can see the plugin by pressing on the arrow on the top right of your screen and pressing `Armature Plugin`
![image](https://user-images.githubusercontent.com/72494811/157926198-35082e94-1dd4-4080-aff8-58c95444cd43.png)
![image](https://user-images.githubusercontent.com/72494811/157926204-5e75e762-98b3-495f-aa3a-30659c346008.png)

### Features
Features include:
1. Creating Armatures from Bezier curves
2. Adjusting Bone amounts along a Bezier curve
3. Aligning a Mesh and Curve based on a mesh's first principal component
### Requirements

minimum requirement is Blender 2.80

See [Blender Versions](https://www.blender.org/download/releases/2-80/)

