from typing import Union

class Location:
    def __init__(self, pos: dict[str, float], name: str, address: str, times: dict[str, str], google: str, waze: str) -> None:
        self.pos = pos
        self.name = name
        self.address = address
        self.times = times
        self.google = google
        self.waze = waze
        
    @classmethod
    def fromDict(cls, loc: dict[str, Union[dict[str,float], str, dict[str,str]]]):
        return cls(
            pos=loc['pos'],
            name=loc['name'],
            address=loc['address'],
            times=loc['times'],
            google=loc['google'],
            waze=loc['waze']
        )
        
    def getPos(self):
        return {'lat': self.getLat(), 'lng': self.getLng()}
    
    def getLat(self):
        if self.pos is not None and self.pos['lat'] is not None:
            return self.pos['lat']
        return 0
    
    def getLng(self):
        if self.pos is not None and self.pos['lng'] is not None:
            return self.pos['lng']
        return 0
    
    def getName(self):
        if self.name is not None:
            return self.name
        return ''
    
    def getAddress(self):
        if self.address is not None:
            return self.address
        return ''
    
    def getTimes(self):
        return {'standard': self.getStandardTimes(), 'special': self.getSpecialTimes()}
    
    def getStandardTimes(self):
        if self.times is not None and self.times['standard'] is not None:
            return self.times['standard']
        return ''
    
    def getSpecialTimes(self):
        if self.times is not None and self.times['special'] is not None:
            return self.times['special']
        return ''
    
    def getGoogle(self):
        if self.google is not None:
            return self.google
        return ''
    
    def getWaze(self):
        if self.waze is not None:
            return self.waze
        return ''
    
    def toJSON(self):
        return {
            'pos': self.getPos(),
            'name': self.getName(),
            'address': self.getAddress(),
            'times': self.getTimes(),
            'google': self.getGoogle(),
            'waze': self.getWaze(),
        }
        
    def __repr__(self) -> str:
        return f'{{\n\tPos: {self.getPos()}\n\tName: {self.getName()}\n\tAddress: {self.getAddress()}\n\tTimes: {self.getTimes()}\n\tGoogle: {self.getGoogle()}\n\tWaze: {self.getWaze()}\n}}'