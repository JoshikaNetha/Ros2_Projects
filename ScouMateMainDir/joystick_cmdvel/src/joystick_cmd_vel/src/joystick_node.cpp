#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <SDL2/SDL.h>

class JoystickCmdVelNode : public rclcpp::Node {
public:
bool init_successful_ = false;

JoystickCmdVelNode() : Node("joystick_cmd_vel") {
    publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);

    if (SDL_Init(SDL_INIT_JOYSTICK) < 0) {
        RCLCPP_ERROR(this->get_logger(), "Failed to initialize SDL2: %s", SDL_GetError());
        return;
    }

    if (SDL_NumJoysticks() < 1) {
        RCLCPP_ERROR(this->get_logger(), "No joysticks connected");
        return;
    }

    joystick_ = SDL_JoystickOpen(0);
    if (!joystick_) {
        RCLCPP_ERROR(this->get_logger(), "Failed to open joystick: %s", SDL_GetError());
        return;
    }

    RCLCPP_INFO(this->get_logger(), "Joystick connected: %s", SDL_JoystickName(joystick_));


    init_successful_ = true;

    timer_ = this->create_wall_timer(
        std::chrono::milliseconds(50),
        std::bind(&JoystickCmdVelNode::publish_cmd_vel, this)
    );
}

bool is_initialized() const {
    return init_successful_;
}


    ~JoystickCmdVelNode() {
        if (joystick_) {
            SDL_JoystickClose(joystick_);
        }
        SDL_Quit();
    }

private:
    void publish_cmd_vel() {
        SDL_JoystickUpdate();

        // Example: Axis 1 for linear (forward/back), Axis 0 for angular (left/right)
        int16_t axis_1 = SDL_JoystickGetAxis(joystick_, 1); // typically forward/backward
        int16_t axis_0 = SDL_JoystickGetAxis(joystick_, 0); // typically left/right

        // Normalize to [-1, 1]
        double linear = -axis_1 / 32768.0;
        double angular = axis_0 / 32768.0;

        geometry_msgs::msg::Twist twist_msg;
        twist_msg.linear.x = linear * 1.0;   // scale as needed
        twist_msg.angular.z = angular * 1.0;


        std::cout<<"publish_cmd_vel "<<twist_msg.linear.x<<std::endl;
        std::cout<<"publish_cmd_vel "<<twist_msg.angular.z<<std::endl;

        publisher_->publish(twist_msg);
    }

    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    SDL_Joystick* joystick_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);

    auto node = std::make_shared<JoystickCmdVelNode>();
    if (!node->is_initialized()) {
        rclcpp::shutdown();
        return 1;
    }

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

