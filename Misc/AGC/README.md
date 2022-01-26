#Automatic Gain Control

This model use a gain control to force the ADC inputs to a constant power. The algotihm works in the time domain and its based in the minimizing the mean square error of the input power and the desired one.

#Implementation info:
- Calculate the square of the input data.
- Use a moving average module to calculate the mean. The DELAY_LINE parameter controls the window size.
- Multiply the average power by a weight coefficient.
- Calcualte the difference between the weighted power and the referece power (thats our error)
- Multiply the error by the error coeficient (our learning rate)
- Adjust the weight. 
- Multiply the input data to control the power actual power level.

#TODO
-[x] Simulation
-[x] Hardware test
-[ ] Documentation
