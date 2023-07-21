import numpy as np
import cv2
import importlib.util
import matplotlib.pyplot as plt


def vidvis(images, output_path='./vis.mp4'):
    # output_path = './vis.mp4'

    # define the color map
    cmap = plt.cm.get_cmap('jet').copy()
    cmap.set_under('k')

    # get the height, width, and number of frames of the video
    num_frames, height, width = images.shape

    # create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(output_path, fourcc, 60, (width, height))

    # write each image to the video writer
    for i in range(num_frames):
        # get the image and normalize it
        frame = images[i, :, :]
        image = cmap(frame)
        image = (image[:, :, :3] * 255).astype(np.uint8)

        # set the color for values below the minimum to black
        image[frame == 0] = [0, 0, 0]

        # set the color for values above or equal to 1 to red
        image[(frame >= 1)] = [0, 0, 255]

        # set the color for values below or equal to 1 to green
        image[(frame <= -1)] = [0, 255, 0]

        # write the color image to the video writer
        output_video.write(image)

    # release the video writer object
    output_video.release()


if __name__ == '__main__':
    # set the path of the helper file
    helper_path = '3d_events.py'

    # load the helper module
    spec = importlib.util.spec_from_file_location('helper', helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)

    # get sequence
    file_path = './c_vl.h5'
    vid_path = file_path.replace('.h5', '.mp4')
    # img_seq = helper.csv2sequence(file_path)
    img_seq = helper.h52sequence_dvx(file_path)

    # trans to video
    vidvis(img_seq, vid_path)
