#%% Import statements
import rss_metrics as rss
from load_data import grad, create_trajectory
import pickle
import numpy as np
import matplotlib.pyplot as plt
from plot_utils import plot_trajectories_2ped

#%% Load RSS stuff
g = 9.8 # acceleration due to gravity
lat_params = rss.LateralParams( 0, #ρ
                            0.1*g, # a_lat_max_acc
                            0.05*g, # a_lat_min_brake
                            1 # Buffer distance
                            )

long_params = rss.LongitudinalParams(   0, #ρ
                                    0.7*g, #a_max_brake
                                    0.1*g, # a_max_acc
                                    0.7*g, # a_min_brake1
                                    0.7*g, # a_min_brake2
                                    1, # Buffer
                                    )

#%% Function for extracting trajectories from pickle file 
def get_trajectories(trajs, trial):
    data = trajs[trial]
    actions = data[0]

    dt = 0.1
    time = np.arange(0, actions.shape[1]*dt, dt)

    car_x = data[1]
    car_y = data[2]
    car_vx = grad(car_x, dt)
    car_vy = grad(car_y, dt)
    car_ax = grad(car_vx, dt)
    car_ay = grad(car_vy, dt)

    car2_x = data[3]
    car2_y = data[4]
    car2_vx = grad(car2_x, dt)
    car2_vy = grad(car2_y, dt)
    car2_ax = grad(car2_vx, dt)
    car2_ay = grad(car2_vy, dt)

    ped1_x = data[5]
    ped1_y = data[6]
    ped1_vx = grad(ped1_x, dt)
    ped1_vy = grad(ped1_y, dt)
    ped1_ax = grad(ped1_vx, dt)
    ped1_ay = grad(ped1_vy, dt)

    ped2_x = data[7]
    ped2_y = data[8]
    ped2_vx = grad(ped2_x, dt)
    ped2_vy = grad(ped2_y, dt)
    ped2_ax = grad(ped2_vx, dt)
    ped2_ay = grad(ped2_vy, dt)

    car_traj = create_trajectory(time, car_y, car_x, car_vy, car_vx, car_ay, car_ax)
    car2_traj = create_trajectory(time, car2_y, car2_x, car2_vy, car2_vx, car2_ay, car2_ax)
    ped1_traj = create_trajectory(time, ped1_y, ped1_x, ped1_vy, ped1_vx, ped1_ay, ped1_ax)
    ped2_traj = create_trajectory(time, ped2_y, ped2_x, ped2_vy, ped2_vx, ped2_ay, ped2_ax)
    return car_traj, car2_traj, ped1_traj, ped2_traj

def get_car1_response(trajs, trial):
    car_traj, _, ped1_traj, ped2_traj = get_trajectories(trajs, trial)
    resp_car_1, _,_,_ = rss.characterize_response(car_traj, ped1_traj, lat_params, long_params)
    resp_car_2, _,_,_ = rss.characterize_response(car_traj, ped2_traj, lat_params, long_params)
    return resp_car_1 + resp_car_2

def get_car2_response(trajs, trial):
    car1_traj, car2_traj, _, _ = get_trajectories(trajs, trial)
    resp_car2, _,_,_ = rss.characterize_response(car2_traj, car1_traj, lat_params, long_params)
    return resp_car2

def frac_improper(responses):
    totalsteps = responses.shape[0]
    num_improper = totalsteps - np.sum(responses == [rss.Response.Proper])
    return num_improper / totalsteps


#%% Load the trajecrtory files
f_gen = open("all_trajs_generic_reward.pkl", "rb")
f_td = open("all_trajs_td_reward.pkl", "rb")
gen_trajs = pickle.load(f_gen)
td_trajs = pickle.load(f_td)
print(gen_trajs.shape[0], " generic AST trajectories")
print(td_trajs.shape[0], " td AST trajectories" )


#%% Plot sample trajectory
trajs = td_trajs
trial = 13
car1_traj, car2_traj, ped1_traj, ped2_traj = get_trajectories(trajs, trial)
car1_resp = get_trajectories(trajs, trial)
danger1 = rss.characterize_danger(car1_traj, ped1_traj, lat_params, long_params)
danger2 = rss.characterize_danger(car1_traj, ped2_traj, lat_params, long_params)
resp_car1_ped1, _, ped1_resp, _ = rss.characterize_response(car1_traj, ped1_traj, lat_params, long_params)
resp_car1_ped2, _, ped2_resp, _ = rss.characterize_response(car1_traj, ped2_traj, lat_params, long_params)
car1_resp = resp_car1_ped1 + resp_car1_ped2
danger = danger1 + danger2

print("fraction improper: ", frac_improper(car1_resp))

plt.figure(1)
plot_trajectories_2ped(car1_traj, ped1_traj, ped2_traj, danger, danger1, danger2, "Danger level")
plt.figure(2)
plot_trajectories_2ped(car1_traj, ped1_traj, ped2_traj, car1_resp, ped1_resp, ped2_resp, "Response to Pedestrians")

#%% Compute fraction of timesteps improper
gen_ped_fracs = []
gen_car2_fracs = []
td_ped_fracs = []
td_car2_fracs = []
for trial in range(50):
    gen_ped_fracs.append(frac_improper(get_car1_response(gen_trajs, trial)))
    gen_car2_fracs.append(frac_improper(get_car2_response(gen_trajs, trial)))
    td_ped_fracs.append(frac_improper(get_car1_response(td_trajs, trial)))
    td_car2_fracs.append(frac_improper(get_car2_response(td_trajs, trial)))

plt.figure(5)
plt.hist(gen_ped_fracs, label="Generic", bins = np.arange(.12, step=0.01), alpha = 0.5, color="blue")
plt.hist(td_ped_fracs, label = "TD", bins = np.arange(.12, step=0.01), alpha = 0.5, color = "red")
plt.title("Vehicle 1 Fraction of Timesteps Improper - Compared to Peds")
plt.legend()

plt.figure(6)
plt.hist(gen_car2_fracs, label="Generic", bins = np.arange(.12, step=0.01), alpha = 0.5, color="blue")
plt.hist(td_car2_fracs, label = "TD", bins = np.arange(.12, step=0.01), alpha = 0.5, color = "red")
plt.title("Vehicle 2 Fraction of Timesteps Improper - Compared to other car")
plt.legend()




#%%
