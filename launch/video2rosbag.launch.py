import os
import launch
import launch.actions
import launch.substitutions
import launch_ros.actions
from launch.actions import DeclareLaunchArgument
from launch.substitutions import TextSubstitution, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    rviz_config_dir = os.path.join(
        get_package_share_directory('video2rosbag'),
        'rviz',
        'video_frames.rviz')

    video_file_launch_arg = DeclareLaunchArgument(
        "video_file", default_value=TextSubstitution(text="nada.mp4")
    )

    video_file = str(LaunchConfiguration('video_file'))

    #video_file_name = video_file.split(".")[0]

    video_path = os.path.join(
        get_package_share_directory('video2rosbag'),
        'videos',
        video_file)   

    bag_files_dir = os.path.join(
        get_package_share_directory('video2rosbag'),
        'bag_files',
        "{0}_bag_file".format(video_file))

    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'video_frames']
        ),
        launch_ros.actions.Node(
            package='video2rosbag',
            executable='video_publisher',
            name='video_publisher'
        ),
        launch_ros.actions.Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
        ),
        launch.actions.ExecuteProcess(
            cmd=['ros2', 'bag', 'record', 
                '/raw_video_frames', 
                '/tf_static',
                '-o', bag_files_dir],
            output='screen'
        ),
    ])