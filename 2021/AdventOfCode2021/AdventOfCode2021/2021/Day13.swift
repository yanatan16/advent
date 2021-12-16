//
//  Day13.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/13/21.
//

import Foundation

// start: 7:49
// part 1: 8:07 (8m)
// part 2: 8:12 (13m)
struct Day13 : Solution {
    var exampleRawInput: String { """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""}
    
    struct Dot : Hashable,CustomStringConvertible {
        let x: Int
        let y:Int
        
        init(_ x: Int, _ y: Int) {
            self.x = x
            self.y = y
        }
        
        var description: String {
            "Dot(\(x),\(y))"
        }
    }
    enum Fold {
        case alongX(Int)
        case alongY(Int)
    }
    struct Input {
        let dots: [Dot]
        let folds: [Fold]
    }
    
    typealias Output = Int
    
    func parseInput(_ raw: String) -> Input {
        let split = raw.split2lines()
        return Input(
            dots: split[0].splitlines().map { line in
                let s = line.components(separatedBy: ",").map { Int($0)! }
                return Dot(s[0], s[1])
            },
            folds: split[1].splitlines().map { line in
                if line.contains("fold along y=") {
                    return Fold.alongY(Int(line.components(separatedBy: "fold along y=")[1])!)
                } else {
                    return Fold.alongX(Int(line.components(separatedBy: "fold along x=")[1])!)
                }
            }
        )
    }
    
    func fold(dots: Set<Dot>, fold: Fold) -> Set<Dot> {
        switch fold {
        case .alongX(let xfold):
            let foldedDots:[Dot] = dots.compactMap { dot in
                if dot.x == xfold {
                    return nil // No longer visible
                } else if dot.x < xfold {
                    return dot // not moved
                } else {
                    return Dot(xfold - (dot.x - xfold), dot.y)
                }
            }
            return Set(foldedDots)
        case .alongY(let yfold):
            let foldedDots:[Dot] = dots.compactMap { dot in
                if dot.y == yfold {
                    return nil // No longer visible
                } else if dot.y < yfold {
                    return dot // not moved
                } else {
                    return Dot(dot.x, yfold - (dot.y - yfold))
                }
            }
            return Set(foldedDots)
        }
    }
    
    func problem1(_ input: Input) -> Int {
        return fold(dots: Set(input.dots), fold: input.folds[0]).count
    }
    
    func problem2(_ input: Input) -> Int {
        let finalDots = input.folds.reduce(Set(input.dots), { (dots, fold) in
            self.fold(dots: dots, fold: fold)
        })
        
        let maxX = finalDots.map { $0.x }.max()!
        let maxY = finalDots.map { $0.y }.max()!
        
        let output:[[Character]] = (0...maxY).map { y in
            (0...maxX).map { x in
                if finalDots.contains(Dot(x,y)) {
                    return "#"
                } else {
                    return "."
                }
            }
        }
        
        print(output.map { String($0) }.joined(separator: "\n"))
        return -1
    }
}
