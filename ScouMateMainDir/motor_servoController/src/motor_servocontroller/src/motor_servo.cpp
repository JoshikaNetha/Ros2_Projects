#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <std_msgs/msg/float32.hpp> // Include this
#include <termios.h>
#include <fcntl.h>
#include <unistd.h>
#include <string>
#include <sstream>
 
class MotorController : public rclcpp::Node
{
public:
	MotorController()
	: Node("motor_controller")
	{
    	// Serial port configuration
    	// serial_port_ = open("/dev/ttyUSB0", O_RDWR | O_NOCTTY);
    	// if (serial_port_ < 0) {
        // 	RCLCPP_ERROR(this->get_logger(), "Failed to open serial port.");
    	// } 
    	// configureSerial(); 
    	subscription_ = this->create_subscription<geometry_msgs::msg::Twist>(
        	"cmd_vel", 10,
        	std::bind(&MotorController::cmdVelCallback, this, std::placeholders::_1)
    	);
		servo_subsciption_ = this->create_subscription<std_msgs::msg::Float32>(
			"servo_angle", 10,
			std::bind(&MotorController::stdmsgCallback, this, std::placeholders::_1)
		);
	} 
	~MotorController()
	{
    	if (serial_port_ > 0) close(serial_port_);
	} 
private:
	int serial_port_;
	rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr subscription_;
	rclcpp::Subscription<std_msgs::msg::Float32>::SharedPtr servo_subsciption_;

 
	void configureSerial()
	{
    	struct termios tty;
    	if (tcgetattr(serial_port_, &tty) != 0) {
        	RCLCPP_ERROR(this->get_logger(), "Error getting serial attributes.");
        	return;
    	} 
    	cfsetispeed(&tty, B115200);
    	cfsetospeed(&tty, B115200); 
    	tty.c_cflag &= ~PARENB; // No parity
    	tty.c_cflag &= ~CSTOPB; // 1 stop bit
    	tty.c_cflag &= ~CSIZE;
    	tty.c_cflag |= CS8; 	// 8 bits per byte
    	tty.c_cflag |= CREAD | CLOCAL; 
    	tty.c_lflag &= ~ICANON;
    	tty.c_lflag &= ~ECHO;
    	tty.c_lflag &= ~ECHOE;
    	tty.c_lflag &= ~ISIG;
    	tty.c_iflag &= ~(IXON | IXOFF | IXANY);
    	tty.c_oflag &= ~OPOST; 
    	tty.c_cc[VMIN] = 0;
    	tty.c_cc[VTIME] = 10; 
    	if (tcsetattr(serial_port_, TCSANOW, &tty) != 0) {
        	RCLCPP_ERROR(this->get_logger(), "Error setting serial attributes.");
    	}
	} 
	void cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg)
	{
    	float joy_x = msg->angular.z;
    	float joy_y = msg->linear.x;
    
    	int left_speed = 0;
    	int right_speed = 0;
    
    	// Same logic as your Python version
    	if (std::abs(joy_x) > 0.15) {
        	if (joy_x > 0) {
            	left_speed = 249;
            	right_speed = 215;
        	} else {
            	left_speed = -255;
            	right_speed = -210;
        	}
    	} else if (std::abs(joy_y) > 0.15) {
        	if (joy_y > 0) {
            	left_speed = -255;
            	right_speed = 210;
        	} else {
            	left_speed = 255;
            	right_speed = -210;
        	}
    	}
    
    	// Create JSON command string
    	std::ostringstream stream;
    	stream << "{\"T\":11,\"L\":" << left_speed << ",\"R\":" << right_speed << "}\n";
    
    	std::string data = stream.str();
    
    	RCLCPP_INFO(this->get_logger(), "Sending Serial JSON: %s", data.c_str());
    
    	// Send over serial
    	// ssize_t bytes_written = write(serial_port_, data.c_str(), data.length());    
    	// if (bytes_written < 0) {
        // 	RCLCPP_ERROR(this->get_logger(), "Failed to write to serial port.");
    	// }
	}  
    
    void stdmsgCallback(const std_msgs::msg::Float32::SharedPtr msg){
        float joy_z = msg->data;

        const float SERVO_DEAD_ZONE = 0.1;  // You can adjust this threshold
        int pos = static_cast<int>(((joy_z + 1.0f) / 2.0f) * 360.0f - 180.0f);
    
        std::ostringstream stream;
    
        if (std::abs(joy_z) < SERVO_DEAD_ZONE) {
            stream << "{\"T\":\"135\"}\n";  // Neutral position
        } else {
            stream << "{\"T\":\"133\",\"X\":" << pos
                   << ",\"Y\":" << pos
                   << ",\"SPD\":200,\"ACC\":100}\n";
        }
    
        std::string data = stream.str();
    
        RCLCPP_INFO(this->get_logger(), "Sending Servo Serial JSON: %s", data.c_str());
    
        ssize_t bytes_written = write(serial_port_, data.c_str(), data.length());
        if (bytes_written < 0) {
            RCLCPP_ERROR(this->get_logger(), "Failed to write servo command to serial port.");
        }
    }
};


int main(int argc, char *argv[])
{
	rclcpp::init(argc, argv);
	auto node = std::make_shared<MotorController>();
	rclcpp::spin(node);
	rclcpp::shutdown();
	return 0;
}
