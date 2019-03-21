# Header variables and parameters.
import os
import numpy as np
from IPython.core.debugger import set_trace
import importlib
import sys
from default_config.masif_opts import masif_opts

params = masif_opts['site']

# Apply mask to input_feat
def mask_input_feat(input_feat, mask):
    mymask = np.where(np.array(mask) == 0.0)[0]
    return np.delete(input_feat, mymask, axis=2)

#config_file = sys.argv[1]
#run_config = importlib.import_module(config_file, package=None)
#params = run_config.params

if 'pids' not in params: 
    params['pids'] = ['p1', 'p2']

# Build the neural network model 
from masif_modules.MaSIF_site import MaSIF_site

if 'n_theta' in params:
    learning_obj = MaSIF_site(params['max_distance'], n_thetas=params['n_theta'], n_rhos=params['n_rho'], n_rotations=params['n_rotations'], idx_gpu = '/gpu:1', feat_mask=params['feat_mask'], n_conv_layers=params['n_conv_layers'])
else:
    learning_obj = MaSIF_site(params['max_distance'], n_thetas=4, n_rhos=3, n_rotations=4, idx_gpu = '/gpu:1', feat_mask=params['feat_mask'], n_conv_layers=params['n_conv_layers'])

# train
from masif_modules.train_masif_site import train_masif_site

print(params['feat_mask'])
if not os.path.exists(params['model_dir']):
    os.makedirs(params['model_dir'])
#else:
#    # Load existing network.
#    print ('Reading pre-trained network')
#    learning_obj.saver.restore(learning_obj.session, params['out_dir']+'model')

train_masif_site(learning_obj, params)

