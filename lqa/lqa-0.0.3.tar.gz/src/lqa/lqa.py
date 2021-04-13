#! /usr/bin/env python
# coding=utf-8

import tensorflow as tf
import keras
import numpy as np
import time
import sys
import copy
import random

class lqa(object):
    # 处理训练任务
    pause = False
    name_dict = {
        'sgd': 'SGD',
        'rmsprop': 'RMSprop',
        'adagrad': 'Adagrad',
        'adadelta': 'Adadelta',
        'adam': 'Adam',
        'adamax': 'Adamax',
        'nadam': 'Nadam'
    }
    
    def name_map(self, x):
        if x in self.name_dict:
            return self.name_dict[x]
        else:
            return x
    
    def log_refresh(self, filename):
        # 更新日志
        with open(filename, 'w') as f:
            f.write('Start \n')

    def log(self, filename, info):
        # 记录信息
        print(info)
        with open(filename, 'a') as f:
            f.write(info+'\n')   
            
    def test(self, _model, batch_size, X0_test, Y0_test):
        # 测试在训练集上的loss、ACC
        # reset
        self.test_loss.reset_states()
        self.test_accuracy.reset_states()

        # 先测试训练集上
        K = int(len(X0_test) / batch_size)    

        for k in range(K):
            if not self.pause:
                _X,_Y = X0_test[k*batch_size:(k+1)*batch_size,],Y0_test[k*batch_size:(k+1)*batch_size]
                # 在batch上计算loss、acc
                self.test_step(_X, _Y)

        # 最终的loss和acc
        return self.test_loss.result().numpy(), self.test_accuracy.result().numpy()

    def record(self, model, train_data, test_data, train_loss, train_acc, test_loss, test_acc):
        # 记录当前模型在测试集训练集上的loss与acc
        _loss, _acc = self.test(model, 2000, train_data[0], train_data[1])
        _loss_test, _acc_test = self.test(model, 2000, test_data[0], test_data[1])
        train_loss.append(_loss)
        train_acc.append(_acc)
        test_loss.append(_loss_test)
        test_acc.append(_acc_test)   

    def get_batch_flow(self, data_flow):
        # 获取单个batch的数据
        for flow in data_flow:
            _X, _Y = flow
            break
        return _X, _Y
        
    def test_flow(self, _model, data_flow):
        # 测试在训练集上的loss、ACC
        # reset
        self.test_loss.reset_states()
        self.test_accuracy.reset_states()

        for k in range(len(data_flow)):
            if not self.pause:
                _X,_Y = self.get_batch_flow(data_flow)
                # 在batch上计算loss、acc
                self.test_step(_X, _Y)
        # 最终的loss和acc
        return self.test_loss.result().numpy(), self.test_accuracy.result().numpy()
    
    def flow_record(self, model, train_flow, test_flow, train_loss, train_acc, test_loss, test_acc):
        # 记录当前模型在测试集训练集上的loss与acc - generator版本
        _loss, _acc = self.test_flow(model, train_flow)
        _loss_test, _acc_test = self.test_flow(model, test_flow)
        train_loss.append(_loss)
        train_acc.append(_acc)
        test_loss.append(_loss_test)
        test_acc.append(_acc_test)  
        
    def __init__(self, 
                model=None, 
                epochs=200, 
                batch_size=64, 
                is_log=True,
                train=None,
                validation=None,
                loss = 'sparse_categorical_crossentropy',
                optimizer='SGD',
                test_accuracy = None,
                lr_default = 0.01,
                lqa = True
                ):
        # 初始化方法
        self.batch_size = batch_size
        self.model = model
        self.train = train
        self.validation = validation
        self.is_lqa = lqa
        self.optimizer = tf.keras.optimizers.get(self.name_map(optimizer))
        self.pause = False
        if self.name_map(optimizer) == 'SGD':
            self.lqa_init = 0.05
            self.lqa_upper = 0.01
            self.lqa_bound = 0.45    
        else:
            self.lqa_init = 0.0002
            self.lqa_upper = 0.0001
            self.lqa_bound = 0.0005
        if optimizer in ['adam', 'ADAM']:
            print('Momentum based optimizers are unsupported in the current version, but will be supported in the future release. Please use a standard SGD optimizer.')
            self.pause = True
        self.optimizer.lr = lr_default
        self.loss = keras.losses.get(loss)
        self.lqa_loss = keras.losses.get(loss)
        if type(loss) == str and 'sparse' in loss:
            self.test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')
        else:
            self.test_accuracy = tf.keras.metrics.CategoricalAccuracy(name='test_accuracy')
        
        if self.is_lqa:
            self.lqa_init = self.delta_init()
            self.lqa_upper = self.lqa_init * 0.02
            self.lqa_bound = self.lqa_init * 10
        
        if self.model == None:
            print('Model is not defined!')
        else:
            # 直接开始训练
            self.model, self.history = self.fit(epochs, batch_size, is_log)

   
    # 给定一个batch的数据，利用batch数据单次迭代训练方法
    @tf.function
    def train_step_grads(self, _X, _Y):
        try:         
            with tf.GradientTape() as tape:
                Y_pred = self.model(_X, training=True)                                                         
                loss = self.loss(y_true=_Y, y_pred=Y_pred)    
                loss = tf.reduce_mean(loss)
            grads = tape.gradient(loss, self.model.trainable_variables)
            return loss, grads
        except Exception as e:
            print(e)
            print('If you are using TensorFlow 2, please import your layers from [ tensorflow.keras ] ( instead of [keras] ).')
            print('* For example:')
            print('from tensorflow.keras.layers import Conv2D,Dense,Flatten,Input,MaxPooling2D')
            print('from tensorflow.keras import Model')
            self.pause = True
        

    # 给定一个batch的数据，测试loss、acc的方法   
    @tf.function
    def test_step(self, _X, _Y):
        try: 
            Y_pred = self.model(_X, training=False)
            t_loss = self.loss(_Y, Y_pred)
            self.test_loss(t_loss)
            self.test_accuracy(_Y, Y_pred)
        except Exception as e:
            print(e)
            print('If you are using TensorFlow 2, please import your layers from [ tensorflow.keras ] ( instead of [keras] ).')
            print('* For example:')
            print('from tensorflow.keras.layers import Conv2D,Dense,Flatten,Input,MaxPooling2D')
            print('from tensorflow.keras import Model')
            self.pause = True
            
    def delta_init(self):
        # 选取较好的initial delta0
        
        _output = sys.stdout
        shows = ['/', '-', '\\']
        cnt = 0
        _output.write('\rLQA is initializing %s' % shows[cnt])
        
        input_train_type = type(self.train)
        if input_train_type == list:
            # 输入为列表，包含X、Y
            [X0, Y0] = self.train
        else:
            if 'Iterator' in str(input_train_type):
                # 输入为generator.flow
                self.is_flow = True
            else:
                print('Wrong input.')
                self.pause = True
                
        # 声明LQA对象实例
        _lqa = lqa_delta()
        _lqa.loss = self.lqa_loss
        _lqa.upper = self.lqa_upper
        _lqa.bound = self.lqa_bound
        
        init_weights = copy.deepcopy(self.model.get_weights())
        
        res = []
        init_state = {}
        
        for test_delta in [0.05, 0.02, 0.01, 0.001]:
            _lqa.init = test_delta
            _losses = []   
            
            for i in range(10):
                if not self.is_flow:
                    k = int( len(X0) / self.batch_size * random.random() )
                    _X,_Y = X0[k*batch_size:(k+1)*batch_size,],Y0[k*batch_size:(k+1)*batch_size]
                else:
                    _X,_Y = self.get_batch_flow(self.train)

                # 获取当前梯度
                loss, grads = self.train_step_grads(_X, _Y)
               
                # 计算基于LQA的学习率
                delta_lqa = _lqa.delta(loss, self.model, _X, _Y, grads, 0)

                # 将LQA学习率输入给优化器
                self.optimizer.lr = delta_lqa

                # 调用优化器更新模型参数估计
                self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))   

                Y_pred = self.model(_X, training=False)                                                         
                _loss = self.loss(y_true=_Y, y_pred=Y_pred)    
                _loss = tf.reduce_mean(_loss)
                _losses.append(_loss)
                
                cnt = (cnt+1) % len(shows)
                _output.write('\rLQA is initializing %s' % shows[cnt])
            init_state[test_delta] = copy.deepcopy(self.model.get_weights())
            self.model.set_weights(init_weights)
            
            _losses = np.array(_losses)
            res.append( (np.median(_losses), test_delta) )
        
        res = sorted(res)
        #print(res)
        better_delta = res[0][1]
        self.model.set_weights(init_state[better_delta])
        _output.write('\rLQA initialized.                \n')
        return better_delta
            
    def fit(self, epochs=200, batch_size=64, is_log=True):
        # 开始训练
        self.is_flow = False
        
        # 训练集、测试集
        input_train_type = type(self.train)
        #print('Input type:', input_train_type)
        if input_train_type == list:
            # 输入为列表，包含X、Y
            [X0, Y0] = self.train
            [X1, Y1] = self.validation
            X0 = X0.astype(np.float32)
            X1 = X1.astype(np.float32)
        else:
            if 'Iterator' in str(input_train_type):
                # 输入为generator.flow
                self.is_flow = True
            else:
                print('Wrong input.')
                self.pause = True
        
        if is_log:
                log_file = 'log'
                self.log_refresh(log_file)
        
        # loss和acc计算
        self.test_loss = tf.keras.metrics.Mean(name='test_loss')
        #self.test_accuracy = test_accuracy(name='test_accuracy')       
        
        # 初始化loss和acc
        self.test_loss.reset_states()
        self.test_accuracy.reset_states()


        # 声明LQA对象实例
        _lqa = lqa_delta()
        _lqa.loss = self.lqa_loss
        _lqa.init = self.lqa_init
        _lqa.upper = self.lqa_upper
        _lqa.bound = self.lqa_bound

        # 记录初始的loss、acc
        losses = []
        accs = []
        losses_test = []
        accs_test = []
        time_pointer = 0.0
        time_points = []
           
        if not self.pause:
            '''
            # 记录初始loss、acc     
            if not self.is_flow:
                self.record(self.model, [X0, Y0], [X1, Y1], losses, accs, losses_test, accs_test)
            else:
                self.flow_record(self.model, self.train, self.validation, losses, accs, losses_test, accs_test)
            if is_log:
                self.log(log_file, '* Initial. Loss: %.4f. ACC: %.4f. Loss_test: %.4f. ACC_test: %.4f.' % 
                      (losses[-1], accs[-1], losses_test[-1], accs_test[-1]))
            '''

            # batch个数数
            if not self.is_flow:
                K = int(len(X0)/batch_size)
            else:
                K = len(self.train)
            #K = max(K, 100)

            # 迭代训练
            for epoch in range(epochs):
                print('Epoch %d/%d' % (epoch+1,epochs))
                # 输出显示位
                _output = sys.stdout
                t0 = time.time()
                for k in range(K):
                    # 获取单个batch的数据
                    if not self.is_flow:
                        _X,_Y = X0[k*batch_size:(k+1)*batch_size,],Y0[k*batch_size:(k+1)*batch_size]
                    else:
                        _X,_Y = self.get_batch_flow(self.train)

                    # 获取当前梯度
                    loss, grads = self.train_step_grads(_X, _Y)

                    
                    if self.is_lqa:
                        # 计算基于LQA的学习率
                        delta_lqa = _lqa.delta(loss, self.model, _X, _Y, grads, epoch)

                        # 将LQA学习率输入给优化器
                        self.optimizer.lr = delta_lqa

                    # 调用优化器更新模型参数估计
                    self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))  
                    
                    # 显示进度条
                    _show = '['
                    _temp_pos = int(float(k+1)/K*40)
                    for _ in range(_temp_pos):
                        _show += '='
                    if _temp_pos==40:
                        _show += '='
                    else:
                        _show += '>'
                    for _ in range(_temp_pos, 40):
                        _show += ' '
                    _show += ']'
                    status = float(k+1)/K*100
                    _output.write('\r %s (%.2f %%)' % (_show, status))

                # 记录loss、acc
                if not self.is_flow:
                    self.record(self.model, [X0, Y0], [X1, Y1], losses, accs, losses_test, accs_test)
                else:
                    self.flow_record(self.model, self.train, self.validation, losses, accs, losses_test, accs_test)
                    
                t1 = time.time()
                epoch_time_cost = t1-t0
                time_pointer += epoch_time_cost
                time_points.append(time_pointer)

                if is_log:
                    self.log(log_file, 'Loss: %.4f. ACC: %.4f. Loss_val: %.4f. ACC_val: %.4f. Time cost: %.2fs' % 
                          (losses[-1], accs[-1], losses_test[-1], accs_test[-1], epoch_time_cost))    
                    
        # 将中间信息打包成json
        history = {
            'train_loss': losses,
            'train_acc': accs,
            'val_loss': losses_test,
            'val_acc': accs_test,
            'time_points': time_points
        }
        
        return self.model, history
        
    


