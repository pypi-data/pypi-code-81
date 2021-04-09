import Pyro5.api
import TimeTagger as TT


def proxy2object(daemon: Pyro5.api.Daemon, proxy):
    """Returns the object for given proxy."""
    objectId = proxy._pyroUri.object
    return daemon.objectsById.get(objectId)


class IteratorBase():
    def __init__(self, tagger, args, kwargs):
        assert isinstance(tagger, TimeTaggerBase)
        TTClass = getattr(TT, type(self).__name__)
        self._obj = TTClass(tagger._obj, *args, **kwargs)


@Pyro5.api.expose
class VirtualChannelBase(IteratorBase):
    pass


@Pyro5.api.expose
class DelayedChannel(VirtualChannelBase):
    _obj: TT.DelayedChannel

    def getChannel(self):
        return self._obj.getChannel()

    def setDelay(self, delay):
        return self._obj.setDelay(delay)


@Pyro5.api.expose
class GatedChannel(VirtualChannelBase):
    _obj: TT.GatedChannel

    def getChannel(self):
        return self._obj.getChannel()


@Pyro5.api.expose
class Coincidence(VirtualChannelBase):
    _obj: TT.Coincidence

    def getChannel(self):
        return self._obj.getChannel()


@Pyro5.api.expose
class Coincidences(VirtualChannelBase):
    _obj: TT.Coincidences

    def getChannels(self):
        return self._obj.getChannels()


@Pyro5.api.expose
class MeasurementBase(IteratorBase):
    _obj: TT.IteratorBase

    def start(self):
        return self._obj.start()

    def startFor(self, capture_duration, clear):
        return self._obj.startFor(capture_duration, clear=clear)

    def stop(self):
        return self._obj.stop()

    def clear(self):
        return self._obj.clear()

    def isRunning(self):
        return self._obj.isRunning()

    def getCaptureDuration(self):
        return self._obj.getCaptureDuration()

    def waitUntilFinished(self, timeout):
        return self._obj.waitUntilFinished(timeout=timeout)


@Pyro5.api.expose
class Histogram(MeasurementBase):
    _obj: TT.Histogram

    def getIndex(self):
        return self._obj.getIndex().tolist()

    def getData(self):
        return self._obj.getData().tolist()


@Pyro5.api.expose
class Histogram2D(MeasurementBase):
    _obj: TT.Histogram2D

    def getIndex(self):
        return self._obj.getIndex().tolist()

    def getIndex_1(self):
        return self._obj.getIndex_1().tolist()

    def getIndex_2(self):
        return self._obj.getIndex_2().tolist()

    def getData(self):
        return self._obj.getData().tolist()


@Pyro5.api.expose
class HistogramLogBins(MeasurementBase):
    _obj: TT.HistogramLogBins

    def getBinEdges(self):
        return self._obj.getBinEdges().tolist()

    def getData(self):
        return self._obj.getData().tolist()

    def getDataNormalizedCountsPerPs(self):
        return self._obj.getDataNormalizedCountsPerPs().tolist()

    def getDataNormalizedG2(self):
        return self._obj.getDataNormalizedG2().tolist()


@Pyro5.api.expose
class Correlation(MeasurementBase):
    _obj: TT.Correlation

    def getIndex(self):
        return self._obj.getIndex().tolist()

    def getData(self):
        return self._obj.getData().tolist()

    def getDataNormalized(self):
        return self._obj.getDataNormalized().tolist()


@Pyro5.api.expose
class Counter(MeasurementBase):
    _obj: TT.Counter

    def getData(self):
        return self._obj.getData().tolist()

    def getIndex(self):
        return self._obj.getIndex().tolist()


@Pyro5.api.expose
class Countrate(MeasurementBase):
    _obj: TT.Countrate

    def getCountsTotal(self):
        return self._obj.getCountsTotal().tolist()

    def getData(self):
        return self._obj.getData().tolist()


