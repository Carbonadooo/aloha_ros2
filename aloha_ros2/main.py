def teleop():
    puppet_bot = InterbotixManipulatorXS(robot_model="vx300s", group_name="arm", gripper_name="gripper", robot_name='puppet', init_node=True)
    master_bot = InterbotixManipulatorXS(robot_model="wx250s", group_name="arm", gripper_name="gripper", robot_name='master', init_node=False)


if __name__=='__main__':
    teleop()