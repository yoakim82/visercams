

if __name__ == '__main__':
    mq = setup_mqtt()


    # Camera intrinsics
    width = 1920  # Replace with your image width in pixels
    height = 1080  # Replace with your image height in pixels
    fov_degrees = 90.0  # Replace with your desired FOV in degrees
    crop_w = 400
    crop_h = 400

    sensor_transforms = [
        carla.Transform(carla.Location(x=-20, y=0.0, z=20.4), carla.Rotation(yaw=45.0, pitch=0.0, roll=0.0)),
        carla.Transform(carla.Location(x=-24, y=26, z=20.4), carla.Rotation(yaw=0.0, pitch=-5.0, roll=0.0)),
        carla.Transform(carla.Location(x=23, y=28.6, z=20.4), carla.Rotation(yaw=180.0, pitch=-5.0, roll=0.0))
    ]

    #crops_que = [ImageQueue(max_size=4) for _ in range(len(sensor_transforms))]
    rgb_data = {f'rgb_image_{i + 1:02}': np.zeros((height, width, 4)) for i in range(len(sensor_transforms))}
    crop_data = {f'rgb_image_{i + 1:02}': np.zeros((crop_h, crop_w, 3)) for i in range(len(sensor_transforms))}
    crops_que = {f'rgb_image_{i + 1:02}': ImageQueue(max_size=100, name=f'crop_{i + 1:02}') for i in range(len(sensor_transforms))}


    setup_flask(rgb_data, crop_data, crop_w, crop_h, crops_que)
    main(mq, rgb_data, crop_data, crops_que, sensor_transforms, width, height, fov_degrees, crop_w, crop_h)