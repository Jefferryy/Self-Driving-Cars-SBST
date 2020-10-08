import matplotlib.pyplot as plt
import rss_metrics as rss

colors = {
    rss.Dangerous.Safe: 'g',
    rss.Dangerous.LongitudinallyDangerous: 'y',
    rss.Dangerous.LaterallyDangerous: 'm',
    rss.Dangerous.Dangerous: 'r',
    rss.Response.Proper: 'g',
    rss.Response.ImproperLongitudinal: 'r',
    rss.Response.ImproperLateral: 'r',
    rss.Response.ImproperBoth: 'r'
}

labels = {
    rss.Dangerous.Safe: "Safe",
    rss.Dangerous.LongitudinallyDangerous: "Longitudinally Dangerous",
    rss.Dangerous.LaterallyDangerous: "Laterally Dangerous",
    rss.Dangerous.Dangerous: "Dangerous",
    rss.Response.Proper: "Proper Response",
    rss.Response.ImproperLongitudinal: "Longitudinally Improper",
    rss.Response.ImproperLateral: "Laterally Improper",
    rss.Response.ImproperBoth: "Both Improper Response"
}

def plot_trajectories_2ped(car_traj, ped1_traj, ped2_traj, car_labels, ped1_labels, ped2_labels, title):
    # Get the list of colors to color each point in the trajectory
    car_colors = [colors[i] for i in car_labels]
    ped1_colors = [colors[i] for i in ped1_labels]
    ped2_colors = [colors[i] for i in ped2_labels]

    # Setup the axes, and title
    p = plt.plot([], [], label="")
    plt.title(title)
    plt.xlabel("x-position (m)")
    plt.ylabel("y-position (m)")
    plt.xlim(-10, 10)

    # Plot the trajectories
    plt.scatter([cs.x for cs in car_traj], [cs.y for cs in car_traj], marker="s", label="", c=car_colors)
    plt.scatter([cs.x for cs in ped1_traj], [cs.y for cs in ped1_traj], marker="o", label="", c=ped1_colors)
    plt.scatter([cs.x for cs in ped2_traj], [cs.y for cs in ped2_traj], marker="*", label="", c=ped2_colors)

    # Set the labels for car and pedestrian
    plt.plot([], [], marker="s", color="k", label="Car")
    plt.plot([], [], marker="o", color="k", label="Pedestrian1")
    plt.plot([], [], marker="*", color="k", label="Pedestrian2")

    # Set the colors for danger level
    for v in set(ped1_labels) | set(car_labels) | set(ped2_labels):
        plt.plot([], [], color=colors[v], linewidth=5, label=labels[v])

    plt.legend()

def plot_trajectories(car_traj, ped_traj, car_labels, ped_labels, title):
    # Get the list of colors to color each point in the trajectory
    car_colors = [colors[i] for i in car_labels]
    ped_colors = [colors[i] for i in ped_labels]

    # Setup the axes, and title
    p = plt.plot([], [], label="")
    plt.title(title)
    plt.xlabel("x-position (m)")
    plt.ylabel("y-position (m)")
    plt.xlim(-10, 10)

    # Plot the trajectories
    plt.scatter([cs.x for cs in car_traj], [cs.y for cs in car_traj], marker="s", label="", c=car_colors)
    plt.scatter([cs.x for cs in ped_traj], [cs.y for cs in ped_traj], marker="o", label="", c=ped_colors)

    # Set the labels for car and pedestrian
    plt.plot([], [], marker="s", color="k", label="Car")
    plt.plot([], [], marker="o", color="k", label="Pedestrian")

    # Set the colors for danger level
    for v in set(ped_labels) | set(car_labels):
        plt.plot([], [], color=colors[v], linewidth=5, label=labels[v])

    plt.legend()
