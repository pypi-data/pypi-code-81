def get_pwm(ppm_L,background_acgt = [0.25,0.25,0.25,0.25]):
    pwm_L = []
    for i in range(len(ppm_L)):
        pwm_L_sample = []
        for j in range(4):
            #这里加1e-3是防止结果中出现0
            #这里的问题在于，正向最多到2，而负向可以到-inf（很大的负数）
            #考虑如何改，或者直接用ppm？
            #这会有一些问题哦——————
            pwm_L_sample.append(list(np.log2((ppm_L[i][j]+1e-2)/background_acgt[j])))
        pwm_L.append(np.array(pwm_L_sample))
    return np.array(pwm_L) 