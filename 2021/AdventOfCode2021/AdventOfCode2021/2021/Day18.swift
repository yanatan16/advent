//
//  Day18.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/17/21.
//

import Foundation

// start: 3:27
// part 1: 4:25 (58m)
// part 2: 4:30 (63m)
struct Day18 : Solution {
    var exampleRawInput: String { """
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
"""}
    
    indirect enum SnailfishNumber : Equatable, CustomStringConvertible {
        case number(Int)
        case pair(x: SnailfishNumber, y: SnailfishNumber)
        
        var description: String {
            switch self {
            case .number(let n):
                return "\(n)"
            case .pair(let x, let y):
                return "[\(x),\(y)]"
            }
        }
        
        func items() -> [(ix: [Int], val: Int)] {
            switch self {
            case .number(let v):
                return [([], v)]
            case .pair(let x, let y):
                return x.items().map { (ix, v) in
                    ([0]+ix, v)
                } + y.items().map { (ix, v) in
                    ([1]+ix, v)
                }
            }
        }
        
        enum SnailfishError : Error {
            case setAtInvalid(num: SnailfishNumber, ix: [Int])
            case badParse(s: String, expected: String)
        }
        
        func setAt(ix: [Int], val: SnailfishNumber) throws -> SnailfishNumber {
            if ix.isEmpty {
                return val
            } else {
                switch self {
                case .number(_):
                    throw SnailfishError.setAtInvalid(num: self, ix: ix)
                    
                case .pair(let x, let y):
                    let i = ix.first!
                    let ixrest = ix.dropFirst().map{$0}
                    if i == 0 {
                        return .pair(x: try x.setAt(ix: ixrest, val: val), y: y)
                    } else {
                        return .pair(x: x, y: try y.setAt(ix: ixrest, val: val))
                    }
                }
            }
        }
        
        func reduceNestingOnce() throws -> (SnailfishNumber, Bool) {
            let items = self.items()
            for (item_i, item) in items.enumerated() {
                if item.ix.count == 5 {
                    var num = try self.setAt(ix: item.ix.dropLast(), val: .number(0))
                    
                    if item_i > 0 {
                        let x = item
                        let explodeLeft = items[item_i-1]
                        num = try num.setAt(ix: explodeLeft.ix, val: .number(explodeLeft.val + x.val))
                    }
                    
                    if item_i+2 < items.count {
                        let y = items[item_i+1]
                        let explodeRight = items[item_i+2]
                        num = try num.setAt(ix: explodeRight.ix, val: .number(explodeRight.val + y.val))
                    }
                    
                    return (num, true)
                }
            }
            return (self, false)
        }
        func reduce10Once() throws -> (SnailfishNumber, Bool) {
            for item in items() {
                if item.val >= 10 {
                    let x = Int(floor(Double(item.val) / 2.0))
                    let y = Int(ceil(Double(item.val) / 2.0))
                    let newNum = try setAt(ix: item.ix, val: .pair(x: .number(x), y: .number(y)))
                    return (newNum, true)
                }
            }
            return (self, false)
        }
        
        func reduce() throws -> SnailfishNumber {
            var num = self
            while true {
                let (reduced, actioned) = try num.reduceNestingOnce()
                if actioned {
                    // print("reduced nesting from \(num) to \(reduced)")
                    num = reduced
                    continue
                }
                let (reduced2, actioned2) = try num.reduce10Once()
                if actioned2 {
                    // print("reduced 10 from \(num) to \(reduced2)")
                    num = reduced2
                    continue
                }
                
                // no action, reduced
                return num
            }
        }
        
        static func +(lhs: SnailfishNumber, rhs: SnailfishNumber) throws -> SnailfishNumber {
            try .pair(x: lhs, y: rhs).reduce()
        }
        
        static func ==(lhs: SnailfishNumber, rhs: SnailfishNumber) -> Bool {
            switch (lhs, rhs) {
            case (.number(let a), .number(let b)):
                return a == b
            case (.pair(let ax, let ay), .pair(let bx, let by)):
                return ax == bx && ay == by
            default:
                return false
            }
        }
        
        static func parse(_ s: String) throws -> (SnailfishNumber, String) {
            if s.starts(with:"[") {
                let (x, rest) = try parse(String(s.dropFirst()))
                if !rest.starts(with: ",") {
                    throw SnailfishError.badParse(s: rest, expected: ",")
                }
                
                let (y, rest2) = try parse(String(rest.dropFirst()))
                
                if !rest2.starts(with: "]") {
                    throw SnailfishError.badParse(s: rest2, expected: "]")
                }
                return (.pair(x:x, y:y), String(rest2.dropFirst()))
            } else {
                guard let ns = s.first else {
                    throw SnailfishError.badParse(s: s, expected: "d")
                }
                guard let n = Int(String(ns)) else {
                    throw SnailfishError.badParse(s: s, expected: "d")
                }
                return (.number(n), String(s.dropFirst()))
            }
        }
        
        var magnitude : Int {
            switch self {
            case .number(let n):
                return n
            case .pair(let x, let y):
                return 3 * x.magnitude + 2 * y.magnitude
            }
        }
    }
    
