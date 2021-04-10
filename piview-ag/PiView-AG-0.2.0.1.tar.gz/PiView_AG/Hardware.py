import subprocess

class Hardware:
    def get_bt(self):
        """
        Check if Bluetooth module is enabled

        :return: boolean
        """
        bt = False
        try:
            c = subprocess.Popen("lsmod", stdout=subprocess.PIPE)
            gr = subprocess.Popen(["grep", "bluetooth"], stdin=c.stdout,
                                  stdout=subprocess.PIPE)
            output = gr.communicate()[0]
            if output[:9] == 'bluetooth':
                bt = True
        except:
            pass
        return bt


    def get_spi(self):
        """
        Check if SPI bus is enabled by checking for spi_bcm2 modules

        :return: boolean
        """
        spi = False
        try:
            c = subprocess.Popen("lsmod", stdout=subprocess.PIPE)
            gr = subprocess.Popen(["grep", "spi_bcm2"], stdin=c.stdout,
                                  stdout=subprocess.PIPE)
            output = gr.communicate()[0]
            if output[:8] == 'spi_bcm2':
                spi = True
        except:
            pass
        return spi

    def get_i2c(self):
        """
        Check if I2C bus is enabled by checking for i2c_bcm2 modules

        :return: boolean
        """
        i2c = False
        try:
            c = subprocess.Popen("lsmod", stdout=subprocess.PIPE)
            gr = subprocess.Popen(["grep", "i2c_bcm2"], stdin=c.stdout,
                                  stdout=subprocess.PIPE)
            output = gr.communicate()[0]
            if output[:8] == 'i2c_bcm2':
                i2c = True
        except:
            pass
        return i2c
