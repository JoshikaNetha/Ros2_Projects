#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "sensor_msgs/msg/range.hpp"

class LineFollowerNode : public rclcpp::Node
{
public:
    LineFollowerNode() : Node("line_follower_node")
    {
        // Publisher for velocity commands
        velocity_publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);

        // Subscriber for line sensor data
        sensor_subscription_ = this->create_subscription<sensor_msgs::msg::Range>(
            "/line_sensor", 10,
            std::bind(&LineFollowerNode::sensor_callback, this, std::placeholders::_1));
    }

private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr velocity_publisher_;
    rclcpp::Subscription<sensor_msgs::msg::Range>::SharedPtr sensor_subscription_;

    void sensor_callback(const sensor_msgs::msg::Range::SharedPtr msg)
    {
        auto cmd_vel = geometry_msgs::msg::Twist();

        if (msg->range < 0.1)
        {
            // Robot is on the line
            cmd_vel.linear.x = 0.5;  // Move forward
            cmd_vel.angular.z = 0.0; // Go straight
        }
        else
        {
            // Robot is off the line
            cmd_vel.linear.x = 0.0;
            cmd_vel.angular.z = 0.5; // Turn to search for the line
        }

        velocity_publisher_->publish(cmd_vel);
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<LineFollowerNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
