//
//  Binary.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/15/21.
//

import Foundation

class BinaryDigits : CustomStringConvertible {
    var bits: [Int]
    
    init() {
        self.bits = []
    }
    
    init(_ bits: [Int]) {
        self.bits = bits
    }
    
    var description: String {
        "Binary[\(bits.map{$0.description}.joined(separator: ""))]"
    }
    
    func intRepr() -> Int {
            bits.reversed().enumerated().map { (index, digit) in
                //print("index \(index) digit \(digit)")
                return digit * twoToThePowerOf(index)
            }.sum()
    }
    
    func pop(n: Int) -> BinaryDigits {
        let ret = BinaryDigits(bits[...(n-1)].map{$0})
        bits.removeFirst(n)
        // print("popped \(n) bits -> \(ret) [\(n < 16 ? ret.intRepr() : -1)]")
        return ret
    }
    
    func append(bits: BinaryDigits) {
        self.bits.append(contentsOf: bits.bits)
    }
    
    static func from(hex: String) -> BinaryDigits {
        BinaryDigits(hex.flatMap { (char:Character)->[Int] in
            switch char {
            case "0":
                return [0, 0, 0, 0]
            case "1":
                return [0, 0, 0, 1]
            case "2":
                return [0, 0, 1, 0]
            case "3":
                return [0, 0, 1, 1]
            case "4":
                return [0, 1, 0, 0]
            case "5":
                return [0, 1, 0, 1]
            case "6":
                return [0, 1, 1, 0]
            case "7":
                return [0, 1, 1, 1]
            case "8":
                return [1, 0, 0, 0]
            case "9":
                return [1, 0, 0, 1]
            case "A":
                return [1, 0, 1, 0]
            case "B":
                return [1, 0, 1, 1]
            case "C":
                return [1, 1, 0, 0]
            case "D":
                return [1, 1, 0, 1]
            case "E":
                return [1, 1, 1, 0]
            case "F":
                return [1, 1, 1, 1]
            default:
                return []
            }
        })
    }
}
