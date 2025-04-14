// src/keyboard_controller.cpp
#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include <termios.h>
#include <unistd.h>
#include <iostream>

class VehicleTeleopKey : public rclcpp::Node
{
public:
    VehicleTeleopKey() : Node("vehicle_teleop_key")
    {
        velocity_publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 5);
        RCLCPP_INFO(this->get_logger(), "Use U/H/J/K/N keys to move, X to quit.");
        control_loop();
    }

private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr velocity_publisher_;

    void control_loop()
    {
        while (rclcpp::ok())
        {
            char key = get_keypress();
            geometry_msgs::msg::Twist cmd;

            switch (key)
            {
            case 'u': cmd.linear.x = 1.0; break;
            case 'n': cmd.linear.x = -1.0; break;
            case 'h': cmd.angular.z = 1.0; break;
            case 'k': cmd.angular.z = -1.0; break;
            case 'j': cmd.linear.x = 0.0; cmd.angular.z = 0.0; break;
            case 'x': RCLCPP_INFO(this->get_logger(), "Exiting..."); return;
            default: continue;
            }

            velocity_publisher_->publish(cmd);
        }
    }

    char get_keypress()
    {
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
    std::make_shared<VehicleTeleopKey>();
    rclcpp::shutdown();
    return 0;
}