    typealias Input = [SnailfishNumber]
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        raw.splitlines().map { try! SnailfishNumber.parse($0).0 }
    }
    
    func problem1(_ input: Input) -> Int {
        return input.dropFirst().reduce(input.first!) {
            // print("Adding \($0) and \($1)")
            let result = try! $0 + $1
            // print("== \(result)")
            return result
        }.magnitude
    }
    
    func problem2(_ input: Input) -> Int {
        input.pairs().flatMap { (x,y) in
            [(try! x+y).magnitude, (try! y+x).magnitude]
        }.max()!
    }
    
}

struct Day18Rewrite : Solution {
    var exampleRawInput: String {
        Day18().exampleRawInput
    }
    
    struct SnailfishFast : CustomStringConvertible {
        typealias NumberAtDepth = (val: Int, depth: Int)
        var pairs: [NumberAtDepth]
        
        var description: String {
            pairs.description
        }
        
        var magnitude : Int {
            var rp = pairs
            while rp.count > 1 {
                var reduced = false
                // print("magnitude \(rp)")
                for i in rp.indices.dropFirst() {
                    if rp[i-1].depth == rp[i].depth {
                        rp[i-1] = (val: 3 * rp[i-1].val + 2 * rp[i].val, depth: rp[i].depth - 1)
                        rp.remove(at: i)
                        
                        reduced = true
                        break
                    }
                }
                if (!reduced) {
                    print("shouldnt get here \(rp)")
                }
            }
            return rp[0].val
        }
        
        static func +(lhs: SnailfishFast, rhs: SnailfishFast) -> SnailfishFast {
            var ret = SnailfishFast(pairs: (lhs.pairs + rhs.pairs).map { (val, depth) in
                (val: val, depth: depth+1)
            })
            return ret.reduce()
        }
        
        mutating func reduce() -> SnailfishFast {
            let depth5 = self.pairs.enumerated().filter { (i,pair) in pair.depth == 5 }
            if depth5.count > 0 {
                let (ix, xpair) = depth5.first!
                let (iy, ypair) = depth5.dropFirst().first!
                
                if ix > 0 {
                    let left = pairs[ix-1]
                    pairs[ix-1] = (val: left.val + xpair.val,
                                   depth: left.depth)
                }
                if iy < (pairs.count - 1) {
                    let right = pairs[iy+1]
                    pairs[iy+1] = (val: right.val + ypair.val,
                                   depth: right.depth)
                }
                pairs[ix] = (val: 0, depth: 4)
                pairs.remove(at: iy)
                
                return reduce()
            }
            
            let tens = self.pairs.enumerated().filter { (i, pair) in pair.val >= 10 }
            if let (i, ten) = tens.first {
                pairs[i] = (val: Int(floor(Double(ten.val) / 2.0)),
                            depth: ten.depth + 1)
                pairs.insert((val: Int(ceil(Double(ten.val) / 2.0)),
                              depth: ten.depth + 1)
                             , at: i+1)
                return reduce()
            }
            
            return self
        }
        
        static func fromSnailfishNumber(_ num: Day18.SnailfishNumber) -> SnailfishFast {
            SnailfishFast(pairs: num.items().map { (ix, val) in
                (val: val, depth: ix.count)
            })
        }
    }
    
    typealias Input = [SnailfishFast]
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        Day18().parseInput(raw).map(SnailfishFast.fromSnailfishNumber)
    }
    
    func problem1(_ input: Input) -> Int {
        return input.dropFirst().reduce(input.first!) {
            // print("Adding \($0) and \($1)")
            let result = $0 + $1
            // print("== \(result)")
            return result
        }.magnitude
    }
    
    func problem2(_ input: Input) -> Int {
        return input.pairs().flatMap { (x,y) in
            [(x+y).magnitude, (y+x).magnitude]
        }.max()!
    }
}
