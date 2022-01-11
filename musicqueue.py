class MusicQueue:

    def __init__(self) -> None:
        self.queue = []
        self.history = []
            
    def setQueue(self, queue):
        self.queue = queue

    def addToQueueEnd(self, track):
        if isinstance(track, list):
            self.queue.extend(track)
        else:
            self.queue.append(track)
    
    def addToQueueStart(self, track):
        if isinstance(track, list):
            self.queue[1:1] = track
        else:
            self.queue.insert(1, track)

    def getQueue(self):
        return self.queue

    def shuffleQueue(self):
        return

    def getNextInQueue(self):
        if len(self.queue) > 0:
            track = self.queue.pop(0)
            self.history.append(track)
            return track
        else:
            return None
