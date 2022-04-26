# Interactive-Cat-Toy
UCF Senior Design Project ( Fall 2021 - Spring 2022 )

The Interactive Cat Toy (ICT) is a whimsical plush toy that is made to stimulate any cat’s playful instincts. With that in mind, our group spent an entire semester understanding and designing multiple components that will grasp the interest and entice your typical domesticated feline. Our findings were that the movement of a tail, sounds, and lighting were all features that were at the top of our list. So, our group decided that the best thing to do was to mash them together! Creating what is now the ICT we have today.

Expanding on those features we are allowing even more customizability of the ICT for cat owners. With interchangeable skins, making the ICT appear to be a squirrel or a lizard (with other possible designs to expand on), the ability to place catnip in the tail, and an application to change the main three different features.

The application has the capability to change each of the main three features. The speaker contains three different sounds to choose from, the lighting has three patterns to choose from, while finally, the movement of the tail has three different motions or speeds to choose from. With the application and the interchangeable skins, there are currently eighteen different combinations for the ICT.

#---- Material programmed with code: ----#
    
    WS2812 LED strip
    ServoMotor
    STEMMA Speaker
    HC-SR501 Sensor 
    HC-05 Bluetooth

#---- Application Signals: ----#

    1st digit is function 
          0 - lighting
          1 - sound
          2 - tail motion
    2nd digit is pattern / sound
          0 - Option 1 (base)
          1 - Option 2
          2 - Option 3
          3 - Option 4 (off)
    Ex: O1 changes lighting to pattern option 2

