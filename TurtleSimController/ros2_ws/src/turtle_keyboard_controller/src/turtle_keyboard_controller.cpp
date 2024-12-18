#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include <iostream>
#include <termios.h>
#include <unistd.h>

class TurtleKeyboardController : public rclcpp::Node
{
public:
    TurtleKeyboardController() : Node("turtle_keyboard_controller")
    {
        // Publisher for velocity commands
        velocity_publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);

        RCLCPP_INFO(this->get_logger(), "Turtle Keyboard Controller initialized. Use keys: W, A, S, D, X");
        RCLCPP_INFO(this->get_logger(), "W: Forward, A: Left, D: Right, X: Backward, S: Stop");

        control_loop();
    }

private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr velocity_publisher_;

    void control_loop()
    {
        while (rclcpp::ok())
        {
            char key = get_keypress();
            geometry_msgs::msg::Twist cmd_vel;

            switch (key)
            {
            case 'w': // Move forward
                cmd_vel.linear.x = 2.0;
                cmd_vel.angular.z = 0.0;
                RCLCPP_INFO(this->get_logger(), "Moving forward");
                break;

            case 'a': // Turn left
                cmd_vel.linear.x = 0.0;
                cmd_vel.angular.z = 2.0;
                RCLCPP_INFO(this->get_logger(), "Turning left");
                break;

            case 'd': // Turn right
                cmd_vel.linear.x = 0.0;
                cmd_vel.angular.z = -2.0;
                RCLCPP_INFO(this->get_logger(), "Turning right");
                break;

            case 'x': // Move backward
                cmd_vel.linear.x = -2.0;
                cmd_vel.angular.z = 0.0;
                RCLCPP_INFO(this->get_logger(), "Moving backward");
                break;

            case 's': // Stop
                cmd_vel.linear.x = 0.0;
                cmd_vel.angular.z = 0.0;
                RCLCPP_INFO(this->get_logger(), "Stopping");
                break;

            case 'q': // Quit
                RCLCPP_INFO(this->get_logger(), "Exiting...");
                return;

            default:
                RCLCPP_INFO(this->get_logger(), "Invalid key. Use W, A, S, D, X");
                continue;
            }

            // Publish velocity command
            velocity_publisher_->publish(cmd_vel);
        }
    }

    char get_keypress()
    {
        // Disable terminal buffering and get a single key press
        struct termios oldt, newt;
        char ch;
        tcgetattr(STDIN_FILENO, &oldt);
        newt = oldt;
        newt.c_lflag &= ~(ICANON | ECHO);
        tcsetattr(STDIN_FILENO, TCSANOW, &newt);
        ch = getchar();
        tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
        return ch;
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TurtleKeyboardController>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
