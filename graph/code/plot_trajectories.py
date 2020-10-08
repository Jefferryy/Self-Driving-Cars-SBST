import rss_metrics as rss
import plot_utils
import matplotlib.pyplot as plt
import load_data as ld

g = 9.8 # acceleration due to gravity
lat_params = rss.LateralParams( 0, #ρ
                            0.1*g, # a_lat_max_acc
                            0.05*g, # a_lat_min_brake
                            1.4 # Buffer distance
                            )

long_params = rss.LongitudinalParams(   0, #ρ
                                    0.7*g, #a_max_brake
                                    0.1*g, # a_max_acc
                                    0.7*g, # a_min_brake1
                                    0.7*g, # a_min_brake2
                                    2.5, # Buffer
                                    )

file = "crashes_200.csv"
available_trials = ld.get_trials(file)
trial = 45
car_traj, ped_traj = ld.get_trajectories(file, trial)
danger = rss.characterize_danger(car_traj, ped_traj, lat_params, long_params)
resp_car, reasons_car, resp_ped, reasons_ped = rss.characterize_response(car_traj, ped_traj, lat_params, long_params)

plt.subplot(2,1,1)
plot_utils.plot_trajectories(car_traj, ped_traj, danger, danger, "Danger Level of Vehicle and Pedestrian Trajectories")
plt.subplot(2,1, 2)
plot_utils.plot_trajectories(car_traj, ped_traj, resp_car, resp_ped, "Response of Vehicle and Pedestrian")

plt.savefig('images/python_vehicle_not_at_fault')
