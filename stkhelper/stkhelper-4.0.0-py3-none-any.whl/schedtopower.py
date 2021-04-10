import sys, pandas

timePairs = []

def parse(csvFile):
	df = pandas.read_csv(csvFile)
	i = 0
	for x in range(len(df.index)):
		if (df.iloc[x,3] =='cruise'):
			timePairs.append([(df.iloc[x,0]),(df.iloc[x,1])])	

parse(sys.argv[1])
from stkhelper import application, scenario, satellite

app = application.Application()
scene = scenario.Scenario(app, 'powergen', '+24hrs')
MOCI = satellite.Satellite(scene, 'MOCI', 25544)

MOCI.SetModel('C:/Users/Supreme/Desktop/STKIntegration/Repository/stkhelper/stkhelper/stkhelper/4Cell.anc')
MOCI.SetAttitude('NadirOrbit')

for x in range (len(timePairs)):
    MOCI.GetPower(timePairs[x][0], timePairs[x][1], 10, 2.5, 'C:/Users/Supreme/Desktop/STKIntegration/Repository/stkhelper/stkhelper/stkhelper/test/pass' + str(x) + '.csv')
    
# from STKIntegration/Repository/stkhelper/stkhelper/stkhelper
# python schedtopower.py ../../../MOCIModesScheduling\schedule.csv