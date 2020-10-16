from rakpy.protocol.BitFlags import BitFlags
from rakpy.protocol.EncapsulatedPacket import EncapsulatedPacket
from rakpy.protocol.Packet import Packet

class DataPacket(Packet):
    id = BitFlags.Valid | 0

    packets = []
    sequenceNumber = None
    
    def encodePayload(self):
        self.putLTriad(self.sequenceNumber)
        for packet in self.packets:
            self.put(packet.toBinary() if isinstance(packet, EncapsulatedPacket) else packet.buffer)
        
    def decodePayload(self):
        self.sequenceNumber = self.getLTriad()
        while not self.feof():
            self.packets.append(EncapsulatedPacket().fromBinary(self.getBuffer()))
            
    def length(self):
        length = 4
        for packet in self.packets:
            length += packet.getTotalLength() if isinstance(packet, EncapsulatedPacket) else len(packet.getBuffer())
        return length