class lqa_delta(object):
    # 计算学习率
    
    # 默认的loss function
    loss = tf.keras.losses.sparse_categorical_crossentropy
    
    # 内置优化器，用于在当前参数估计附近作小范围变动，进而计算loss
    _optimizer = tf.keras.optimizers.SGD(learning_rate=0.1) 
    
    @tf.function
    def get_loss(self, _model, _X, _Y):
        # 计算模型给定参数估计下的loss
        Y_pred = _model(_X, training=False)   
        t_loss = self.loss(y_true=_Y, y_pred=Y_pred)
        loss = tf.reduce_mean(t_loss)      
        return loss

    def grad_add(self, grads1, grads2):
        # 合并两个grad（两个梯度相加）
        for i in range(len(grads1)):
            grads1[i] = grads1[i] + grads2[i]
        return grads1

    def grad_scale(self, grads, scale):
        # 对梯度每层乘以一个数值 scale
        for i in range(len(grads)):
            grads[i] = grads[i] * scale
        return grads

    def update_weights(self, var, grads, delta):
        # 计算参数+梯度*delta
        for i in range(len(var)):
            var[i] = var[i] + delta * grads[i]
        return var

    def get_ab(self, loss0, model, x, y, grads, delta_try):
        # 计算lqa、BB中共同部分的项
        
        # 计算loss_p（loss(θ+δ_0)）
        #self._optimizer.lr = delta_try
        #self._optimizer.apply_gradients(grads_and_vars=zip(grads, model.trainable_variables)) 
        model.set_weights( self.update_weights(model.trainable_variables, grads, delta_try) )
        loss_p = self.get_loss(model, x, y)      

        # 计算loss_n（loss(θ-δ_0)）
        #self._optimizer.lr = -2*delta_try
        #self._optimizer.apply_gradients(grads_and_vars=zip(grads, model.trainable_variables)) 
        model.set_weights( self.update_weights(model.trainable_variables, grads, -2*delta_try) )
        loss_n = self.get_loss(model, x, y)

        # * 复原模型参数估计
        #self._optimizer.lr = delta_try
        #self._optimizer.apply_gradients(grads_and_vars=zip(grads, model.trainable_variables)) 

        _e = 1e-7
        _term = (loss_p - loss_n) / ( 2.0 * (loss_p + loss_n - 2.0*loss0) + _e )
        
        return _term.numpy()

    # LQA方法
    # 尝试的学习率 δ_0
    #@tf.function
    def delta(self, loss0, model, x, y, grads, epoch):
        # 基于当前loss值，计算lqa学习率

        # 设置尝试性学习率，用于产生当前参数估计附近的loss值，进而计算LQA学习率
        delta_try = max(self.init * (1-epoch*0.01), self.upper)
        # 计算LQA学习率
        delta_lqa = delta_try * self.get_ab(loss0, model, x, y, grads, delta_try)

        # 若计算学习率为负，可能为局部（或近似的局部）非凸，替换为默认学习率
        if delta_lqa <= 0 or np.isnan(delta_lqa):
            delta_lqa = delta_try * 1.05
        
        # 若计算学习率过大，替换为默认学习率
        if delta_lqa > self.bound:
            delta_lqa = self.init
            if epoch >= 50:
                delta_lqa = self.init * 0.1
        
        # * 需考虑复原模型参数估计
        delta_lqa = abs(delta_lqa)+delta_try
        return abs(delta_lqa)
    
    
    