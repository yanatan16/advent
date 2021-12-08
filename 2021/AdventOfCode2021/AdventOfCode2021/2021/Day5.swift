//
//  Day5.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/6/21.
//

import Foundation

struct Day5 : Solution {
    var exampleRawInput:String { """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""" }
    
    struct Point : Hashable {
        let x:Int
        let y: Int
        
        init(_ x :Int, _ y:Int) {
            self.x = x
            self.y = y
        }
    }
    
    
    struct Vector : CustomStringConvertible {
        let p1: Point
        let p2: Point
        init(_ p1: Point, _ p2: Point) {
            self.p1 = p1
            self.p2 = p2
        }
        
        func isHoriz() -> Bool {
            p1.x == p2.x
        }
        func isVert() -> Bool {
            p1.y == p2.y
        }
        func isDiagnol() -> Bool {
            p1.x != p2.x && p1.y != p2.y
        }
        func rows() -> [Int] {
            if (p1.x > p2.x) {
                return (p2.x ... p1.x).map{$0}.reversed()
            } else {
                return (p1.x ... p2.x).map{$0}
            }
        }
        func cols() -> [Int] {
            if (p1.y > p2.y) {
                return (p2.y ... p1.y).map{$0}.reversed()
            } else {
                return (p1.y ... p2.y).map{$0}
            }
        }
        func points() -> [Point] {
            if (isHoriz()) {
                return cols().map { Point(p1.x, $0) }
            } else if (isVert()) {
                return rows().map { Point($0, p1.y) }
            } else {
                return zip(rows(), cols()).map { (x,y) in Point(x,y) }
            }
        }
        
        public var description: String {
            "\(p1.x),\(p1.y) -> \(p2.x),\(p2.y)"
        }
    }
    
    struct Input {
        
        let vectors : [Vector]
    }
    
    typealias Output = Int
    
    
    
    func parsePoint(_ pt : String) -> Point {
        let split = pt.components(separatedBy: ",")
        return Point(Int(split[0])!, Int(split[1])!)
    }
    
    func parseInput(_ inp : String) -> Input {
        Input(
            vectors: inp.components(separatedBy: "\n").filter { !$0.isEmpty }.map { line in
                let split = line.components(separatedBy: " -> ")
                return Vector(parsePoint(split[0]), parsePoint(split[1]))
            }
        )
    }
    
    func problem1(_ input: Input) -> Output {
        let horiz = input.vectors.filter { $0.isHoriz() }
        let vert = input.vectors.filter { $0.isVert() }
        print("Found \(horiz.count) horizontal vectors and \(vert.count) vertical vectors")
        
        var lookup : [Point:Int] = [:]
        for vector in horiz {
            for y in vector.cols() {
                lookup[Point(vector.p1.x, y), default: 0] += 1
            }
        }
        
        for vector in vert {
            for x in vector.rows() {
                lookup[Point(x, vector.p1.y), default: 0] += 1
            }
        }
        
        return lookup.values.filter { $0 > 1 }.count
    }
    
    func problem2(_ input: Input) -> Output {
        var lookup : [Point:Int] = [:]
        
        for vector in input.vectors {
            for point in vector.points() {
                lookup[point, default: 0] += 1
            }
        }
        
        return lookup.values.filter { $0 > 1 }.count
    }
}

