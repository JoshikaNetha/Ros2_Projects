#include "rclcpp/rclcpp.hpp"
#include "turtlesim/srv/teleport_absolute.hpp"
#include "turtlesim/srv/set_pen.hpp"
#include <chrono>
#include <memory>

using namespace std::chrono_literals;

class TurtleController : public rclcpp::Node
{
public:
    TurtleController() : Node("turtle_controller")
    {
        // Create service clients
        teleport_client_ = this->create_client<turtlesim::srv::TeleportAbsolute>("/turtle1/teleport_absolute");
        pen_client_ = this->create_client<turtlesim::srv::SetPen>("/turtle1/set_pen");

        // Wait for services to be available
        RCLCPP_INFO(this->get_logger(), "Waiting for turtlesim services...");
        while (!teleport_client_->wait_for_service(1s) || !pen_client_->wait_for_service(1s))
        {
            RCLCPP_INFO(this->get_logger(), "Waiting for turtlesim services...");
        }

        // Call functions after initialization
        change_pen_color();
        teleport_turtle();
    }

private:
    rclcpp::Client<turtlesim::srv::TeleportAbsolute>::SharedPtr teleport_client_;
    rclcpp::Client<turtlesim::srv::SetPen>::SharedPtr pen_client_;

    void change_pen_color()
    {
        // Prepare request to change the pen color
        auto pen_request = std::make_shared<turtlesim::srv::SetPen::Request>();
        pen_request->r = 255;
        pen_request->g = 234;
        pen_request->b = 0;
        pen_request->width = 5;
        pen_request->off = 0;

        auto future = pen_client_->async_send_request(pen_request);

        // Wait for the future to complete
        if (rclcpp::spin_until_future_complete(this->get_node_base_interface(), future) == rclcpp::FutureReturnCode::SUCCESS)
        {
            RCLCPP_INFO(this->get_logger(), "Pen color changed successfully.");
        }
        else
        {
            RCLCPP_ERROR(this->get_logger(), "Failed to change pen color.");
        }
    }

    void teleport_turtle()
    {
        // Prepare request to teleport the turtle
        auto teleport_request = std::make_shared<turtlesim::srv::TeleportAbsolute::Request>();
        teleport_request->x = 10.0;
        teleport_request->y = 5.0;
        teleport_request->theta = 0.0;

        auto future = teleport_client_->async_send_request(teleport_request);

        // Wait for the future to complete
        if (rclcpp::spin_until_future_complete(this->get_node_base_interface(), future) == rclcpp::FutureReturnCode::SUCCESS)
        {
            RCLCPP_INFO(this->get_logger(), "Turtle teleported successfully.");
        }
        else
        {
            RCLCPP_ERROR(this->get_logger(), "Failed to teleport turtle.");
        }
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);

    // Use std::make_shared to ensure proper shared_ptr management
    auto turtle_controller_node = std::make_shared<TurtleController>();
    rclcpp::spin(turtle_controller_node);
    rclcpp::shutdown();

    return 0;
}
