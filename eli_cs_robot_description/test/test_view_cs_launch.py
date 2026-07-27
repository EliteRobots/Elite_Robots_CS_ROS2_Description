# Author: Chen Shichao

import os
import pytest

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_testing.actions import ReadyToTest


# Executes the given launch file and checks if all nodes can be started
@pytest.mark.rostest
def generate_test_description():
    launch_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("eli_cs_robot_description"), "launch/view_cs.launch.py")
        ),
        launch_arguments={"cs_type": "cs63"}.items(),
    )

    return LaunchDescription([launch_include, ReadyToTest()])
