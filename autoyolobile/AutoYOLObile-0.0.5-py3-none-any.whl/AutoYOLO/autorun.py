import os
from train import main_autorun
from test import test_autorun

class YOLO_Autorun:
    def print_info(self, info):
        print('---------------------------------------------------')
        print(info)
        print('---------------------------------------------------')

    
    def run(self):
        str1 = input("Please enter the accuracy (mAP 0.5) requirement (default 48):")
        str2 = input("Please enter the latency requirement (default 5.2):")
        str3 = input("Please enter the device number, split by ',' (default 0,1,2,3):")

        #acc_req = requirement['accuracy']
        #speed_req = requirement['inference_time']

        if str1 != '':
            acc_req = float(str1)
        else:
            acc_req = 48
        if str2 != '':
            speed_req = float(str2)
        else:
            speed_req = 5.2
        if str3 != '':
            device = str(str3)
        else:
            device = '0,1,2,3'
        print('The accuracy requirement is {}'.format(acc_req))
        print('The speed requirement is {}'.format(speed_req))

        if acc_req > 48 and  acc_req < 50:
            prune_file = 'config_csdarknet53pan_v14'
            sparsity = 'block-punched'
        elif acc_req >= 50 and  acc_req < 51:
            prune_file = 'config_csdarknet53pan_v10'
            sparsity = 'block-punched'
        elif acc_req >= 51 and  acc_req < 52:
            prune_file = 'config_csdarknet53pan_v8'
            sparsity = 'block-punched'
        elif acc_req >= 52:
            prune_file = 'config_csdarknet53pan_v4'
            sparsity = 'block-punched'
        else:
            prune_file = 'config_csdarknet53pan_v14'
            sparsity = 'block-punched'
            
        # ckpts_prune = 'ckpts/ckpt_a'
        # ckpts_retrain = 'ckpts/ckpt_m'
        # ckpts_final = 'ckpts/ckpt_f'
        # if not os.path.exists(ckpts_prune):
        #     os.makedirs(ckpts_prune)
        # if not os.path.exists(ckpts_retrain):
        #     os.makedirs(ckpts_retrain)
        # if not os.path.exists(ckpts_final):
        #     os.makedirs(ckpts_final)

        upperpath = 'ModelOpt/AutoYOLO/'

        cmd_prune = 'python {}train.py --admm --epoch 25 --cfg {}cfg/csdarknet53s-panet-spp.cfg --data {}data/coco2014.data --weights weights/yolov4dense.pt --device {} --config-file {} --sparsity-type {}'.format(upperpath, upperpath, upperpath, device, prune_file, sparsity)
        cmd_retrain = 'python {}train.py --masked-retrain --epoch 280 --cfg {}cfg/csdarknet53s-panet-spp.cfg --data {}data/coco2014.data --device {} --config-file {} --sparsity-type {} --multi-scale'.format(upperpath, upperpath, upperpath, device, prune_file, sparsity)

        # cmd_test_prune = 'python pytorch/test_mask.py --model_dir={}/best_checkpoints --config-file={} --sparsity-type={}'.format(ckpts_prune, prune_file, sparsity)
        cmd_test_retrain = 'python {}test.py --device {} --cfg {}cfg/csdarknet53s-panet-spp.cfg --data {}data/coco2014.data --weights {}weights/best.pt'.format(upperpath, device, upperpath, upperpath, upperpath)


        # copy_ckpts_original = 'cp ckpts/ckpts_original/* {}'.format(ckpts_prune) 
        # os.system(copy_ckpts_original)
        # print_info('obtain original model')
            
        self.print_info('start prune.')

        # print(cmd_prune)
        # os.system(cmd_prune)
        main_autorun(['--admm', 
                        '--epoch', '1', 
                        '--cfg', upperpath+'cfg/csdarknet53s-panet-spp.cfg', 
                        '--data', upperpath+'data/coco2014.data', 
                        '--weights', 'weights/yolov4dense.pt', 
                        '--device', device,
                        '--config-file', prune_file,
                        '--sparsity-type', sparsity])

        # print_info('finish admm prune process')
        # copy_ckpts_prune = 'cp {}/best_checkpoints/*  {}'.format(ckpts_prune, ckpts_retrain)
        # os.system(copy_ckpts_prune)
        # print_info('obtain pruned model')

        self.print_info('finish prune, start retrain.')

        # print(cmd_retrain)
        # os.system(cmd_retrain)
        main_autorun(['--masked-retrain', 
                        '--epoch', '1', 
                        '--cfg', upperpath+'cfg/csdarknet53s-panet-spp.cfg', 
                        '--data', upperpath+'data/coco2014.data', 
                        '--multi-scale',
                        '--device', device,
                        '--config-file', prune_file,
                        '--sparsity-type', sparsity])

        self.print_info('finish retrain.')

        # print(cmd_test_retrain)
        # os.system(cmd_test_retrain)

        test_autorun(['--device', device,
                        '--cfg', upperpath+'cfg/csdarknet53s-panet-spp.cfg',
                        '--data', upperpath+'data/coco2014.data',
                        '--weights', 'weights/best.pt'])
        self.print_info('finish retrain with the above accuracy')



        self.print_info('obtain final model')

        self.print_info('you can find the model at ./weights/best.pt')

        
    
if __name__ == "__main__":
    ac = YOLO_Autorun()
    ac.run()