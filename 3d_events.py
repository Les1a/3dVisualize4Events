import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def view_sequence(event_sequence):
    # create a 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    # get the coordinates of the non-zero elements in the data
    t_idx, x_idx, y_idx = np.nonzero(event_sequence)

    # get the values of the non-zero elements in the data
    values = event_sequence[t_idx, x_idx, y_idx]

    # plot the non-zero elements as a scatter plot in 3D space
    for i in range(len(x_idx)):
        if values[i] >= 1:
            ax.scatter(t_idx[i], y_idx[i], x_idx[i], c='red', s=1)
        elif values[i] <= -1:
            ax.scatter(t_idx[i], y_idx[i], x_idx[i], c='blue', s=1)

    # set the labels for the x, y and t axes
    ax.set_xlabel('Time(ms) axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('X axis')

    # show the plot
    plt.show()


def h52squence(h5_path):
    with h5py.File(h5_path, "r") as f:
        # get the event data
        x = f['x'][:]
        y = f['y'][:]
        t = f['t'][:]
        p = f['p'][:]

        # create a DataFrame to store the event data
        event_points = pd.DataFrame({'x': x, 'y': y, 't': t, 'p': p})
        fps = 1000
        period_t = 1 / fps  # s
        num_frame = ((event_points.iloc[-1]['t'] - event_points['t'][0]) * fps) // 1

        '''sum events'''
        print(num_frame)
        img_list = []
        for n in np.arange(num_frame//7.5, num_frame//6.5):
            print(n)
            t_start = event_points['t'][0] + period_t * n
            t_end = event_points['t'][0] + period_t * (n + 1)
            chosen_idx = np.where((event_points['t'] >= t_start) * (event_points['t'] < t_end))[0]
            xypt = event_points.iloc[chosen_idx]
            x, y, p = xypt['x'], xypt['y'], xypt['p']
            p = p * 2 - 1

            img = np.zeros((480, 640))
            img[y, x] += p
            img_list.append(img)
        img_list = np.array(img_list)
    return img_list


def csv2sequence(csv_path):
    event_points = pd.read_csv(csv_path, names=['t', 'x', 'y', 'p'])  # names=['x', 'y', 'p', 't']

    fps = 1000
    period_t = 1 / fps  # s
    num_frame = (event_points.iloc[-1]['t'] * fps) // 10

    '''sum events'''
    print(num_frame)
    img_list = []
    for n in np.arange(num_frame):
        print(n)
        chosen_idx = np.where((event_points['t'] >= period_t * n) * (event_points['t'] < period_t * (n + 1)))[0]
        xypt = event_points.iloc[chosen_idx]
        x, y, p = xypt['x'], xypt['y'], xypt['p']
        p = p * 2 - 1

        img = np.zeros((720, 1280))
        img[y, x] += p
        img_list.append(img)
    img_list = np.array(img_list)
    return img_list


if __name__ == '__main__':
    file_path = './events.h5'
    if file_path.endswith('csv'):
        view_sequence(csv2sequence(file_path))
    elif file_path.endswith('h5'):
        view_sequence(h52squence(file_path))
