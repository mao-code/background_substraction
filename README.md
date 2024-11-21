[Github link](https://github.com/mao-code/background_substraction)
# Demo
Our threshold: ```motion_threshold = 5000```
Below is the simple background substraction demonstration and the event triggered:
Before(static):
![bf](images/bf.png)

After(moving)
![af](images/af.png)

Triggered Events
![event](images/triggered.png)

# Main Idea
$$ \text{Image}_t - \text{Image}_{t-1} > \text{threshold} $$


# References
* [Background Substraction](https://medium.com/@muhammadsabih56/background-subtraction-in-computer-vision-402ddc79cb1b)