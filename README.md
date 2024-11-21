[Github link](https://github.com/mao-code/background_substraction)
# Demo
## Background Substraction
Our threshold: ```motion_threshold = 5000```
Below is the simple background substraction demonstration and the event triggered:

<div>Before(static):</div>
<img src="images/bf.png" width="500"/>

<div>After(moving):</div>
<img src="images/af.png" width="500"/>

<div>Triggered Events:</div>
<img src="images/triggered.png" width="500"/>

## Background Substraction w/ hand detection

<div>Before:</div>
<img src="images/hand_bf.png" width="500"/>
<img src="images/hand_bf_2.png" width="500"/>

<div>After:</div>
<img src="images/hand_af.png" width="500"/>

# Main Idea
$$ \text{Image}_t - \text{Image}_{t-1} > \text{threshold} $$

# References
* [Background Substraction](https://medium.com/@muhammadsabih56/background-subtraction-in-computer-vision-402ddc79cb1b)