//
//  Day8.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

struct Day8 : Solution {
    var exampleRawInput: String { """
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
"""}
    
    struct Line {
        let signals : [String]
        let output : [String]
    }
    typealias SignalMap = [Character:Character]
    typealias Input = [Line]
    
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        raw.splitlines().compactMap { line in
            if line.count == 0 {
                return nil
            }
            let split = line.components(separatedBy: " | ")
            return Line(signals: split[0].components(separatedBy: " "),
                        output: split[1].components(separatedBy: " "))
        }
    }
    
    func uniqueSignalCount(line: Line) -> Int {
        return line.output.filter { code in
            if code.count == 2 || code.count == 3 || code.count == 4 || code.count == 7 {
                return true
            } else {
                return false
            }
        }.count
    }
    
    func problem1(_ input: Input) -> Int {
        return input.map(uniqueSignalCount).sum()
    }
    
    func signalMap(line: Line) -> SignalMap {
        let signals = line.signals.map {
            Set($0.map{$0})
        }
        
        let one = signals.filter{ $0.count == 2 }.first!
        let four = signals.filter{ $0.count == 4 }.first!
        let seven = signals.filter{ $0.count == 3 }.first!
        
        let len5s = signals.filter{ $0.count == 5 }
        let len6s = signals.filter{ $0.count == 6 }
        
        // A is 7 - 1
        let a = seven.subtracting(one)
        
        // G is the single in the two sixes minus 4 and 7
        let g = len6s.map { len6 in
            len6.subtracting(four).subtracting(seven)
        }.filter { $0.count == 1 }.first!
        
        // e is the same operation subtracting g
        let e = len6s.map { len6 in
            len6.subtracting(four).subtracting(seven).subtracting(g)
        }.filter { $0.count == 1 }.first!
        
        // d is the intersection of all the 5's minus a and g
        let d = len5s.dropFirst()
            .reduce(len5s.first!) { (s, len5) in
                s.intersection(len5)
            }.subtracting(a).subtracting(g)
        
        // b is 4 - 1 - d
        let b = four.subtracting(one).subtracting(d)
        
        // f is only single after len6  - a b d e g
        let f = len6s.map { len6 in
            len6.subtracting(a)
                .subtracting(b)
                .subtracting(d)
                .subtracting(e)
                .subtracting(g)
        }.filter { $0.count == 1 }.first!
        
        // c is 1 - f
        let c = one.subtracting(f)

        return [
            a.first!: "a",
            b.first!: "b",
            c.first!: "c",
            d.first!: "d",
            e.first!: "e",
            f.first!: "f",
            g.first!: "g"
        ]
    }
    
    let CodeMap : [Set<Character>: Int] = [
        Set("abcefg"): 0,
        Set("cf"): 1,
        Set("acdeg"): 2,
        Set("acdfg"): 3,
        Set("bcdf"): 4,
        Set("abdfg"): 5,
        Set("abdefg"): 6,
        Set("acf"): 7,
        Set("abcdefg"): 8,
        Set("abcdfg"): 9
    ]
    
    func calc(line: Line, map: SignalMap) -> Int {
        line.output.map { code in
            let codeSet = Set(code.map { codedChar in map[codedChar]! })
            return CodeMap[codeSet]!
        }.fromDigits()
    }
    
    func problem2(_ input: Input) -> Int {
        input.map { line in
            calc(line: line, map: signalMap(line: line))
        }.sum()
    }
}

extension Array where Element == Int {
    func fromDigits() -> Int {
        let v = reversed().enumerated().map { (i, n) in
            n * Int(pow(10.0, Double(i)))
        }.sum()
        print("fromDigits \(self) \(v)")
        return v
    }
}