@Pyro5.api.expose
class CountBetweenMarkers(MeasurementBase):
    _obj: TT.CountBetweenMarkers

    def getBinWidths(self):
        return self._obj.getBinWidths().tolist()

    def getIndex(self):
        return self._obj.getIndex().tolist()

    def getData(self):
        return self._obj.getData().tolist()

    def ready(self):
        return self._obj.ready()


class TimeDifferences(MeasurementBase):
    _obj: TT.TimeDifferences

    def getCounts(self):
        return self._obj.getCounts()

    def getIndex(self):
        return self._obj.getIndex().tolist()

    def getData(self):
        return self._obj.getData().tolist()

    def ready(self):
        return self._obj.ready()

    def setMaxCounts(self, max_counts):
        return self._obj.setMaxCounts(max_counts)


@Pyro5.api.expose
class SynchronizedMeasurements(IteratorBase):
    _obj: TT.SynchronizedMeasurements

    def registerMeasurement(self, measurement_proxy):
        measurement = proxy2object(self._pyroDaemon, measurement_proxy)
        return self._obj.registerMeasurement(measurement._obj)

    def unregisterMeasurement(self, measurement_proxy):
        measurement = proxy2object(self._pyroDaemon, measurement_proxy)
        return self._obj.unregisterMeasurement(measurement._obj)

    def start(self):
        return self._obj.start()

    def startFor(self, capture_duration, clear):
        return self._obj.startFor(capture_duration, clear=clear)

    def stop(self):
        return self._obj.stop()

    def clear(self):
        return self._obj.clear()

    def isRunning(self):
        return self._obj.isRunning()


@Pyro5.api.expose
class TimeTaggerBase(IteratorBase):
    _obj: TT.TimeTaggerBase

    def __init__(self, args, kwargs) -> None:
        raise NotImplementedError(
            'TimeTaggerBase is abstract and shall not be instantiated directly'
        )

    def setTestSignal(self, *args):
        return self._obj.setTestSignal(*args)

    def setInputDelay(self, channel, delay):
        return self._obj.setInputDelay(channel, delay)

    def setDeadtime(self, channel, deadtime):
        return self._obj.setDeadtime(channel, deadtime)

    def setDelayHardware(self, channel, delay):
        return self._obj.setDelayHardware(channel, delay)

    def setDelaySoftware(self, channel, delay):
        return self._obj.setDelaySoftware(channel, delay)

    def getInputDelay(self, channel):
        return self._obj.getInputDelay(channel)

    def getDelaySoftware(self, channel):
        return self._obj.getDelaySoftware(channel)

    def getDelayHardware(self, channel):
        return self._obj.getDelayHardware(channel)

    def getTestSignal(self, channel):
        return self._obj.getTestSignal(channel)

    def getOverflowsAndClear(self):
        return self._obj.getOverflowsAndClear()

    def getOverflows(self):
        return self._obj.getOverflows()

    def clearOverflows(self):
        return self._obj.clearOverflows()

    def getDeadtime(self, channel):
        return self._obj.getDeadtime(channel)

    def sync(self, timeout):
        return self._obj.sync(timeout=timeout)

    def getConfiguration(self):
        return self._obj.getConfiguration()


@Pyro5.api.expose
class TimeTagger(TimeTaggerBase):
    """Adapter for the TimeTagger class"""
    _obj: TT.TimeTagger

    def __init__(self, args, kwargs):
        self._obj = TT.createTimeTagger(*args, **kwargs)

    def setTriggerLevel(self, channel, voltage):
        return self._obj.setTriggerLevel(channel, voltage)

    def getTriggerLevel(self, channel):
        return self._obj.getTriggerLevel(channel)

    def getSerial(self):
        return self._obj.getSerial()

    def getModel(self):
        return self._obj.getModel()

    def getSensorData(self):
        return self._obj.getSensorData()

    def getDACRange(self):
        return self._obj.getDACRange()


