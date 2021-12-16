//
//  Day16.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/15/21.
//

import Foundation

struct Day16 : Solution {
    var exampleRawInput: String { """
38006F45291200
"""}
    
    enum Packet {
        case literal(version: Int, type: Int, value: Int)
        case op(version: Int, type: Int, packets: [Packet])
    }
    
    typealias Input = Packet
    typealias Output = Int
    
    func parsePacket(bits b: BinaryDigits) -> Packet {
        let version = b.pop(n: 3).intRepr()
        let type = b.pop(n: 3).intRepr()
        
        switch type {
        case 4:
            let value = BinaryDigits()
            while true {
                let groupPrefix = b.pop(n: 1).intRepr()
                let valueBits = b.pop(n: 4)
                value.append(bits: valueBits)
                if groupPrefix == 0 {
                    break
                }
            }
            return .literal(
                version: version,
                type: type,
                value: value.intRepr()
            )
        default:
            let lengthTypeId = b.pop(n: 1).intRepr()
            var packets:[Packet] = []
            if lengthTypeId == 0 {
                let packetLength = b.pop(n: 15).intRepr()
                
                let packetPayload = b.pop(n: packetLength)
                while packetPayload.bits.count > 0 {
                    packets.append(parsePacket(bits: packetPayload))
                }
            } else {
                let nPackets = b.pop(n: 11).intRepr()
                
                (1...nPackets).forEach { _ in
                    packets.append(parsePacket(bits: b))
                }
            }
            return .op(
                version: version,
                type: type,
                packets: packets
            )
        }
    }
    
    func parseInput(_ raw: String) -> Input {
        let bits = BinaryDigits.from(hex: raw.splitlines()[0])
        return parsePacket(bits: bits)
    }
    
    func problem1(_ input: Input) -> Int {
        switch input {
        case .literal(let version,_,_):
            return version
        case .op(let version, _, let packets):
            return version + packets.map(problem1).sum()
        }
    }
    
    func eval(_ p: Packet) -> Int {
        switch p {
        case .literal(version: _, type: _, value: let value):
            return value
        case .op(version: _, type: let type, packets: let packets):
            switch type {
            case 0: // sum
                return packets.map(eval).sum()
            case 1: // product
                return packets.map(eval).product()
            case 2: // min
                return packets.map(eval).min()!
            case 3: // max
                return packets.map(eval).max()!
            case 5: // greater than
                if eval(packets[0]) > eval(packets[1]) {
                    return 1
                } else {
                    return 0
                }
            case 6: // less than
                if eval(packets[0]) < eval(packets[1]) {
                    return 1
                } else {
                    return 0
                }
            case 7: // equal to
                if eval(packets[0]) == eval(packets[1]) {
                    return 1
                } else {
                    return 0
                }
            default:
                return -1
            }
        }
    }
    func problem2(_ input: Input) -> Int {
        eval(input)
    }
}
