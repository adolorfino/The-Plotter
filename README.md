# The Whiteboard Plotter

## Our Project
At the end of the term our team developed a Whiteboard Plotter to translate HPGL files into physical drawings on a whiteboard. The goal was to be able to hand draw a single line image using inkspace and then be able to use our plotter to draw a similar image on the whiteboard. With out final design we were able to sucessfully plot a handful of images. The purpose of our device was to be a simple plotter that almost anyone in our class could operate. We wanted our plotter to be something easy for a person with limited knowledgable in mechatronics to understand. Based on our hardware and software design a person would first set our plotter in it's starting position: as far clockwise on the whiteboard the pen would got and with the pen carrier closest to the main axial. Then the user can draw a single line image in inkspace. They would save the drawing's coordinates as a text file which they would enter in line 198 in the main file of our software. All that's left is to run the main file and then turn on power to the plotter and the image should be drawn on the whiteboard.

## Hardware Design
Majority of our plotter ws made from scraps found in the Mechatronic Lab or already in our ME405 Tub. The main outliers were the two motor connecters we 3D printed and the threaded rod set we bought from amazon. We have a more detailed breakdown our our materials in the "Bill of Material" section of the README below. Additionally, we added the CAD model references from which we built our final hardwar from in the "CAD Model" section of the report.

Here are images of our final hardware design:
![Final1](/../main/images/Final1.jpg)
![Final2](/../main/images/Final2.jpg)
![Final3](/../main/images/Final3.jpg)

As seen from the images we have two motors controlling the movement of the plotter. One is located closer to the axis of the plotter and is connected to the threaded rod carrying the pen. When that motor moves it adjusts how far the pen is related to the axis, the r value coordinate. The other motor is located at the end of the arm of the plotter and attached to a wheel. This motor is responsible for adjusting the theta value of the plotter. Each set of the r and theta values for a given coordinate is communicated through a Nucleo attached to the back of the plotter's arm. The Nucleo tells the two motors how much each of them are supposed to move and in what direction to reach the next coordinates; meausurements are converted from inches to ticks on the encoder. As the two motors adjust to the set r and theta values the pen carriers moves and draws on the whiteboard to plot the image.

## Bill of Materials 

| Qty. | Part                  | Source                | Est. Cost |
|:----:|:----------------------|:----------------------|:---------:|
|  2   | Pittperson Gearmotors | ME405 Tub             |     -     |
|  1   | Nucleo with Shoe      | ME405 Tub             |     -     |
|  1   | Whiteboard            | ME405 Classroom       |     -     |
|  1   | Expo Marker           | Pencil Case           |     -     |
|  1   | Threaded Rod Set      | Amazon                |   $30.39  |
|  1   | Wooden panel          | Leftover scrap wood   |     -     |
|  1   | Wiring                | ME405 Tub             |     -     |
|  1   | Dremel cutting set    | Amazon                |   $7.18   |
|  1   | Caster wheel          | Theatre Department    |     -     |
|  2   | Motor Connectors      | 3D print              |     -     |
|  1   | Screws/Nuts/Bolts     | Mustang 60 Bolt Wall  |     -     |

## CAD Model

Below are pictures of the 3D model of our proposed machine.
![CAD1](/../main/images/CAD1.PNG)
![CAD2](/../main/images/CAD2.PNG)

## Software Design
Since the plotter works in the polar plane instead of the ploter plane we needed to convert the given x and y values from our HPGL file to r and theta values. To do that was needed to separate each x-y coordinate pair and put them in a list to be converted into a new list of r and theta coordinates. Then our code would feed each coordinate pair to our plotter so it could adjust it's postitioning. Once the flags were triggered to tell our code that the correct r and theta values were reached, our code would send the next coordinate until it was done with the list. A more detail explanation of our code can be found on our Doxygen page [here.]()

## Project Results
A video of our plotter drawing a figure 8 can be seen [here.](https://youtube.com/shorts/5B91q9ULuf0?feature=share)

From the video one can see our plotter draws the shape of the figure 8 quite well. While the figure 8 image plots successfully our plotter our team had difficultly plotting more complex shapes. For example, when we attempted to draw a single-line dachshund only some parts of the dog were recognizeable. We beieve this was from our conversion calculations from cartiesan to polar not being perfect conversions. This was most likely from an offset in the plotter's arm from the rotating axial. We were unsure how to correct for the the offset but sill were able to produce some of the images correctly.

Before the final testing we also performed some preliminary testing on the plotter. To check the controller for the two motors we perfromed test to make sure that once our motors reach a set point it would not move until given the next point. For example, we put in a set point and then manually tried to move the plotter from that spot, after a few iterations we were successful for both motor. 

## Takeaways 
The main takeaways from this project is that when making a plotter there are three improvments we would recommend. The first is to account for the offest of the plotter arm or make the plotter arm directly in-line with the main axial.  This would eliminate some of the miscommunication between the coordinates from the coade and the ones being plotted on the whiteboard. The other improvement would be to make the plotter automatically go to its set starting position when it is first ran. This would ensure that plotter is always starting at a point that makes sure the drawing does not run off the page. The last improvment would to be adding a solenoid to the pen carrier to open our options to multi-lined drawings. 

We believe our plotter was a great first iteration however there is much room for improvemnt in our design. If given a little more time we think we could improve our plotter to plot more complicated images.
