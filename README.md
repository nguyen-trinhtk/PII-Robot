<h1>Trash-collecting Robot</h1>

<h2>Project Description</h2>
<h3>1. Overview</h3>
This is an autonomous bottle-collecting robot that uses computer vision to detect bottles and lidar algorithms to avoid obstacles. Plastic trash pollution is on the rise in modern times, with dire consequences for the environment. However, automatic trash-collecting robots on the market today are difficult to obtain and quite complicated. Previous deployments of automated systems for the same task had not been optimized in terms of cost and hardware. After designing, simulating obstacle avoidance algorithms, and retraining the object detection model, the goal of this research is to improve and create a more optimized robot system. Its findings can be used in future similar research.

<h3>2. The PII program</h3>
This research project is carried out as part of the PTNK Innovation Initiative (PII) Summer Research Internship Program under the topic "4d. Smart Robot" at Makerspace - Fulbright University Vietnam from June 15, 2023, to September 5, 2023. The program is established and run by PTNK (<i>VNU-HCM High School for the Gifted</i>) STEAM CLUB.

<h2>Implementation</h2>
The implementation of this robot includes three main stages: designing its mechanics, assembling electronic components, and establishing its software.
●  Our 3D design file can be found here: <a href="https://github.com/nguyen-trinhtk/PII-robot/RobotDesign">Design folder.</a>
●  We used an Arduino Uno and Jetson Nano as controllers; DC motors as actuators; and an RPLidar and webcam as sensors.
●  There are three main programs for this robot: bottle detection, obstacle avoidance, and controlling the motors. Arduino Uno and Jetson Nano communicate through the serial port. Bottle detection and obstacle avoidance algorithms are joined by multi-threading. For optimizing the object detection model, we trained the TinyYoloV3 with an available dataset. An equation for calculating the distance to a bottle from the camera's image is formed. 
For more details, please see our code repository: <a href="https://github.com/nguyen-trinhthi/PII-robot/Arduino">Arduino</a>, <a href="https://github.com/nguyen-trinhthi/PII-robot/BottleDetection">Bottle Detection</a>, and <a href="https://github.com/nguyen-trinhthi/PII-robot/RPLidar">Obstacle Avoidance</a>.

<h2>Results and discussion</h2>
We have successfully deployed a robot system capable of navigating, detecting bottles, and avoiding obstacles with a price range of $341 to $400. This result fits the initial scope of this project. However, the Jetson Nano's processing speed and object detection model's rate are still relatively slow; the lidar can be optimized with the implementation of ROS SLAM simulation. In addition, the robot's electronic components are not covered, making them susceptible to damage and malfunction. Future research should focus on resolving these proposed issues.

Images and videos of this robot can be found here: <a href="https://github.com/nguyen-trinhtk/PII-robot/Results/Media">Media</a>

<h2>Report</h2>
<object data="https://github.com/nguyen-trinhtk/PII-Robot/blob/main/Results/Report%20Paper.pdf" type="application/pdf" width="700px" height="700px">
        <p>For further information, please refer to our report: <a href="https://github.com/nguyen-trinhtk/PII-Robot/blob/main/Results/Report%20Paper.pdf">View on GitHub</a> or 
        <a href="https://github.com/nguyen-trinhtk/PII-Robot/raw/main/Results/Report%20Paper.pdf">Download PDF.</a></p>
</object>
