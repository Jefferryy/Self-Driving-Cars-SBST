import pandas as pd
import numpy as np

import rss_metrics as rss

def grad(y, h):
    end = np.size(y)
    dy = np.zeros(end)
    dy[1:end-1] = (y[2:] - y[:end-2])/(2*h)
    dy[0] = (y[1] - y[0]) / h
    dy[end-1] = (y[end-1] - y[end-2]) / h
    return dy


# Create a trajectory from independent vectors
def create_trajectory(t, x, y, vx, vy, ax, ay):
    n = np.size(t)
    traj = [rss.CarState(t[i], x[i], y[i], vx[i], vy[i], ax[i], ay[i]) for i in range(n)]
    return traj

# Get the available trials from the file
def get_trials(file):
    df = pd.read_csv(file)
    trials = list(set(df["# trial"]))
    return trials


# Load the data into CarState trajectories for the specified trial
def get_trajectories(file, trial):
    df = pd.read_csv(file)

    trials = df["# trial"]
    trial_rows = trials == trial
    x_car = df[" x_car"][trial_rows].values
    y_car = df[" y_car"][trial_rows].values
    vx_car = df[" v_x_car"][trial_rows].values
    vy_car = df[" v_y_car"][trial_rows].values

    dt = (x_car[2] - x_car[1]) / (vx_car[1])
    t = dt * df[" step"][trial_rows].values
    ax_car_num = grad(vx_car, dt)
    ay_car_num = grad(vy_car, dt)

    x_ped = df["x_ped_0"][trial_rows].values
    y_ped = df["y_ped_0"][trial_rows].values
    vx_ped = df[" v_x_ped_0"][trial_rows].values
    vy_ped = df["v_y_ped_0"][trial_rows].values
    ax_ped = df["a_x_0"][trial_rows].values
    ay_ped = df["a_y_0"][trial_rows].values

    car_traj = create_trajectory(t, y_car, x_car, vy_car, vx_car, ay_car_num, ax_car_num)
    ped_traj = create_trajectory(t, y_ped, x_ped, vy_ped, vx_ped, ay_ped, ax_ped)
    return car_traj, ped_traj
