Open Color ramp generator.py in /Color

Enter the starting color's HSV components and target contrast ratio, which is the contrast ratio you desire between each generated color.
Then enter the delta due, saturation, and value, which are ratios that make up the slope in 3d color space of the line on which all of the colors fall.

Example: You want a ramp for some forest foliage that goes from a very dark blue-green for deep shadows to a bright light green for new leaves in spring.
Try 210 hue, 90 saturation, and 10 value. This gives us the very dark starting color.
1.4 target contrast ratio will do. Higher if you want a shorter ramp with greater difference between the colors.
For 'Delta hue' enter -1.8, since we want to shift towards red as the colors get brighter. If you wanted to shift towards purple, use a positive number.
In this example we want the colors to get less saturated as they get brighter, so enter a negative value for 'Delta saturation' like -0.3.
And since we're starting on the dark end of the ramp, obviously we want the colors to get brighter, so use a positive number for 'Delta value'. Try entering 1.

Press 'Generate', and continue tweeking things and re-generating until you get what you want, and then copy the colors with the 'Copy hex' buttons.


Notes:

 - The delta fields are just ratios, you can enter whatever values you want. 1:0.3 is equivilant to 100:30.
 - The contrast ratio formula affects the colors generated. At present there are just two very slightly different options, and in many cases you won't be able to
tell the difference between them by looking at the colors. The hexadecimal color codes will be different tho, at least for the colors on the right side.
Future versions are likely to include other contrast ratio formulas.