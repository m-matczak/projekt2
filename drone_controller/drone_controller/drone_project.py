import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist, Pose


class DroneController(Node):
    def __init__(self):
        super().__init__('drone_controller')
        
        # Current pose subscriber
        self.gt_pose_sub = self.create_subscription( Pose, '/drone/gt_pose',
            self.pose_callback, 1)

        self.gt_pose = None

        # Control command publisher
        self.command_pub = self.create_publisher(Twist, '/drone/cmd_vel', 10)
        
        # Callback for executing a control commands
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Feel fre to fill with your code! Add some objects to represent a goal points to achieve
        self.goals = [[10.0, -10.0],[10.0, 10.0], [-10.0, 10.0], [-10.0, -10.0]]
        self.next_goal = 0
    
    def pose_callback(self, data):
        self.gt_pose = data
        #print(f"{data}")

    
    def timer_callback(self):
        # HINT: Check a current pose. Use it to check if a drone achieved a desired pose.
        x = 0
        y = 0
        if self.gt_pose is not None:
            x = self.gt_pose.position.x
            y = self.gt_pose.position.y
        
        # Calculating distance to checkpoint
        # for some reason position recievied and sent is different hence the multiplication
        dx = abs(x*2 - self.goals[self.next_goal][0])
        dy = abs(y*2 - self.goals[self.next_goal][1])

        # if distance to checkpoint is small enough move to the next
        if dx < .5 and dy < .5:
            print("Reached goal, going to the next one")
            self.next_goal += 1
            if self.next_goal > len(self.goals) -1:
                self.next_goal = 0

        # HINT: Use a self.command_pub to publish a command
        # Fill with your code!
        msg = Twist()
        msg.linear.z = 2.5

        msg.linear.x = self.goals[self.next_goal][0]
        msg.linear.y = self.goals[self.next_goal][1]

        self.command_pub.publish(msg)



def main(args=None):
    rclpy.init(args=args)

    node = DroneController()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