@Pyro5.api.expose
class TimeTaggerRPC:
    """Adapter for the Time Tagger Library"""

    def _instantiate(self, PyroClass: type, tagger_proxy, args, kwargs):
        tagger_obj = proxy2object(self._pyroDaemon, tagger_proxy)
        pyro_obj = PyroClass(tagger_obj, args, kwargs)
        self._pyroDaemon.register(pyro_obj)
        return pyro_obj

    @property
    def CHANNEL_UNUSED(self):
        return TT.CHANNEL_UNUSED

    def scanTimeTagger(self):
        """Return the serial numbers of the available Time Taggers."""
        return TT.scanTimeTagger()

    def createTimeTagger(self, *args, **kwargs):
        """Create the Time Tagger."""
        tagger = TimeTagger(args, kwargs)
        self._pyroDaemon.register(tagger)
        return tagger

    def freeTimeTagger(self, tagger_proxy):
        tagger = proxy2object(self._pyroDaemon, tagger_proxy)
        self._pyroDaemon.unregister(tagger)
        return TT.freeTimeTagger(tagger._obj)

    def SynchronizedMeasurements(self, tagger_proxy):
        return self._instantiate(SynchronizedMeasurements, tagger_proxy, [], {})

    def Histogram(self, tagger_proxy, *args, **kwargs):
        """Create Histogram measurement."""
        return self._instantiate(Histogram, tagger_proxy, args, kwargs)

    def DelayedChannel(self, tagger_proxy, *args, **kwargs):
        """Create DelayedChannel."""
        return self._instantiate(DelayedChannel, tagger_proxy, args, kwargs)

    def Correlation(self, tagger_proxy, *args, **kwargs):
        return self._instantiate(Correlation, tagger_proxy, args, kwargs)

    def Coincidence(self, tagger_proxy, *args, **kwargs):
        return self._instantiate(Coincidence, tagger_proxy, args, kwargs)

    def Coincidences(self, tagger_proxy, *args, **kwargs):
        return self._instantiate(Coincidences, tagger_proxy, args, kwargs)

    def GatedChannel(self, tagger_proxy, *args, **kwargs):
        return self._instantiate(GatedChannel, tagger_proxy, args, kwargs)

    def Histogram2D(self, tagger_proxy, *args, **kwargs):
        return self._instantiate(Histogram2D, tagger_proxy, args, kwargs)

    def HistogramLogBins(self, tagger_proxy, *args, **kwargs):
        return self._instantiate(HistogramLogBins, tagger_proxy, args, kwargs)

    def TimeDifferences(self, tagger_proxy, *args, **kwargs):
        return self._instantiate(TimeDifferences, tagger_proxy, args, kwargs)

    def Countrate(self, tagger_proxy, *args, **kwargs):
        return self._instantiate(Countrate, tagger_proxy, args, kwargs)

    def Counter(self, tagger_proxy, *args, **kwargs):
        return self._instantiate(Counter, tagger_proxy, args, kwargs)

    def CountBetweenMarkers(self, tagger_proxy, *args, **kwargs):
        return self._instantiate(CountBetweenMarkers, tagger_proxy, args, kwargs)


def start_server(host='localhost', port=23000, use_ns=False, start_ns=False):
    
    # Start Pyro nameserver in a subprocess
    if start_ns:
        import subprocess
        ns_proc = subprocess.Popen(['python', '-m', 'Pyro5.nameserver', '-n', host])
    
    try:
        with Pyro5.api.Daemon(host=host, port=port) as daemon:
            # register the Pyro class
            uri = daemon.register(TimeTaggerRPC, 'TimeTagger')
            if use_ns:
                ns = Pyro5.api.locate_ns()         # find the name server
                # register the object with a name in the name server
                ns.register("TimeTagger", uri)
            # start the event loop of the server to wait for calls
            daemon.requestLoop()
    except KeyboardInterrupt:
        pass
    finally:
        if start_ns:
            ns_proc.terminate()


if __name__ == "__main__":
    start_server()
