import pickle

from examples.AV.example_runner_ba_av import runner as ba_runner
from examples.AV.example_runner_drl_av import runner as drl_runner
from examples.AV.example_runner_ge_av import runner as go_explore_runner
from examples.AV.example_runner_mcts_av import runner as mcts_runner

if __name__ == '__main__':
    # Overall settings
    max_path_length = 50
    s_0 = [0.0, -4.0, 1.0, 11.17, -35.0]
    base_log_dir = './data'
    # experiment settings
    run_experiment_args = {'snapshot_mode': 'last',
                           'snapshot_gap': 1,
                           'log_dir': None,
                           'exp_name': None,
                           'seed': 0,
                           'n_parallel': 8,
                           'tabular_log_file': 'progress.csv'
                           }

    # runner settings
    runner_args = {'n_epochs': 101,
                   'batch_size': 5000,
                   'plot': False
                   }

    # env settings
    env_args = {'id': 'ast_toolbox:GoExploreAST-v1',
                'blackbox_sim_state': True,
                'open_loop': False,
                'fixed_init_state': True,
                's_0': s_0,
                }

    # simulation settings
    sim_args = {'blackbox_sim_state': True,
                'open_loop': False,
                'fixed_initial_state': True,
                'max_path_length': max_path_length
                }

    # reward settings
    reward_args = {'use_heuristic': True}

    # spaces settings
    spaces_args = {}

    # DRL Settings

    drl_policy_args = {'name': 'lstm_policy',
                       'hidden_dim': 64#,
                       #'use_peepholes': True,
                       }

    drl_baseline_args = {}

    drl_algo_args = {'max_path_length': max_path_length,
                     'discount': 0.99,
                     'lr_clip_range': 1.0,
                     'max_kl_step': 1.0,
                     # 'log_dir':None,
                     }


    # DRL settings
    exp_log_dir = base_log_dir
    run_experiment_args['log_dir'] = exp_log_dir + '/drl'
    run_experiment_args['exp_name'] = 'drl'

    drl_runner(
        env_args=env_args,
        run_experiment_args=run_experiment_args,
        sim_args=sim_args,
        reward_args=reward_args,
        spaces_args=spaces_args,
        policy_args=drl_policy_args,
        baseline_args=drl_baseline_args,
        algo_args=drl_algo_args,
        runner_args=runner_args,
    )
    

